# -*- coding: utf-8 -*-

"""
This file is part of the Sequence Inserter add-on for Anki

Main Module, hooks add-on methods into Anki

Copyright: Glutanimate 2017
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

import re

from aqt import mw

import anki
from anki.collection import _Collection
from anki.sound import stripSounds

from anki.consts import *
from anki.utils import splitFields
from anki.hooks import addHook, remHook, runFilter, wrap

from .parser import Parser

tag_regex = r"\|\|(.*?)\|\|"

def _renderQA(self, data, qfmt=None, afmt=None):
    "Returns hash of id, question, answer."
    # data is [cid, nid, mid, did, ord, tags, flds]
    # unpack fields and create dict
    flist = splitFields(data[6])
    fields = {}
    model = self.models.get(data[2])
    for (name, (idx, conf)) in self.models.fieldMap(model).items():
        fields[name] = flist[idx]
    fields['Tags'] = data[5].strip()
    fields['Type'] = model['name']
    fields['Deck'] = self.decks.name(data[3])
    fields['Subdeck'] = fields['Deck'].split('::')[-1]
    if model['type'] == MODEL_STD:
        template = model['tmpls'][data[4]]
    else:
        template = model['tmpls'][0]
    fields['Card'] = template['name']
    fields['c%d' % (data[4]+1)] = "1"

    # render q & a
    d = dict(id=data[0])
    qfmt = qfmt or template['qfmt']
    afmt = afmt or template['afmt']
    for (type, format) in (("q", qfmt), ("a", afmt)):
        if type == "q":
            format = re.sub("{{(?!type:)(.*?)cloze:", r"{{\1cq-%d:" % (data[4]+1), format)
            format = format.replace("<%cloze:", "<%%cq:%d:" % (
                data[4]+1))
        else:
            format = re.sub("{{(.*?)cloze:", r"{{\1ca-%d:" % (data[4]+1), format)
            format = format.replace("<%cloze:", "<%%ca:%d:" % (
                data[4]+1))
            fields['FrontSide'] = stripSounds(d['q'])
        fields = runFilter("mungeFields", fields, model, data, self)
        html = anki.template.render(format, fields)
        d[type] = html
    ############################
    tags = getTagMatches(d["a"])
    cid = data[0]
    if tags:
        if hasattr(self, "_spLast") and self._spLast == cid and tags == self._spTags:
            # preserve last replacements across card reloading
            # (required for: previewer, card templates editor)
            replacements = self._spRepl
        else: 
            seq_parser = Parser()
            replacements = seq_parser.parse(tags)
            self._spLast = cid
            self._spTags = tags
            self._spRepl = replacements
    else:
        if hasattr(self, "_spTags"):
            del self._spTags
        if hasattr(self, "_spRepl"):
            del self._spRepl
        if hasattr(self, "_spLast"):
            del self._spLast
    for type in ("q", "a"):
        html = d[type]
        if tags:
            format_str = getFormatString(html)
            html = formatTagString(format_str, replacements)
        d[type] = runFilter(
            "mungeQA", html, type, fields, model, data, self)
        # empty cloze?
        if type == 'q' and model['type'] == MODEL_CLOZE:
            if not self.models._availClozeOrds(model, data[6], False):
                d['q'] += ("<p>" + _(
            "Please edit this note and add some cloze deletions. (%s)") % (
            "<a href=%s#cloze>%s</a>" % (HELP_SITE, _("help"))))
    #############################
    return d

def getTagMatches(html):
    """Search for sequence tags in html"""
    return re.findall(tag_regex, html)

def getFormatString(html):
    """Replace sequence tags in html with placeholders"""
    ret = html.replace("{", "{{").replace("}", "}}") # escape existing brackets
    return re.sub(tag_regex, "{}", ret)

def formatTagString(format_str, replacements):
    """Replace placeholders with final strings"""
    formatted = format_str.format(*replacements)
    formatted = formatted.replace("{{", "{").replace("}}", "}") # unescape brackets
    return formatted

def tagMungeQA(html, type, fields, model, data, col):
    # TODO?: update latex processor, so that the same hash is used for all
    # images (in order to prevent image proliferation in the media collection)
    pass

def cleanup():
    """Reset state when exiting reviewer"""
    if hasattr(mw.col, "_spTags"):
        del mw.col._spTags
    if hasattr(mw.col, "_spRepl"):
        del mw.col._spRepl
    if hasattr(mw.col, "_spLast"):
        del mw.col._spLast

addHook("reviewCleanup", cleanup)
_Collection._renderQA = _renderQA