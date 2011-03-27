.. _directory_structure:

Directory Structure
===================

Lanyon will look for articles in a directory called “input” and templates in a directory called “templates”. The output will be written to a directory called “output”.

Viewing the Site
----------------

To view your site, start the local webserver with ``lanyon -s``. Lanyon will watch the input and template directories for changes and automatically recompile the site.

Articles/Media Files
--------------------

Lanyon distinguishes between article and media files. Articles are files with a particular file extension (see list below). All other files are considered media files.

**.html .htm .xml**
    Uses the HtmlParser. This will parse only the article headers. The body is not processed.
**.rst**
    Uses the RstParser. Converts ReStructuredText body to html.
**.md .markdown**
    Uses the MarkdownParser. Converts Markdown body to html.

Media files are associated with articles if they are in the same directory. If an article specifies an “url” header, its media files are going to be copied to the same directory as the article.


