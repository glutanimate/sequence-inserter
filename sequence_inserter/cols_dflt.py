# -*- coding: utf-8 -*-

"""
This file is part of the Sequence Inserter add-on for Anki

(Sub-)collection and subsequence definitions

Copyright: Glutanimate 2017
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

# Please use cols.py for user-defined collections.
# If cols.py is not present, the add-on wil automatically fall back to cols_dflt.py

#################################################################################
#                           Don't modify this part
#--------------------------------------------------------------------------------
#
#
from .utils import select
#
#
#                 Everything below this line can be modified
#--------------------------------------------------------------------------------


###########  Individual (Sub)collections  ###########

# (sub)collections can either be defined inline in the collections dictionary
# below, or as separate list variables that can be referenced in the
# dictionary

# Some list syntax pointers:
#  - comments are preceded with a '#' and either need to be inserted after a linebreak,
#    or at the end of a line
#  - line breaks within lists can only be inserted after a comma

PeriodicTable = ["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron",
"Carbon", "Nitrogen","Oxygen", "Fluorine", "Neon", # 10
"Sodium", "Magnesium", "Aluminium", "Silicon",
"Phosphorus", "Sulfur", "Chlorine", "Argon"] # 18

# lists can be sliced to create sublists ("sub-collections"):

PeriodicTable1 = PeriodicTable[0:10]

# The index for slices starts at 0 for the first element
# The lower bound is inclusive, the upper bound exclusive
# [0:10] will get the first 10 items of the list


# characters in strings can be converted to item lists by using list():

rusABC = list(u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
# (strings with non-ASCII characters need to be preceded with a "u")

# individual list items can be selected with select(list, (indexes))

rusVowels = select(rusABC, (1,6,7,10,13,16,31,29,32,33))

########### Collections dictionary ###########
#
# Syntax:
#
#  collections = {
#    "key1": ["item1", "item2", "itemN"],
#    "key2": ["itemA", "itemB", "itemZ"]
#  }
#
# Also supports (sub)collections defined outside of the dictionary, e.g.:
#
# list_variable = ["item1", "item2", "itemN"]
#
# collections =  {
#   "key": list_variable
# }
#
# list_variables have to be defined before the collections dictionary

collections = {
    "fruit": ["apple", "orange", "banana", "ananas"],
    "colours": ["Red","Orange","Yellow","Brown","White","Green",
                "Cyan","Blue","Indigo","Purple","Violet","Magenta"],
    "com": ["4*5", "5*4"],
    "abc": list("abcdefghijklmnopqrstuvwxyz"),
    "ABC": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "PeriodicTable": PeriodicTable,
    "PeriodicTable1": PeriodicTable1,
    "rusABC": rusABC,
    "rusVowels": rusVowels,
    "Mult": ["a", "0", "b", "c", "ab", "ac"],
    "B5": ["Panthenol", "Pantetheine", "Pantethine", "Coenzyme-A", "Iso-coenzyme-A"]
}

########### Subsequence dictionary ###########
#
# Syntax:
#
# "key": "subsequence_string"
#
# The subsequence string follow the regular tag syntax, just
# without the outer "||" markers (also see syntax.md)


subsequences = {
    "O": "set::PeriodicTable1::2::dlm|. ",
    "M": "seq::Mult::1",
    "S1": "rpick::colours::1,2,3",
    "S2": "rpick::colours::2,3,4",
    "S3": "rpick::colours::1",
    "PA": "set::B5::1"
}