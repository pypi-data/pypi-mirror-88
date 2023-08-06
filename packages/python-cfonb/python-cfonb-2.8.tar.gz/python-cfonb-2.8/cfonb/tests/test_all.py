import doctest
import unittest
from os.path import join, pardir

from cfonb.parser import common
# cfonb tests import
from cfonb.tests import test_statement
from cfonb.tests import test_transfert
# cfonb import
from cfonb.writer import transfert


def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_statement.suite())
    suite.addTest(test_transfert.suite())
    # doctests
    suite.addTest(doctest.DocTestSuite(common,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    suite.addTest(doctest.DocTestSuite(transfert,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    suite.addTest(doctest.DocFileSuite(join(pardir, pardir, 'README.rst'),
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    return suite
