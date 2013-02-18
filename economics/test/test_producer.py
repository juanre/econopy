import sympy as sp
import unittest

from economics.producer import Firm, ProducerAggregate
import economics.tools as et


class ProducerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_surplus(self):
        """Practice problem 3.4
        """
        sp.var('q p')
        firm = Firm(q, p, q**2/10., SFC=0, FC=0)
        self.assertEqual(firm.surplus_at(p=10), 250)

    def test_subsidy(self):
        """Problem 3.3
        """
        sp.var('q p', positive=True)
        firm = Firm(q, p, q**2/1000., SFC=0, FC=0)
        self.assertEqual(sp.solve(firm.supply() - 1000, p)[0], 2)

if __name__ == '__main__':
    unittest.main()
