#!/usr/bin/python

from os import remove
from os.path import abspath, dirname, join, exists
import unittest

from lanyon import utils


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.fixture_dir = join(
            dirname(abspath(__file__)), 'fixtures', 'utils')

    def test_hash_from_path(self):
        """
        Given a filename test that the correct hash is returned.
        """
        result = utils.get_hash_from_path(join(self.fixture_dir, 'myfile'))
        expected = '50b7be4c6f75b67f6226feceb96e3b39'
        self.assertEqual(result, expected)

    def test_copy_file(self):
        """
        Given two paths (src, dst) test that the parent directories
        are created and the file is copied.
        """
        src = join(self.fixture_dir, 'myfile')
        dst = join(self.fixture_dir, 'myfile_copied') 
        self.assert_(not exists(dst))
        utils.copy_file(src, dst)
        self.assert_(exists(dst))

    def tearDown(self):
        # remove copied file from test_copy_file()
        filepath = join(self.fixture_dir, 'myfile_copied')
        if exists(filepath):
            remove(filepath)

if __name__ == '__main__':
    unittest.main()

