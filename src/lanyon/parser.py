import datetime
import re
from os.path import splitext

class ParserException(Exception):
    """Exception raised for errors during the parsing."""
    pass

class Parser(object):
    output_ext = None

    def __init__(self, settings, source):
        self.settings = settings
        self.source = source
        self.headers = {}
        self.text = ''

    def _parse_headers(self):
        """
        Parses and removes the headers from the source.
        """
        META_RE = re.compile(
            r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
        lines = self.source.splitlines()
        for num, line in enumerate(lines):
            match = META_RE.match(line)
            if match:
                key = match.group('key').strip().lower()
                value = match.group('value').strip()
                if value:
                    # custom header transformation
                    header_method = getattr(self, '_parse_%s_header' % key,
                                            None)
                    if header_method:
                        value = header_method(value)
                    self.headers[key] = value
                    num_last_match = num
            else:
                break
        # remove header lines from input source
        try:
            del lines[:num_last_match + 1]
        except UnboundLocalError:
            pass

        # check if a blank line followed the header lines and remove it
        try:
            if not lines[0]:
                del lines[0]
        except IndexError:
            pass
        self.text = '\n'.join(lines)

    def _parse_tags_header(self, value):
        """
        Parses the value from the 'tags' header into a list.
        """
        return [t.strip() for t in value.split(',')]

    def _parse_date_header(self, value):
        """
        Parses the date header into a python datetime.datetime object.
        The value must be in the format as specified by the 'date_format'
        setting; otherwise a ParserException will be thrown.
        """
        format = self.settings['date_format']
        try:
            return datetime.datetime.strptime(value, format)
        except ValueError as error:
            raise ParserException(error)

    def _parse_updated_header(self, value):
        return self._parse_date_header(value)

    def _parse_status_header(self, value):
        """
        Checks that the value of the 'status' header is 'live', 'hidden' or
        'draft'. If not 'live' is returned.
        """
        if value in ('live', 'hidden', 'draft'):
            return value
        return 'live'

    def _parse_text(self):
        """
        Returns the raw input text. Override this method to process
        text in another markup language such as Markdown.
        """
        return self.text

    def parse(self):
        self._parse_headers()
        self._parse_text()
        return (self.headers, self.text)


class RstParser(Parser):
    """ReStructuredText Parser"""
    output_ext = 'html'

    def pygments_directive(self, name, arguments, options, content, lineno,
                           content_offset, block_text, state, state_machine):
        """
        Parse sourcecode using Pygments

        From http://bitbucket.org/birkenfeld/pygments-main/src/tip/external/rst-directive-old.py
        """
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import get_lexer_by_name, TextLexer
        from docutils import nodes

        try:
            lexer = get_lexer_by_name(arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        formatter = HtmlFormatter(noclasses=False)
        parsed = highlight(u'\n'.join(content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]
    pygments_directive.arguments = (1, 0, 1)
    pygments_directive.content = 1

    def _parse_text(self):
        try:
            from docutils.core import publish_parts
            from docutils.parsers.rst import directives
        except ImportError:
            raise Exception("The Python docutils library isn't installed.")
        else:
            # if pygments is installed, register the "sourcecode" directive
            try:
                import pygments
            except ImportError:
                pass
            else:
                directives.register_directive('sourcecode',
                                              self.pygments_directive)
            self.text = publish_parts(source=self.text,
                                      settings_overrides={
                                            "doctitle_xform": False,
                                            "initial_header_level": 2
                                      },
                                      writer_name='html4css1')['fragment']


class MarkdownParser(Parser):
    """Markdown Parser"""
    output_ext = 'html'

    def _parse_text(self):
        try:
            import markdown
        except ImportError:
            raise Exception("The Python markdown library isn't installed.")
        else:
            self.text = markdown.markdown(self.text,
                                          ['codehilite(css_class=highlight)'])


# a mapping of file extensions to the corresponding parser class
parser_map = (
    (('html', 'htm', 'xml', 'txt'), Parser),
    (('rst',), RstParser),
    (('md', 'markdown'), MarkdownParser),
)


def get_parser_for_filename(filename):
    """
    Factory function returning a parser class based on the file extension.
    """
    ext = splitext(filename)[1][1:]
    try:
        return [pair[1] for pair in parser_map if ext in pair[0]][0]
    except IndexError:
        return
