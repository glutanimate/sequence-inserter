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
from __future__ import unicode_literals
from .utils import select
#
#
#                 Everything below this line can be modified
#--------------------------------------------------------------------------------

########### General instructions for defining strings in Python ###########

# - all strings in this file will be treated as unicode strings by default,
#   meaning you do not have to escape non-ASCII characters or prepend your string
#   with a 'u'
# - strings that contain backslashes and other characters that might have a special
#   meaning should be prepended with an 'r'. This will preven Python from swallowing
#   certain parts of your string up (e.g. r"\ast")

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

rusABC = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")

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


########### Buttons dictionary ###########
#
# Syntax
#
# General syntax:
#
# buttons = {
#     "profile name 1": [
#         {row1},
#         {row2}
#     ],
#     "profile name 2": [
#         {row1},
#         {row2}
#     ]
# }
# 
# Row syntax:
#
# {
#   "btn_dimensions": (width, height), # row-specific btn size
#   "btns": [ # actual buttons
#       {button dictionary 1},
#       {button dictionary 2}
#   ]
# }
#
# Single button dictionary syntax:
#
# {"label": "rn", "description": "Insert random number",
#   "shortcut": "Alt+R", "sequence": "rset::int:1",
#   "deck": "Fruit", "profile": "User 1", 
#   "restrictsize": False}
#
# The "deck" key optionally restricts the button to 
# specific decks.
#
# By default the buttons will use the specified row button
# dimensions for their size. If no btn_dimensions are provided
# the button size will fall back to 20x20 (Anki default).
#
# If you would like a button to scale dynamically to its contents,
# instead, you can set the "restrictsize" button dictionary key
# to False.

buttons = {
    "User 1": [
        {
            "btn_dimensions": (40, 30),
            "btns": [
                {"label": "rn", "description": "Insert random number", 
                    "shortcut": "Alt+R", "sequence": r"||rset::int::1||"},
                {"label": "ra", "description": "Insert random letter", 
                    "shortcut": "Alt+A", "sequence": r"||rset::abc::1||"},
                {"label": "rf", "description": "Insert random fruit", 
                    "shortcut": "Alt+F", "sequence": r"||rset::fruit::1||",
                    "deck": "Fruit"},
            ]
        }, # row 1
        {
            "btn_dimensions": (50, 20),
            "btns": [
                {"label": "*", "description": "Insert LaTeX sequence", 
                    "shortcut": "Alt+L", "sequence": r"\ast"},
                {"label": "π", "description": "Insert LaTeX sequence", 
                    "shortcut": "Alt+P", "sequence": r"\pi"},
            ]
        }, # row 2
    ],
    "User 2": [
        {
            "btn_dimensions": (20, 20),
            "btns": [
                {"label": "rp", "description": "Random element", 
                    "sequence": r"||rset::PeriodicTable::1||"},
                {"label": "rp", "description": "Random element 2", 
                    "sequence": r"||rset::PeriodicTable::2||"},
            ]
        }, # row 1
    ],
}


########### Button options ###########
#
# These options govern the appearance of your custom buttons.
# Here is an example of you how would set up two different profiles
# to display different fonts and font sizes, respectively:
#
# options = {
#     "User 1": {
#         "labelFont": "Times New Roman",
#         "labelSize": 12 # no quotes!
#     },
#     "User 2": {
#         "labelFont": "Segoe UI Symbol",
#         "labelSize": 14 # no quotes!
#     },
# }
#
# If a value is left empty, the add-on will fall back to Anki's
# app-wide defaults.

options = {
    "User 1": {
        "labelFont": "",
        "labelSize": None # no quotes!
    },
    "User 2": {
        "labelFont": "",
        "labelSize": None # no quotes!
    },
}