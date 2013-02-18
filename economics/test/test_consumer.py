import sympy as sp
import unittest

from economics.consumer import Consumer, ConsumerAggregate
import economics.tools as et


class ConsumerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_surplus(self):
        """Practice problem 2.2
        """
        sp.var('A x p')
        cons = Consumer(x, p, 2*A * sp.sqrt(x))
        self.assertEqual(sp.piecewise_fold(cons.surplus()),
                         sp.Piecewise((0, p < 0),
                                      (-A**2/p + 2*A*sp.sqrt(A**2/p**2), True)))
        self.assertEqual(sp.piecewise_fold(cons.surplus_at(p*2)),
                         sp.Piecewise((0, 2*p < 0),
                                      (-A**2/(2*p) + A*sp.sqrt(A**2/p**2), True)))

    def test_surplus_tax(self):
        """Practice problem 2.3
        """
        sp.var('x p W')
        benefit = et.benefit_from_demand(x, p, 100 - p)
        sp.plot(benefit, (x, 0, 100))

        cons = Consumer(x, p, benefit)
        cons_sub = Consumer(x, p, benefit, other=W - x*p/2)
        self.assertEqual(cons_sub.surplus().subs(p, 50) - cons.surplus().subs(p, 50),
                         1562.5)




if __name__ == '__main__':
    unittest.main()
