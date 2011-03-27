.. _installation:

Installation
============

The easiest way to get lanyon is if you have pip_ installed::

	pip install lanyon

Without pip, it's still pretty easy. Download the lanyon.tar.gz file
from `lanyon's PyPI page`_, untar it and run::

	python setup.py install

.. _lanyon's PyPI page: http://pypi.python.org/pypi/lanyon/
.. _pip: http://pip.openplans.org/

Dependencies
------------

- Python 2.6
- Jinja 2.2
- docutils 0.6 (optional; only if you want to use the rst parser)
- python-markdown (optional; only if you want to use the markdown parser)
- Pygments 1.1 (optional; only if you want to use syntax highlighting)

If you want to install all optional dependencies, you can run the
following command::

    pip install pygments docutils markdown lanyon
