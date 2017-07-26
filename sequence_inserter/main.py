# -*- coding: utf-8 -*-

"""
This file is part of the Sequence Inserter add-on for Anki

Main Module, hooks add-on methods into Anki

Copyright: Glutanimate 2017
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

import re

from aqt.qt import *
from aqt import mw
from aqt.utils import shortcut
from aqt.editor import Editor
from aqt.addcards import AddCards
from aqt.editcurrent import EditCurrent

import anki
from anki.collection import _Collection
from anki.sound import stripSounds

from anki.consts import *
from anki.utils import splitFields, isWin, isMac, json
from anki.hooks import addHook, remHook, runFilter, wrap


# create user collections file if it doesn't exist
try:
    import cols
except ImportError:
    import os
    from shutil import copyfile
    p = os.path.dirname(__file__)
    copyfile(os.path.join(p, "cols_dflt.py"),
        os.path.join(p, "cols.py"))

# fall back to default collections if user collections
# can't be imported (e.g.: syntax errors)
try:
    from .cols import buttons, options
except ImportError:
    from .cols_dflt import buttons, options

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


###### Hooks and UI modifications #######


def create_button(self, name, func, key=None, tip=None, size=True, text="",
                  check=False, native=False, canDisable=True):
    """
    Create custom editor button and add it to our own button hbox
    Based on neftas/supplementary-buttons
    """
    button = QPushButton(text)

    if check:
        button.clicked[bool].connect(func)
    else:
        button.clicked.connect(func)

    if size:
        button.setFixedHeight(20)
        button.setFixedWidth(20)

    if not native:
        if self.plastiqueStyle:
            button.setStyle(self.plastiqueStyle)
        button.setFocusPolicy(Qt.NoFocus)
    else:
        button.setAutoDefault(False)

    if key:
        button.setShortcut(QKeySequence(key))

    if tip:
        button.setToolTip(shortcut(tip))

    if check:
        button.setCheckable(True)

    if canDisable:
        self._buttons[name] = button

    self.seq_btnbox.addWidget(button)

    return button


def insertSequence(self, seq):
    """Insert sequence text into current field"""
    self.web.eval("""
        setFormat("inserthtml",{});
    """.format(json.dumps(seq)))

def setupButtons(self):
    """
    Create custom button hbox and insert it below
    default editor toolbar
    """

    parent = self.parentWindow

    deck = None
    if isinstance(parent, AddCards):
        deck = parent.deckChooser.deck.text()
    
    profile = mw.pm.name
    prof_options = options.get(profile, None)

    # set up font for buttons
    font = QApplication.font()
    if prof_options:
        font_family = prof_options.get("labelFont", None)
        font_size = prof_options.get("labelSize", None)
        if font_family:
            font = QFont(font_family)
        if font_size:
            font.setPointSize(font_size)

    # set up custom buttons
    self.seq_btnbox = QHBoxLayout()
    for btn in buttons:
        bdeck = btn.get("deck", None)
        bprofile = btn.get("profile", None)
        if bdeck and deck and bdeck != deck:
            continue
        if bprofile and profile and bprofile != profile:
            continue
        label = btn.get("label", "B")
        shortcut = btn.get("shortcut", "")
        descr = btn.get("description", "")
        size = btn.get("restrictsize", True)
        b = self.create_button(label,
               lambda _, s=btn["sequence"]: self.insertSequence(s),
               key=shortcut,
               tip="{} ({})".format(descr, shortcut),
               text=label, size=size,
               check=False)
        b.setFont(font)
    self.seq_btnbox.insertStretch(0, 1)
    if not isMac:
        self.seq_btnbox.setContentsMargins(0,0,6,0)
        self.seq_btnbox.setSpacing(0)
    else:
        self.seq_btnbox.setMargin(0)
        self.seq_btnbox.setSpacing(14)

    self.outerLayout.insertLayout(1, self.seq_btnbox)


addHook("reviewCleanup", cleanup)
_Collection._renderQA = _renderQA

Editor.insertSequence = insertSequence
Editor.create_button = create_button
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)