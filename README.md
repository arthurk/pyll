Pyll
====

Pyll is a Python-Powered Static Site Generator.

Installation
------------

`pip install pyll`

Quickstart
----------

Run `pyll --quickstart mysite` to generate a basic site skeleton.

Usage
-----

Run the `pyll` command to generate a site. The command looks for files
with a .htm/.html, .xml, .rst and .md/.markdown extension and parses them.
Directories and files that start with a dot or an underscore will be ignored.
Everything else will be copied. The generated site will be available
in the `_output` directory.
