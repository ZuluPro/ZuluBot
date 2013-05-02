from wiki_handler import *


def suite():
    import unittest
    TEST_CASES = (
        'core.tests.wiki_handler',
    )
    suite = unittest.TestSuite()

    for t in TEST_CASES:
        suite.addTest(unittest.TestLoader().loadTestsFromModule(__import__(t, globals(), locals(), fromlist=["*"])))
    return suite
