from os.path import join, dirname, abspath
import unittest
from datetime import datetime
from lanyon.app import Site

FIXTURE_DIR = join(dirname(abspath(__file__)), 'fixtures', 'default_headers')
SETTINGS = {'input_dir': '/default_headers'}
site = Site(SETTINGS)

class DefaultHeaderTests(unittest.TestCase):
    """Tests for the default headers"""

    def test_values(self):
        """Test that the returned headers are valid."""
        input_filename = join(SETTINGS['input_dir'], 'foobar.rst')
        result = site._get_default_headers(input_filename)
        expected = {
            'status': 'live',
            'template': 'default.html',
            'title': 'Foobar',
            'url': 'default',
            'slug': 'foobar'
        }
        for key in expected:
            self.assertEquals(expected[key], result[key])
        self.assert_(isinstance(result['date'], datetime))

class SlugDefaultHeaderTests(unittest.TestCase):
    """Tests for the slug header default"""

    def test_filename_as_slug(self):
        """Check that the filename is used as the slug."""
        input_filename = join(SETTINGS['input_dir'], 'foobar.rst')
        expected = 'foobar'
        result = site._get_default_headers(input_filename)
        self.assertEquals(expected, result['slug'])

    def test_dirname_as_slug(self):
        """
        Check that the directory name is used as the slug if
        the file is named "index.*".
        """
        input_filename = join(SETTINGS['input_dir'], 'bar', 'index.rst')
        expected = 'bar'
        result = site._get_default_headers(input_filename)
        self.assertEquals(expected, result['slug'])

    def test_index_as_slug(self):
        """
        Check that the filename is used as the slug if the file
        is named "index.*" but is located in the root input dir.
        """
        input_filename = join(SETTINGS['input_dir'], 'index.rst')
        expected = 'index'
        result = site._get_default_headers(input_filename)
        self.assertEquals(expected, result['slug'])

if __name__ == '__main__':
    unittest.main()
