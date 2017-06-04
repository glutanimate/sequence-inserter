# -*- coding: utf-8 -*-

"""
This file is part of the Sequence Inserter add-on for Anki

Common reusable utilities

Copyright: Glutanimate 2017
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""


def select(lst, idxs):
    """Pick out multiple list items by their indexes"""
    try:
        return [lst[i] for i in idxs]
    except IndexError:
        return lst
