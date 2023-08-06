import logging
from pysuperconductor.meta import __version__


def get_version():
	return __version__


logging.getLogger(__name__).addHandler(logging.NullHandler())
