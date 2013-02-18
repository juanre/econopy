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

        mkt = Market(q, p, demand=1000-p, supply=sp.Eq(p, 100))
        self.assertEqual(mkt.equilibrium(), (100, 900))
        self.assertEqual(mkt.free_market_social_surplus(), 405000)

        mkt = Market(q, p, demand=1000-p, supply=sp.Eq(p, 250))
        self.assertEqual(mkt.free_market_social_surplus(), 281250)


if __name__ == '__main__':
    unittest.main()
