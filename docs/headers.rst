.. _headers:

Headers
=======

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

URL Header
----------

There are several ways to specify an output URL/directory. The simplest one is to write it in the article itself::

    url: 2009/05/05/foobar.html

or, in case you want to hide the .html extension, append a slash at the end::

    url: 2009/05/05/foobar/

The rendered article will then be written to a ``index.html`` file in the foobar directory.

Variables
~~~~~~~~~

You can use variables in the URL header. They must be prefixed by a dollar sign. Example::
    
    url: $year/$month/$day/$slug.$ext

The following variables are available:

**year**
    The year from the parsed "date" header
**month**
    The month from the parsed "date" header
**day**
    The day of the parsed "date" header
**slug**
    The filename of the article or, in case the article is named "index.*" (e.g. index.rst) and not in the root input directory, the parent directory name.
**ext**
    The output extension as set by the parser (currently all parsers use "html")

Named URL Patterns
~~~~~~~~~~~~~~~~~~

You can use names to refer to url patterns::

    url: pretty

If you don't specify an url, the "default" rule is used. The following named url patterns are available:

**default**
    The directory hierarchy from the input directory is used to determine the output path. (/input/foo/bar.rst -> /output/foo/bar.html)
**pretty**
    ``$year/$month/$day/$slug/``

Custom Named URL Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

Custom url patterns go into the ``urls.py`` file inside the project directory.

Here's an example that defines a ``slug_only`` url pattern (the function name is used as the pattern name). This url will write articles into the root output directory::

    from os.path import basename, splitext
    from lanyon.url import register

    @register
    def slug_only(**kwargs):
        path = kwargs['path']
        output_ext = kwargs['extension']
        filename, ext = splitext(basename(path))
        url = filename + '.' + output_ext
        return url

You can now use the ``slug_only`` url pattern in your articles::

    url: slug_only

The following values are available in the keyword argument ``kwargs``:

**path**
    The relative path from the input directory to the article file (e.g. "foo/bar/index.rst")
**extension**
    The output extension as specified by the parser (currently always "html")
**headers**
    The parsed article headers.

Bonus tip: You can use the same variables as described `above <#variables>`_::

    from lanyon.url import register

    @register
    def slug_only(**kwargs):
        return '$slug.$ext'

URLs patterns for specific paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The register decorator optionally takes a ``match`` argument. This argument allows you to specify a URL for files that match a specific input path. The value of the match argument must be a ``fnmatch`` pattern like ``articles/*``. If no match argument is specified the default value ``*`` is used.

Here is an example that will override the default URL pattern and write all articles to ``writing/$slug/`` unless they are in the ``old/`` directory, in which case they will be written to ``$year/$month/$day/$slug/``::


    from lanyon.url import register

    @register
    def default(**kwargs):
        return 'writing/$slug/'

    @register(match='articles/old/*')
    def default(**kwargs):
        return '$year/$month/$day/$slug/'

