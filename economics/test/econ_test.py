"""Integrate unittest and docstring.  Main entry for testing.
"""

from test_consumer import ConsumerTest
from test_producer import ProducerTest

import economics.tools
import economics.consumer
import economics.producer
import economics.market

import unittest, doctest

def suite():
    tests = [unittest.TestLoader().loadTestsFromTestCase(ConsumerTest),
             unittest.TestLoader().loadTestsFromTestCase(ProducerTest),
             doctest.DocTestSuite(economics.tools),
             doctest.DocTestSuite(economics.consumer),
             doctest.DocTestSuite(economics.producer),
             doctest.DocTestSuite(economics.market)]
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
