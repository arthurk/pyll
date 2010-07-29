from datetime import datetime
from os.path import abspath, dirname, join
import unittest

from lanyon.template import Jinja2Template


class Jinja2TemplateTests(unittest.TestCase):

    def setUp(self):
        template_dir = join(dirname(abspath(__file__)), 'fixtures', 'template')
        self.settings = dict(template_dir=template_dir)
        self.template = Jinja2Template(self.settings)

    def test_render_string(self):
        """
        Test that a template is rendered from a string.
        """
        template_str = 'Welcome, {{ name }}!'
        output = self.template.render_string(template_str, name='arthur')
        self.assertEqual(output, 'Welcome, arthur!')

    def test_render(self):
        """
        Test that a template is rendered from a file name.
        """
        output = self.template.render('detail.html', name='arthur')
        self.assertEqual(output, 'Hi, arthur!')

    def test_datetimeformat_filter(self):
        """
        Test that the datetimeformat filter is available in the template.
        """
        date = datetime(2009, 01, 01)
        template_str = '{{ date|datetimeformat("%Y") }}'
        output = self.template.render_string(template_str,
                                             date=date)
        self.assertEqual(output, '2009')

if __name__ == '__main__':
    unittest.main()

