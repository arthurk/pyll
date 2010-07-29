from datetime import datetime
from os.path import abspath, dirname, join
import unittest

from lanyon.app import Site


class ParseTests(unittest.TestCase):

    def setUp(self):
        project_dir = join(dirname(abspath(__file__)),
                           'fixtures', 'parse')
        self.settings = dict(project_dir=project_dir,
                             input_dir=join(project_dir, 'input'),
                             output_dir=join(project_dir, 'output'),
                             date_format='%Y-%m-%d')
        self.site = Site(self.settings)
        input_data = self.site._read_input()
        self.site._parse(input_data)

    def test_parse_drafts(self):
        """
        Articles with the draft status shouldn't be processed.
        """
        for article in self.site.articles:
            self.assertNotEqual(article.headers['status'], 'draft')

    def test_parse_future_dated(self):
        """
        Articles with a date in the future shouldn't be processed.
        """
        for article in self.site.articles:
            self.assert_(article.headers['date'] <= datetime.today())

    def test_parse_media_association(self):
        """
        Test that media is correctly associated to articles.

        This means that media in the input directory should not be
        associated to any articles.
        Media that is in the same directory as an article or has a parent
        directory with an article in it, should be associated.
        """
        self.assertEqual(self.site.media,
                         [join(self.settings['input_dir'], 'mediafile')])
        for article in self.site.articles:
            if article.headers['url'] == 'foo/bar.html':
                expected_media = [join(self.settings['input_dir'],
                                  'foo', 'mediafile')]
            else:
                expected_media = []
            self.assertEqual(article.media, expected_media)

if __name__ == '__main__':
    unittest.main()

