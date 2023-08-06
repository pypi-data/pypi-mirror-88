try:
    from etlx.build import __version__
except ImportError:  # pragma: no cover
    __version__ = '0.0.0.dev'
