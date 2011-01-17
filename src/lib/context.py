import sys
import os

class ContextError(Exception):
    pass

def platform():
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    return 'linux'


def setup():
    if hasattr(sys, 'frozen'):
        return 'frozen'
    return 'source'


def find_parent(path, base):
    if base == os.path.basename(path):
        return path
    if not path:
        raise ContextError('Could not find "%s" parent path.', base)
    return find_parent(os.path.abspath(os.path.join(path, '..')), base)


def find_source_path(base_source):
    if base_source is None:
        return '?'
    return find_parent(os.path.abspath(os.path.dirname(__file__)), base_source)


CONTEXT = (platform(), setup())

if CONTEXT == ('mac', 'frozen'):
    APP_ROOT = os.path.dirname(os.path.dirname(unicode(sys.executable,
        sys.getfilesystemencoding())))
    DATA = os.path.join(APP_ROOT, 'Resources') # py2app
elif CONTEXT == ('windows', 'frozen'):
    APP_ROOT = os.path.dirname(context['executable'][0])
    DATA = os.path.join(APP_ROOT, 'data') # py2exe
else:
    APP_ROOT = find_source_path('src')
    DATA = os.path.join(APP_ROOT, '..', 'data') # when run from source
