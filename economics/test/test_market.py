import sympy as sp
import unittest

from economics.producer import Firm, ProducerAggregate
from economics.consumer import Consumer, ConsumerAggregate
from economics.market import Market
import economics.tools as et


class MarketTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fixed_marginal(self):
        """Problem 5.4
        """
        sp.var('q p', positive=True)

        print sp.solve((sp.Eq(q, 1000-p), (sp.Eq(p, 100))), p, q, dict=True)[0][p]

        print sp.integrate(sp.Eq(p, 100), (q, 0, q))

        print sp.integrate(sp.Eq(q, 100*p), (q, 0, q))

        ###

        print

        print sp.solve((1000-p-q, p - 100), p, q, dict=True)[0][p]

        print sp.integrate(sp.solve(p - 100, p)[0], (q, 0, q))

        print sp.integrate(sp.solve(q - 100*p, p)[0], (q, 0, q))

        #mkt = Market(q, p, demand=1000-p, supply=)

        ##benefit = et.benefit_from_demand(q, p, 1000-p)
        ##cons = Consumer(q, p, benefit=benefit)
        ##
        ##consumers = ConsumerAggregate((cons, 1))
        ##
        ###firm1 = Firm(q, p, cost_from_marginal(q, p, 400),
        ###                  SFC=0, FC=0)
        ##cost_100 = et.cost_from_marginal(q, p, 100)
        ##firm2 = Firm(q, p, cost_100,
        ##                  SFC=0, FC=0)
        ##producers = ProducerAggregate((firm2, 10)) #, (firm2, 10))
        ##
        ##print firm2.total_cost()
        ##print producers.total_cost(q)
        ##print sp.integrate(100, (q, 0, q))
        ###print consumers.total_benefit()
        ###print consumers.total_benefit_at_p()
        ###print producers.total_cost_at_p()


if __name__ == '__main__':
    unittest.main()
