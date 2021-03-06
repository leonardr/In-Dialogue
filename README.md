In Dialogue
===========

a 2013 NaNoGenMo project

by Leonard Richardson

"In Dialogue" extracts the dialogue from Project Gutenberg ebooks and
provides a tool for replacing all the dialogue from one text with
dialogue from another.

The NaNoGenMo entry itself is in two parts found in the entry/
directory, and can also be 
[read on my web site](http://www.crummy.com/software/NaNoGenMo-2013/).

To generate your own texts, run `0-extract-dialogue.py`, then
`1-generate-book.py`. The `1-generate-book.py` script will show you
which texts are available.

You can add new texts by downloading Project Gutenberg files into the
raw/ directory. For example, these commands will add "Oliver Twist" to
the list of available texts:

`$ wget http://www.gutenberg.org/ebooks/730.txt.utf-8 -O raw/730.txt.utf-8`
`$ ./0-extract-dialogue.py`

Then, this command prints the text of "A Christmas Carol", with all
the dialogue replaced with dialogue from "Oliver Twist":

`$ ./1-generate-book.py "A Christmas Twist" 46 730`
