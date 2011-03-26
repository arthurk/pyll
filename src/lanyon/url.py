from fnmatch import fnmatch
from os.path import splitext, split, relpath

from lanyon.utils import OrderedDict
registry = OrderedDict()

def get_url(page):
    "Returns the final output url string for `page`"
    urlfunc = get_url_func(page)
    return urlfunc(page)

def get_url_func(page):
    """
    Returns the entry from the url registry that matches the specified
    url header value.
    """
    path = page['path']
    url = page['url']
    for pattern in reversed(registry):
        rules = registry[pattern]
        if fnmatch(path, pattern):
            if url in rules:
                return rules[url]
            elif pattern == '*' and url != 'default':
                # special case: user entered something but it isn't
                # a url function -> assume its an output path 
                return lambda **x: url
            elif 'default' in rules:
                return rules['default']

def register(func=None, match='*'):
    "A registry for url rules"
    def decorated(func):
        # this returns the final, decorated function,
        # regardless of how it was called
        match_rules = registry.setdefault(match, {})
        match_rules[func.__name__] = func
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    if func is None:
        # the decorator was called with arguments
        def decorator(func):
            return decorated(func)
        return decorator
    # the decorator was called without arguments
    return decorated(func)

@register
def default(page):
    "default url rule"
    path = page['path']
    ext = page['output_ext']
    url = splitext(path)[0] + '.' + ext
    head, tail = split(url)
    if tail == 'index.html':
        # don't link to "index.html" files
        url = head + '/'
    return url

@register
def pretty(page):
    return '$year/$month/$day/$slug/'
