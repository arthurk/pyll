from datetime import datetime
from os.path import abspath, dirname, join
import unittest

from lanyon.app import Site


class GeneralTests(unittest.TestCase):
    """Tests for reading and associating input files"""

    def setUp(self):
        self.fixture_dir = join(
            dirname(abspath(__file__)), 'fixtures', 'general')
        self.settings = dict(project_dir=self.fixture_dir,
                             input_dir=self.fixture_dir,
                             output_dir=self.fixture_dir,
                             date_format='%Y-%m-%d')
        self.site = Site(self.settings)
        self.site._parse(self.site._read_input())

    def test_filter_public(self):
        """
        Test that non-public articles are filtered out.
        """
        self.assertEqual(len(self.site.articles), 2)
        public_articles = filter(self.site._is_public, self.site.articles)
        self.assertEqual(len(public_articles), 1)

    def test_sort(self):
        """
        Test that articles are sorted by date.
        """
        self.site._sort_articles()
        self.assertEquals(self.site.articles[0].headers['date'],
                          datetime(2009, 2, 2, 0, 0))
        self.assertEquals(self.site.articles[1].headers['date'],
                          datetime(2009, 1, 1, 0, 0))

if __name__ == '__main__':
    unittest.main()

