import unittest
import datetime

from lanyon.parser import Parser, RstParser, MarkdownParser,\
                          get_parser_for_filename, ParserException


class ParserFactoryTests(unittest.TestCase):
    """Tests for the Parser factory functions."""

    def test_parser_class(self):
        """
        Test that a the correct parser class is returned for
        a file extension.
        """
        test_data = [
            ('file.rst', RstParser),
            ('file.md', MarkdownParser),
            ('file.markdown', MarkdownParser),
            ('file.html', Parser),
            ('file.htm', Parser),
            ('file.xml', Parser),
            ('file.xhtml', None),
            ('file.png', None),
            ('', None)]
        for data in test_data:
            self.assertEqual(get_parser_for_filename(data[0]), data[1])


class ParserTests(unittest.TestCase):
    """Tests for the Parser class."""

    def _check_result(self, text, expected):
        """Runs the parser and compares the result with the expected value."""
        parser = Parser({'date_format': '%Y-%m-%d'}, text)
        result = parser.parse()
        self.assertEquals(result, expected)

    def test_header_parsing(self):
        """
        Test that header fields followed by a new line return the correct
        header dict and text.
        """
        text = 'foo: bar\n123:345\nfoo bar'
        expected = ({'foo': 'bar', '123': '345'}, 'foo bar')
        self._check_result(text, expected)

    def test_header_parsing_strips_newline(self):
        """
        Test that a newline after the headers and before the
        text is stripped.
        """
        text = 'foo: bar\n123:345\n\nfoo bar'
        expected = ({'foo': 'bar', '123': '345'}, 'foo bar')
        self._check_result(text, expected)

    def test_no_headers(self):
        """
        Test that no headers return an empty dict.
        no headers should return ({}, '')
        """
        text = ''
        expected = ({}, '')
        self._check_result(text, expected)

    def test_no_headers_but_text(self):
        """
        Test that if no headers but text is specified, an empty dict and
        the correct text is returned.
        """
        text = 'hah!'
        expected = ({}, 'hah!')
        self._check_result(text, expected)

    def test_header_no_value(self):
        """
        Test that a header field is not returned if there was no value
        specified.
        """
        text = 'foo:'
        expected = ({}, 'foo:')
        self._check_result(text, expected)

    def test_whitespace_after_delimiter(self):
        """
        Test that the whitespace after the delimiter still returns the 
        correct results.

        should be the same as foo:bar and 'foo  :  bar'(?)
        """
        text = 'foo:       bar'
        expected = ({'foo': 'bar'}, '')
        self._check_result(text, expected)

    def test_tag_header(self):
        """
        Test that the value from a header field called 'tags' is
        transformed into a list.

        'tags: foo, bar' ----> ['foo', 'bar',]
        """
        text = 'tags: foo, bar'
        expected = ({'tags': ['foo', 'bar']}, '')
        self._check_result(text, expected)

    def test_date_header(self):
        """
        Test that a datetime.datetime object is returned for the value
        (in Y-m-d format) of a field named 'date'.
        """
        text = 'date: 2009-01-01'
        expected = ({'date': datetime.datetime(2009, 1, 1, 0, 0)}, '')
        self._check_result(text, expected)

    def test_date_header_wrong_format(self):
        """
        Test that a ParserException is raised when the date is specified
        in the wrong format.
        """
        text = 'date: 01.01.2009'
        expected = ({'date': '01.01.2009'}, '')
        self.assertRaises(ParserException, self._check_result, text, expected)

    def test_status_header(self):
        """
        Test that for a header field named 'status' only the values 'live',
        'draft' or 'hidden' are accpepted.
        """
        status = ('live', 'hidden', 'draft')
        for stat in status:
            text = 'status: %s' % stat
            expected = ({'status': stat}, '')
            self._check_result(text, expected)

    def test_status_header_invalid(self):
        """
        Test that an invalid value for the status header returns 'live'.
        """
        text = 'status: omg'
        expected = ({'status': 'live'}, '')
        self._check_result(text, expected)


class RstParserTests(unittest.TestCase):
    """Tests for the ReStructuredText parser"""

    def _check_result(self, text, expected):
        """Runs the parser and compares the result with the expected value."""
        parser = RstParser({'date_format': '%Y-%m-%d'}, text)
        result = parser.parse()
        self.assertEquals(result, expected)

    def test_parser(self):
        """
        Test that ReStructuredText parsing works.
        """
        text = '*foobar*'
        expected = ({}, u'<p><em>foobar</em></p>\n')
        self._check_result(text, expected)

    def test_doctitle_xform_disabled(self):
        """
        Test that the title is included in the document, if the rst
        document starts with a header and the header is the only one
        in the whole document.
        """
        text = "\nFoobar\n======\n\nhah\n"
        expected = ({}, u'<div class="section" id="foobar">\n<h2>Foobar</h2>\n<p>hah</p>\n</div>\n')
        self._check_result(text, expected)

class MarkdownParserTests(unittest.TestCase):
    """Tests for the Markdown parser"""

    def _check_result(self, text, expected):
        """Runs the parser and compares the result with the expected value."""
        parser = MarkdownParser({'date_format': '%Y-%m-%d'}, text)
        result = parser.parse()
        self.assertEquals(result, expected)

    def test_parser(self):
        """
        Test that the parser parses markdown correctly.
        """
        text = '*foobar*'
        expected = ({}, u'<p><em>foobar</em></p>')
        self._check_result(text, expected)

if __name__ == '__main__':
    unittest.main()

