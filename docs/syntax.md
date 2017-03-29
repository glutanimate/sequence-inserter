## Sequence Inserter Syntax Specification

<!-- MarkdownTOC -->

- [General Syntax Components](#general-syntax-components)
- [General Tag Fields](#general-tag-fields)
    - [Required fields](#required-fields)
    - [Tag types](#tag-types)
    - [Item sources](#item-sources)
    - [Sample specification](#sample-specification)
    - [Additional fields](#additional-fields)
- [Subsequence Tags](#subsequence-tags)

<!-- /MarkdownTOC -->


### General Syntax Components

These markers cannot be used anywhere within the inline content of the sequence.

- Outer tag delimiter: `||`
- Field separator: `::`
- In-field tag delimiter: `|`
- In-field separator: `,`

### General Tag Fields

#### Required fields

These need to be present for each tag. Their order has to be preserved.

    ||tag_type::item_source::sample||

#### Tag types

The `tag_type` field has to point to one of the following tag type identifiers:

##### `rset`

A random unordered set of items. Duplicates may occur across different instances of the tag.

Supported item sources: inline collections, external collections, generators (int, float)

Example: `||rset::int::1|| – ||rset::int::2|| – ||rset::int::1||`

Result: `4 – 1, 3 – 4`

##### `set`

A uniquely random unordered set of items. No duplicates across different instances of the tag. If the draw of random elements is exhausted, the add-on will advise you accordingly.

Supported item sources: inline collections, external collections, generators (int)

Example: `||set::int::1,1,3|| – ||set::int::1,1,3|| – ||set::int::1,1,3|| – ||set::int::1,1,3||`

Result: `3 – 1 – 2 – [unique items exceeded]`

##### `seq`

An ordered sequence of items. No duplicates across different instances of the tag. Each subsequent tag moves further down the sequence.

Supported item sources: inline collections, external collections, generators (int)

Example: `||seq::int::1|| – ||seq::int::1|| – ||seq::int::1|| – ||seq::int::1||`

Result: `1 – 2 – 3 – 4`

##### `pick`

Selects items of a given collection by their index number. Follows existing order of items.

Supported item sources: inline collections, external collections

Example: `||pick::fruit|apple,orange,banana::1|| – ||pick::fruit::1|| – ||pick::fruit::3||`

Result: `apple – apple – banana`

##### `rpick`

Selects items of a randomized instance of a given collection. All instances of the tag pick from the same randomized instance, meaning that multiple references to the same index numbers will always yield the same item on that card viewing.

Supported item sources: inline collections, external collections

Example: `||rpick::fruit|apple,orange,banana::1|| – ||rpick::fruit::1|| – ||rpick::fruit::3||`

(randomized instance: `orange, banana, apple`)

Result: `orange – orange – apple`

#### Item sources

Items can be supplied through three different means: inline collections, external collections, and generators.

##### Inline collections

`item_source` syntax: `collection_identifier|comma,separated,items`

Inline collections offer a quick way to define item sources without having to modify the config file. Once an inline collection is defined for a card, the `collection_identifier` may be used to reference that collection in subsequent instances of the tag on that card.

Example:

    ||rset::fruit|apple,orange,banana::1|| # first instance
    ||pick::fruit::3|| # subsequent references

i.e. "Choose one random item from the newly defined fruit collection" and "Pick item nr.3 out of that inline collection"

##### External collections

`item_source` syntax: `collection_identifier`

External collections have to be set up in the `cols.py` file in the add-on directory. This file persists across add-on updates and reinstallation and is the main configuration file for Sequence Inserter.

The `collection_identifier` needs to point to a key within the `collections` directory in `cols.py`. For more information on how to set-up external collections, please consult the inline documentation in `cols.py`.

Example:

    ||rset::abc:4|| # abc defined in cols.py

i.e.: "Choose a random set of 4 items from the 'abc' collection"

##### Generators

`item_source` syntax: `generator_identifier`

Generators can create a random or sequential set of numbers on-demand. The following `generator_identifiers` can currently be referenced:

- `int`: produces a series of integers
- `float`: produces a series of rational numbers, rounded to two decimals by default

Example:

    ||rset::int::4||

i.e. "Generate a random set of 4 integers"

For tag types that require unique items (e.g. `set/seq`), generators will produce items that are unique to a given range.

For instance, the sequences `||seq:int::1,1,20||` (range 1-20) and `||seq:int::1,10,30||` (range 10-30) will be kept track of independently.

#### Sample specification

The role of the `sample` field differs based on the tag type and item source. Multiple numbers in the `sample` field have to either be separated by a comma or a semicolon.

##### Collections

- *rset/set/seq*: single integer, specifying the number of items to draw
- *pick/rpick*: one or more integers, refering to index numbers of a collection, e.g.: `pick::fruit::1,3,4` (i.e. "pick fruit number 1, 3, and 4")

##### Generators

- *rset/set/seq*: **either** one **or** three integers. If just one integer is supplied, the add-on will draw that number of items from a default range (0-100). To customize that range you can supply an additional lower and upper bound, e.g.: `rset::int::3;10,30` (i.e. "3 random integers between 10 and 30")


#### Additional fields

These are optional and follow the syntax below:

    option_key|value

Please make sure to always supply them after ther required fields:

    ||tag_type::item_source::sample::option_key|value||

The following options are currently available:

**`dlm`**

Defines a custom item delimiter. If not supplied, the add-on will fall back to the default (`, `).

Example:

    ||rpick::fruit|apple,orange,banana::3::dlm| – ||

Possible result:

    orange – apple – banana


### Subsequence Tags

The user configuration file (`cols.py`) may also be used to define quick-access tags for predefined sequences. Items in the `subsequences` dictionary in `cols.py` can be referenced in fields using the following syntax:

    ||subsequence_key||

Example:

    ||O||

i.e.: "Insert the subsequence 'O', as defined in the subsequences dictionary"

Please refer to the inline documentation in `cols.py` on how to define a subsequence.
