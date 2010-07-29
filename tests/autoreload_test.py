from datetime import datetime
from os.path import abspath, dirname, join
import unittest

from lanyon.autoreload import get_mtimes, files_changed


class AutoreloadTests(unittest.TestCase):
    """Tests for the autoreloading of the integrated webserver"""

    def setUp(self):
        self.fixture_dir = join(
            dirname(abspath(__file__)), 'fixtures', 'autoreload')

    def test_get_mtimes(self):
        """
        Given a directory path the method should return a dict with
        the files under that directory as the key and the mtime as the value.
        """
        expected_files = [join(self.fixture_dir, f)
                          for f in ('file', join('dir', 'anotherfile'))]
        result = get_mtimes(self.fixture_dir)
        for expected_file in expected_files:
            self.assert_(expected_file in result)
            self.assert_(isinstance(result[expected_file], float))

    def test_files_changed_key_not_in_first(self):
        """
        Given two dicts check if True is returned if a key is not in the
        first dict.
        """
        d2 = dict(foo='bar')
        d1 = dict()
        result = files_changed(d1, d2)
        self.assert_(result)

    def test_files_changed_key_not_in_second(self):
        """
        Given two dicts check if True is returned if a key is not in the
        second dict.
        """
        d1 = dict(foo='bar')
        d2 = dict()
        result = files_changed(d1, d2)
        self.assert_(result)

    def test_files_changed_different_value(self):
        """
        Given two dicts with the same keys but different values. Check that
        True is returned.
        """
        d1 = dict(foo=123)
        d2 = dict(foo=456)
        result = files_changed(d1, d2)
        self.assert_(result)

    def test_files_changed_same_value(self):
        """
        Given two dicts with the same keys and values. Check that
        False is returned.
        """
        d1 = dict(foo=123)
        d2 = dict(foo=123)
        result = files_changed(d1, d2)
        self.assert_(not result)

if __name__ == '__main__':
    unittest.main()

