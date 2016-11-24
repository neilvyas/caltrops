from builtins import str as text
from collections import namedtuple


Error = namedtuple('Error', ('type', 'message'))


def exception_wrapper(f):
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Can also log the args.
            return Error(type(e).__name__, text(e))
    return wrapped
