from datetime import datetime
from os.path import abspath, dirname, join
import unittest

from lanyon.app import Site


class ReadInputTests(unittest.TestCase):
    """Tests for reading and associating input files"""

    def setUp(self):
        self.fixture_dir = join(
            dirname(abspath(__file__)), 'fixtures', 'readinput')
        self.settings = dict(project_dir=self.fixture_dir)

    def test_hidden_files_and_directories(self):
        """
        Given an input directory that has hidden files and directories.
        The returned data shouldn't include them.
        """
        settings = self.settings
        settings['input_dir'] = join(self.fixture_dir, 'hidden')
        site = Site(self.settings)
        self.assertEqual({}, site._read_input())

    def test_empty_input_dir(self):
        """
        Given an empty or nonexisting input directory test that 
        an empty dict is returned.
        """
        settings = self.settings
        settings['input_dir'] = join(self.fixture_dir, 'DFGHJK')
        site = Site(self.settings)
        self.assertEqual({}, site._read_input())

    def test_not_associate_in_root_input_dir(self):
        """
        Given an input directory that has articles and media files
        in the top level directory. The files should not be associated.
        """
        settings = self.settings
        settings['input_dir'] = join(self.fixture_dir, 'no_root_assoc')
        site = Site(self.settings)
        result = site._read_input()

        expected_articles = [join(settings['input_dir'], 'article.rst')]
        expected_media = [join(settings['input_dir'], f)
                          for f in ('media1', 'media2')]
        expected = (expected_articles, expected_media)

        self.assertEqual(result[settings['input_dir']], expected)

    def test_associate_in_same_dir(self):
        """
        Given an input directory that has an article with media
        files in a subdirectory. The files should be associated.
        """
        settings = self.settings
        settings['input_dir'] = join(self.fixture_dir, 'same_dir')
        site = Site(self.settings)
        result = site._read_input()
        article_dir = join(settings['input_dir'], 'some-article')

        expected_articles = [join(article_dir, 'index.rst')]
        expected_media = [join(article_dir, 'media')]
        expected = (expected_articles, expected_media)

        self.assertEqual(result[article_dir], expected)

    def test_associate_with_article_in_parent_dir(self):
        """
        Given an input directory that has an article in a subdirectory.
        The article has media files in subdirectory. The media files should
        be associated with the article in the parent dir.
        """
        settings = self.settings
        settings['input_dir'] = join(self.fixture_dir, 'parent_dir')
        site = Site(self.settings)
        result = site._read_input()
        article_dir = join(settings['input_dir'], 'article')

        expected_articles = [join(article_dir, 'index.rst')]
        expected_media = [join(article_dir, 'media', 'mediafile')]
        expected = (expected_articles, expected_media)

        self.assertEqual(result[article_dir], expected)

    def test_associate_with_root_if_no_parent_article(self):
        """
        Given an input directory that has media files in a subdirectory.
        The media files have no article in the parent directories and should
        be associated with the root input dir.
        """
        settings = self.settings
        settings['input_dir'] = join(self.fixture_dir, 'no_parent_article')
        site = Site(self.settings)
        result = site._read_input()

        expected_articles = []
        expected_media = [join(settings['input_dir'], 'media',
                               'images', 'file')]
        expected = (expected_articles, expected_media)

        self.assertEqual(result[settings['input_dir']], expected)

if __name__ == '__main__':
    unittest.main()

