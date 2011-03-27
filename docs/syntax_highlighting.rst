.. _syntax_highlighting:

Syntax Highlighting
===================

If you have Pygments installed, it's possible to highlight code in ReStructuredText and Markdown articles.

ReStructuredText
----------------

To highlight syntax in ReStructuredText articles, use the “sourcecode” directive::

    .. sourcecode:: python

        print "hello!"

Markdown
--------

The CodeHilite extension is used to highlight syntax in Markdown articles (its included in the markdown package and installed by default)::

    :::python
    print "hello!"

