import BaseHTTPServer
from codecs import open
from collections import defaultdict, namedtuple
from datetime import datetime
import imp
import logging
from optparse import OptionParser
from os import makedirs, getcwd
from os.path import splitext, join, dirname, split, abspath, getctime, isdir,\
                    basename, exists, relpath, isabs
from shutil import rmtree
from string import Template
import sys
import time

from lanyon import __version__, parser
from lanyon.url import get_url
from lanyon.utils import copy_file, walk_ignore, OrderedDict
from lanyon.template import Jinja2Template, TemplateException
from lanyon.server import LanyonHTTPRequestHandler

LOGGING_LEVELS = {'info': logging.INFO, 'debug': logging.DEBUG}

class Site(object):

    def __init__(self, settings):
        self.settings = settings
        self.pages = []
        self.static_files = []

    def _copy_media(self):
        # media that isn't associated with articles
        for medium in self.media:
            dst = join(self.settings['output_dir'],
                       relpath(medium, self.settings['input_dir']))
            copy_file(medium, dst)
        # media that is associated with articles
        for article in self.articles:
            for medium in article.media:
                dst = join(self.settings['output_dir'],
                           dirname(article.output_path),
                           relpath(medium, dirname(article.input_path)))
                copy_file(medium, dst)

    def _is_public(self, article):
        """Return True if article is public"""
        if article.headers['status'] != 'hidden':
            return True
        return False

    def _sort_articles(self):
        """Sort articles by date (newest first)"""
        self.articles.sort(key=lambda x: x.headers['date'], reverse=True)

    def _delete_output_dir(self):
        """Delete the output directory"""
        if exists(self.settings['output_dir']):
            rmtree(self.settings['output_dir'])

    def _write(self):
        public_articles = filter(self._is_public, self.articles)
        template_cls = Jinja2Template(self.settings)
        for article in self.articles:
            try:
                makedirs(dirname(article.output_path))
            except OSError:
                pass
            if article.headers['template'] == 'self':
                render_func = template_cls.render_string
                template = article.body
            else:
                render_func = template_cls.render
                template = article.headers['template']
            try:
                rendered = render_func(template,
                                       body=article.body,
                                       headers=article.headers,
                                       articles=public_articles,
                                       settings=self.settings)
            except TemplateException as error:
                logging.error(error)
                logging.error('skipping article "%s"', article.input_path)
                continue
            logging.debug("writing %s to %s", article.input_path,
                                              article.output_path)
            fout = open(article.output_path, 'w', 'utf-8')
            fout.write(rendered)
            fout.close()

    def _read_files(self):
        """
        Walks through the project directory and separates files into article
        and static files.
        - into parseable files (file extensions for which a parser exists)
        and static files (file extensions for which no parser exists)
        """
        data = OrderedDict()
        for root, dirs, files in walk_ignore(self.settings['project_dir']):
            pages = [] # parseable files; rename to (pages)
            static = [] # rename to (static)

            # check if a parser exists and append to corresponding list
            for file in files:
                path = join(root, file)
                if parser.get_parser_for_filename(path):
                    pages.append(path)
                else:
                    static.append(path)

            # assign static files with pages
            if pages:
                data[root] = (pages, static)
            elif static:
                # dir has static file(s) but no pages. check if one of
                # the parent dirs has a page and associate the static files
                # with it
                has_parent = False
                if root != self.settings['project_dir']:
                    parent_dir = dirname(root)
                    while parent_dir != self.settings['project_dir']:
                        if parent_dir in data:
                            data.setdefault(parent_dir, ([], []))[1].\
                                    extend(static)
                            has_parent = True
                        parent_dir = dirname(parent_dir)
                # if no parent dir could be found, or the file is in the
                # root dir associate the files with the root of the project dir
                if not has_parent:
                    data.setdefault(self.settings['project_dir'],
                                    ([], []))[1].extend(static)
        return data

    def _get_default_headers(self, path):
        """
        Returns a dict with the default headers for `path`.

        `path` - the relative path from the project dir to the file
        `title` - titleized version of the filename
        `date` - set to ctime. On unix this is the time of the most recent
                 metadata change; on windows the creation time. If ctime
                 cannot be accessed (due to permissions), the current 
                 time is used.
        `status` - set to 'live'
        `template` - set to 'default.html'
        `url` - set to "default" rule
        `slug` - filename or, if the filename is "index", the dirname
               of the parent directory unless its the top level dir.
        `output_ext` - the extension of the parsed file
        """
        output_ext = splitext(path)[1][1:]
        root, filename = split(splitext(path)[0])
        if filename == 'index' and root != self.settings['project_dir']:
            slug = basename(root)
        else:
            slug = filename
        title = filename.title()
        try:
            date = datetime.fromtimestamp(getctime(path))
        except OSError:
            # use the current date if the ctime cannot be accessed
            date = datetime.now()
        return dict(path=relpath(path, self.settings['project_dir']),
                    title=title, date=date, status='live',
                    slug=slug, template='default.html', url='default',
                    output_ext=output_ext)

    def _get_output_path(self, url):
        """
        Returns the absolute output path for a page.

        Keyword arguments:
            url -- the parsed "url" header
        """
        if isabs(url):
            # omit starting slash char; if we wouldn't do this, the
            # join() below would return a path that starts from 
            # the root of the filesystem instead of the output_dir.
            url = url[1:]
        if not basename(url):
            # url is a directory -> write to 'index.html'
            output_path = join(url, 'index.html')
        else:
            # url is a filename
            output_path = url
        return join(self.settings['output_dir'], output_path)

    def _parse(self, input_data):
        "Parses the input data"
        for input_dir in input_data:
            pages, static_files = input_data[input_dir]

            # special case: static files at the top level of the project dir 
            # are not associated with any pages
            if input_dir == self.settings['project_dir']:
                self.static_files = static_files
                static = []

            for path in pages:
                page = dict(static_files=static_files,)
                page.update(self._get_default_headers(path))

                # parse the page
                parser_cls = parser.get_parser_for_filename(page['path'])
                with open(path, 'r', encoding='utf8') as f:
                    parser_inst = parser_cls(self.settings, f.read())

                try:
                    parsed = parser_inst.parse()
                except parser.ParserException as parser_error:
                    logging.error(parser_error)
                    logging.error('skipping article "%s"', path)
                    continue

                # update the values in the page dict
                page.update(output_ext=parser_cls.output_ext,
                            body=parsed[1],
                            **parsed[0])

                # skip drafts
                if page['status'] == 'draft':
                    logging.debug('skipping %s (draft)', path)
                    continue
                # skip pages with a date that is in the future
                elif page['date'] > datetime.today():
                    logging.debug('skipping %s (future-dated)', path)
                    continue
                
                # resolve url pattern
                page['url'] = get_url(page)

                # substitute variables in url pattern
                substitute_vars = dict(
                    year=page['date'].year,
                    month=page['date'].strftime('%m'),
                    day=page['date'].strftime('%d'),
                    slug=page['slug'],
                    ext=page['output_ext'],
                )
                tmpl = Template(page['url'])
                page['url'] = tmpl.safe_substitute(substitute_vars)

                # get the output path for the page
                #output_path = self._get_output_path(headers['url'])

                self.pages.append(page)
                sys.stdout.write('.')
        sys.stdout.write('\n')

    def run(self):
        start_time = time.time()
        logging.debug("reading input files")
        input_data = self._read_files()
        logging.debug("input data %s", input_data)
        logging.debug("parsing files")
        self._parse(input_data)
        """
        self._sort_articles()
        logging.debug("writing files")
        self._delete_output_dir()
        self._write()
        self._copy_media()
        logging.debug("%s articles written", len(self.articles))
        finish_time = time.time()
        article_count = len(self.articles)
        print("OK (%s %s; %s seconds)" % (
            article_count,
            'article' if article_count == 1 else 'articles',
            round(finish_time - start_time, 2)))
        """

def main():
    parser = OptionParser(version="%prog " + __version__)
    parser.add_option('-l', '--logging-level',
                      help="sets the logging level. 'info' (default) or 'debug'")
    (options, args) = parser.parse_args()

    project_dir = abspath(getcwd())
    settings = {'project_dir': project_dir,
                'output_dir': join(project_dir, '_output'),
                'template_dir': join(project_dir, '_templates'),
                'lib_dir': join(project_dir, '_lib'),
                'url_path': join(project_dir, '_lib', 'urls.py'),
                'build_time': datetime.today(),
                'date_format': '%Y-%m-%d'}

    # configure logging
    logging_level = LOGGING_LEVELS.get(options.logging_level, logging.INFO)
    logging.basicConfig(level=logging_level,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug('default settings %s', settings)

    # import custom urls
    try:
        urls = imp.load_source('urls', settings['url_path'])
    except IOError as e:
        logging.debug('couldn\'t load urls from "%s": %s',
                      settings['url_path'], e)

    # initialize site
    site = Site(settings)
    site.run()

if __name__ == '__main__':
    main()
