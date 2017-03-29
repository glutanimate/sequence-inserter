# -*- coding: utf-8 -*-

"""
This file is part of the Sequence Inserter add-on for Anki

Tag string parser

Copyright: Glutanimate 2017
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

import random

from .consts import *
from .gens import generators


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
    from .cols import collections, subsequences
except ImportError:
    from .cols_dflt import collections, subsequences


class Parser(object):
    """Tag string parser"""

    def __init__(self):
        super(Parser, self).__init__()
        # save inline collections, so that they can be referenced:
        self.inlinecols = {}
        # record items that have been used before:
        self.cur = {
            "rset": None,
            "set": {},
            "seq": {},
            "pick": None,
            "rpick": {}
        }

    def parse(self, tags):
        """Iterate over all tags and call processTag"""
        replacements = [self.processTag(tag) for tag in tags]
        return replacements

    def processTag(self, tag):
        """Return sequence for given tag"""
        invalid = False
        params = tag.split("::")
        if len(params) == 1:
            tag = subsequences.get(params[0], None)
            if not tag:
                invalid = True
            else:
                params = tag.split("::")
        if invalid or len(params) < 3:
            return "[Invalid tag]"
        ttype, ident, sample_str = params[:3]
        if not ttype or not ident or not sample_str:
            return "[Invalid tag]"
        sample = sample_str.replace(";", ",").split(",")

        options = self.getOptions(params[3:])
        stype, orig_col, ident = self.getSource(ident, sample_str)

        rng = None
        try:
            sample = [int(i) for i in sample]
            length = len(sample)
            if ttype not in ("pick, rpick") and stype != "gen":
                assert length == 1
                assert sample[0] >= 1
                sample = int(sample[0])
            elif stype == "gen":
                assert sample[0] >= 1
                if length == 1:
                    rng = (DEFAULT_RANGE[0], DEFAULT_RANGE[1]+1)
                elif length == 3:
                    assert sample[1] < sample[2]
                    rng = (sample[1], sample[2]+1)
                    ident = ident + "%d-%d" % (sample[1], sample[2])
                else:
                    assert False
                sample = int(sample[0])
        except (ValueError, AssertionError):
            return "[Invalid sample]"

        if not orig_col:
            return "[Invalid identifier]"
        if stype == "gen" and ttype not in ("rset", "set", "seq"):
            return "[Invalid tag type for generator]"
        cur_col = self.cur.get(ttype, False)

        if cur_col is False:
            return "[Invalid sequence type]"
        if stype == "gen":
            gen = orig_col
            items = self.genItems(ttype, gen, cur_col, ident, sample, rng)
        else:
            items = self.getItems(ttype, orig_col, cur_col, ident, sample)

        if not items:
            return "[Invalid tag]"

        dlm = options.get("dlm", unicode(DEFAULT_DELIMITER))
        replacement = dlm.join(unicode(i) for i in items)

        return replacement


    def getOptions(self, fields):
        """Parse optional tag parameters"""
        options = {}
        for field in fields:
            try:
                key, val = field.split("|")
            except ValueError:
                continue
            if key in ("rng", "idx"):
                val = val.split(",")
            options[key] = val
        return options

    def getSource(self, ident, sample_str):
        """Identify item source"""
        # inline collections:
        col_inline = self.inlinecols.get(ident, None)
        if col_inline:
            return "inline", col_inline, ident
        inline = ident.split("|")
        if len(inline) == 2:
            ident = inline[0]
            col = inline[1].split(",")
            self.inlinecols[ident] = col
            return "inline", col, ident
        # generators:
        gen = generators.get(ident, None)
        if gen:
            return "gen", gen, ident
        # external collections
        col = collections.get(ident, None)
        if col:
            return "col", col, ident
        return None, None, None

    def genItems(self, ttype, gen, cur_col, ident, sample, rng):
        """Generate list of sequence items"""
        if ttype in ("pick", "rpick"):
            return ["[Generators are incompatible with pick/rpick]"]
        if ttype == "seq" and not ident.startswith("int"):
            return ["[Sequences are only compatible with int]"]
        if cur_col is not None:
            if ident not in cur_col:
                if ttype == "set":
                    # empty list of excluded items
                    cur_col[ident] = []
                elif ttype == "seq":
                    cur_col[ident] = range(*rng)
            current = cur_col[ident]
        ret = None
        popped = None
        if ttype == "rset":
            ret = gen(rng, sample)
        elif ttype == "set":
            ret = gen(rng, sample, current)
            cur_col[ident] += ret # already used
        elif ttype == "seq":
            ret, popped = self.sequencePop(current, sample)
            cur_col[ident] = popped # remaining sequence items
        return ret
    
    def getItems(self, ttype, orig_col, cur_col, ident, sample):
        """Select list of sequence items from collection"""
        if cur_col is not None:
            if ident not in cur_col:
                if ttype in ("set", "rpick"):
                    # shuffle orig_col:
                    cur_col[ident] = self.randomSample(orig_col, len(orig_col))
                elif ttype == "seq":
                    cur_col[ident] = orig_col
            current = cur_col[ident]
        popped = None
        ret = None
        if ttype == "rset":
            ret = self.randomSample(orig_col, sample)
        elif ttype == "set":
            ret, popped = self.sequencePop(current, sample)
        elif ttype == "pick":
            ret = self.sequencePick(orig_col, sample)
        elif ttype == "rpick":
            ret = self.sequencePick(current, sample)
        elif ttype == "seq":
            ret, popped = self.sequencePop(current, sample)
        if popped:
            # record items that have already been used if required
            cur_col[ident] = popped
        return ret

    def sequencePop(self, sequence, sample):
        """Pop the n first items off of a given sequence"""
        if not sequence or sample > len(sequence):
            return ["[Unique sequence items exceeded]"], None
        if len(sequence) == 1:
            return [sequence.pop(0)], sequence
        return sequence[:sample], sequence[sample:]

    def sequencePick(self, sequence, sample):
        """Return and pop the given indices out of the sequence"""
        try:
            if isinstance(sample, int):
                return [sequence[sample-1]]
            else:
                return [sequence[i-1] for i in sample]
        except IndexError:
            return ["[Pick exceeds sequence index]"]

    def randomSample(self, sequence, length=1):
        """Return a random sample list of the sequence"""
        return random.sample(sequence, length)
