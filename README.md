## Sequence Inserter Add-on for Anki

Allows you to define lists and sequences which can later be referenced in your cards by using a special tag syntax.

For instance, having defined `fruit = ["apple", "orange", "banana"]` as a collection you could reference that collection within your notes using `||set::fruit::1||`. When reviewing your cards this tag would then be randomly assigned a value drawn from the `fruit` collection, i.e.  `apple`, `orange`, or `banana` .

### Features

- 5 different tag types (random set, unique set, sequence, selection, random selection)
- supports inline list definitions as well as references to external collections
- 2 number generators (integers and floats) are provided for convenience
- subsequence tags allow you to reference predefined tags quickly

### Usage

Sequence tags can be inserted anywhere within your fields or card templates. The tag syntax is quite elaborate and explained [in a separate document](https://github.com/Glutanimate/sequence-inserter/blob/master/docs/syntax.md).

You can edit `cols.py` in the add-on directory to define global item collections. This file is user-specific, so your collections will be safe across add-on updates.

Here is a quick example of how the `fruit` collection mentioned above could be defined:

```python
collections {
    "fruit": ["apple", "orange", "banana"]
}
```

Make sure to consult the inline documentation in `cols.py` for more information on the exact collection and subsequence syntax.

### Client Support

Only the desktop releases are supported at this time. Your sequences will not be substituted on AnkiWeb or any of the mobile clients, but rather appear in their literal form.

### Credits and License

*Sequence Inserter* is *Copyright © 2017 [Aristotelis P.](https://github.com/Glutanimate)*

This add-on was developed on a commission by [BB on the Anki support forums](https://anki.tenderapp.com/discussions/add-ons/9504-100-for-add-on-developer-2). All credit for the original add-on idea goes to them.

I'm always happy for new add-on commissions. If you have an idea for an add-on or new feature please feel free to reach out to me on [Twitter](https://twitter.com/glutanimate), or at glutanimate [αt] gmail . com.

Licensed under the [GNU AGPL v3](https://www.gnu.org/licenses/agpl.html).