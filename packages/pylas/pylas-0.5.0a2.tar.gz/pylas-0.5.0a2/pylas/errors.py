""" All the custom exceptions types
"""


class PylasError(Exception):
    pass


class UnknownExtraType(PylasError):
    pass


class PointFormatNotSupported(PylasError):
    pass


class FileVersionNotSupported(PylasError):
    pass


class LazError(PylasError):
    pass


class IncompatibleDataFormat(PylasError):
    pass


def private(path="pylas"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            import inspect
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])

            if not mod.__name__.startswith(path):
                raise RuntimeError(f"'{func.__name__}' function is private to '{path}'")
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def private_meth(path="pylas"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            import inspect
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])

            print("name:", func.__name__, " qualname ", func.__qualname__)

            if not mod.__name__.startswith(path):
                raise RuntimeError(f"'{func.__name__}' function is private to '{path}'")
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def private_module(func):
    return private(__name__)(func)


@private("pylas.errors")
def lol(a):
    return a


@private_module
def mdr(a):
    return a + 1


class Mdr:
    @private_meth
    def a(self):
        return 1
