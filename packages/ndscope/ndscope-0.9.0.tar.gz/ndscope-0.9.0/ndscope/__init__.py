__version__ = '?.?.?'
try:
    import setuptools_scm
    __version__ = setuptools_scm.get_version(fallback_version=__version__)
# FIXME: fallback_version is not available in the buster version
# (3.2.0-1)
except TypeError:
    try:
        __version__ = setuptools_scm.get_version()
    except LookupError:
        pass
except ModuleNotFoundError:
    pass
