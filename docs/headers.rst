.. _headers:

Article Headers
===============

Articles can specify metadata ("headers") in the form of key:value pairs at
the top of an article. 

Following is a list of header fields that are special to lanyon. These
header fields will use a default value if not specified, and are thus always
available in the template context.

**date**
    Publication date in %Y-%m-%d format, e.g., 2009-12-03. Defaults to 
    the file's ctime.
**status**
    Value must be ``live``, ``hidden`` or ``draft``. Defaults to ``live``.
**template**
    Path to a Jinja2 Template file or "self".
    If not specified this will default to "default.html".
**title**
    The article's title. Default is the filename without the extension e.g.
    "Foobar" for "foobar.rst".
**url**
    Output path. Default is the relative path to article file e.g.
    if the article is in "2011/09/09/article.rst" the output will be written
    to "2011/09/09/article.html". If the url is a directory, the article will
    be written in a file named "index.html" e.g. "url: 2011/09/09/" will
    be written to "2011/09/09/index.html".
**slug**
    URL-safe representation of the title. Default value is the filename or,
    if the filename is "index", the directory name of the parent directory
    (unless its the top level directory).

You can also specify your own custom header fields and access them in the
template.

Example::

    title: Hello World!
    date: 2009-12-12
    tags: example, helloworld
    url: 2009/dec/12/
    foo: bar

    Hello, World!

