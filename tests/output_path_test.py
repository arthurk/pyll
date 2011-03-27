import unittest
from lanyon.app import Site


class OutputPathTests(unittest.TestCase):
    """Tests that the output path is computed correctly."""

    def setUp(self):
        self.settings = dict(input_dir='/input/', output_dir='/output/')
        self.site = Site(self.settings)

    def test_absolute_url(self):
        """
        Check that absolute urls like "/foo/bar/baz.html" are joined with the
        output path, and do not start at the root of the filesystem.
        """
        url = '/foo/bar.html'
        expected = '/output/foo/bar.html'
        result = self.site._get_output_path(url)
        self.assertEquals(expected, result)

    def test_directory_url(self):
        """
        Check that "index.html" is appended to urls that are a directory
        (like "foo/bar/").
        """
        url = 'foo/bar/'
        expected = '/output/foo/bar/index.html'
        result = self.site._get_output_path(url)
        self.assertEquals(expected, result)

    def test_filename_url(self):
        """
        Check that a url which is a filename ("foo/bar.html) is not changed
        and joined with the output directory.
        """
        url = 'foo/bar.html'
        expected = '/output/foo/bar.html'
        result = self.site._get_output_path(url)
        self.assertEquals(expected, result)

if __name__ == '__main__':
    unittest.main()
