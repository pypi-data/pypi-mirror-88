"""PyGreSQL test suite.

You can specify your local database settings in LOCAL_PyGreSQL.py.
"""

import unittest

if not (hasattr(unittest, 'skip')
        and hasattr(unittest.TestCase, 'setUpClass')
        and hasattr(unittest.TestCase, 'skipTest')
        and hasattr(unittest.TestCase, 'assertIn')):
    raise ImportError('Please install a newer version of unittest')


def discover():
    loader = unittest.TestLoader()
    suite = loader.discover('.')
    return suite
