from os.path import splitext, split
from lanyon.utils import OrderedDict

registry = OrderedDict()
def register(func=None, match='*'):
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
def default(**kwargs):
    path = kwargs['path']
    ext = kwargs['extension']
    url = splitext(path)[0] + '.' + ext
    head, tail = split(url)
    if tail == 'index.html':
        # don't link to "index.html" files
        url = head + '/'
    return url

@register
def pretty(**kwargs):
    return '$year/$month/$day/$slug/'
