# -*- coding: utf-8 -*-

"""
This file is part of the Sequence Inserter add-on for Anki

Sequence generators

Copyright: Glutanimate 2017
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

import random

from .consts import *

def randint(rng, sample, exclude=None):
    """Generate list of random integers"""
    try:
        if not exclude:
            return random.sample(range(*rng), sample)
        sel = set(range(*rng)) - set(exclude)
        return random.sample(sel, sample)
    except ValueError:
        return ["[Unique sequence items exceeded]"]

def randfloat(rng, sample, exclude=None):
    """Generate list of random rounded floats"""
    return [round(random.uniform(*rng), DEFAULT_DECIMALS) for _ in xrange(sample)]

# Register generators in dictionary:

generators = {
    "int": randint,
    "float": randfloat,
}