from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader
from jinja2 import TemplateNotFound

class TemplateException(Exception):
    pass

class Jinja2Template(object):
    default_template = 'default.html'

    def __init__(self, settings):
        self.settings = settings
        self.env = Environment(loader=ChoiceLoader([
            FileSystemLoader(self.settings['template_dir']),
            PackageLoader('lanyon')]))
        self.env.filters['datetimeformat'] = self.datetimeformat
        self.env.filters['ordinalsuffix'] = self.ordinal_suffix

    def ordinal_suffix(self, day):
        """
        Return the day with the ordinal suffix appended.

        Example: 1st, 2nd, 3rd, 4th, ...
        """
        day = int(day)
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        return "%s%s" % (day, suffix)

    def datetimeformat(self, value, format='%H:%M / %d-%m-%Y'):
        """
        Return a formatted time string.

        Keyword arguments:
        value -- tuple or struct_time representing a time
        format -- the desired format
        """
        return value.strftime(format)

    def render_string(self, template_str, **kwargs):
        """Use `template_str` as a template"""
        template = self.env.from_string(template_str)
        try:
            return template.render(**kwargs)
        except TemplateNotFound as err:
            raise TemplateException("Template '%s' not found" % err)

    def render(self, template_name, **kwargs):
        """Use `template_name` as a template"""
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateException
        try:
            return template.render(**kwargs)
        except TemplateNotFound as err:
            raise TemplateException("Template '%s' not found" % err)
