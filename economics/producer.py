#!/usr/bin/env python

import sympy as sp
import tools


class Firm(object):
    """Given a production function q=F(k, l) we can compute the
    minimum cost given q as a function of the cost of k and l, r and
    w.  The solution of the maximization problem is then when the
    marginal cost (the derivative of the minimum cost function of q)
    equals the price, as long as it is above the average minimum cost.
    If it is below, there will be losses and the firm will shut
    down.
    """
    def __init__(self, q, p, variable_cost, SFC=None, FC=None):
        self.q = q
        self.p = p
        self._var_cost = variable_cost
        if SFC is None:
            SFC = sp.Symbol('SFC')
        self._SFC = SFC
        if FC is None:
            FC = sp.Symbol('FC')
        self._FC = FC

    def total_cost(self):
        return self._var_cost + self._SFC + self._FC

    def marginal_cost(self):
        return sp.solve(sp.diff(self.total_cost(), self.q) - self.p,
                        self.p)[-1]

    def avg_total_cost_sfc(self):
        return (self.total_cost() - self._FC) / self.q

    def min_atc_sfc(self):
        min_atc, cond = tools.minimize(self.avg_total_cost_sfc(),
                                       over=self.q)
        if min_atc is not None:
            return min_atc, cond
        return 0, True

    def earnings(self):
        return self.p * self.q - self.total_cost()

    def earnings_at(self, q):
        return self.earnings().subs(self.q, q)

    def supply(self):
        """
        >>> sp.var('p q', positive=True)
        (p, q)
        >>> f = Firm(q, p, q**2/1000., SFC=1000)
        >>> f.supply()
        Piecewise((0, p < 1000.0), (500.0*p, And(0 <= p, p >= 1000.0)))
        """
        min_atc, min_atc_cond = self.min_atc_sfc()
        supply, supply_cond = tools.maximize(self.earnings(), over=self.q)
        if supply is None:
            return 0
        return sp.Piecewise((0, sp.Lt(self.p, min_atc)),
                            (supply, sp.And(sp.Ge(self.p, min_atc),
                                            supply_cond,
                                            min_atc_cond)))

    def supply_at(self, p):
        return self.supply().subs(self.p, p)

    def surplus(self):
        supply = self.supply()
        return self.earnings_at(supply) - self.earnings_at(0)

    def surplus_at(self, p):
        """
        >>> sp.var('p q')
        (p, q)
        >>> f = Firm(q, p, q**2/10., SFC=0, FC=0)
        >>> '%.2f' % f.surplus_at(10)
        '250.00'
        """
        return self.surplus().subs(self.p, p)

    def total_cost_at_p(self):
        return self.total_cost().subs(self.q, self.supply())


class ProducerAggregate(object):
    def __init__(self, *firms):
        self._firms = firms

    def firms(self):
        return tools.aggregate_iterator(self._firms)

    def supply(self):
        aggregate = sp.Piecewise((0, True))
        for firm, n in self.firms():
            aggregate = sp.piecewise_fold(aggregate + n*firm.supply())
        return aggregate

    def surplus_at(self, p_var, p_at, rational=True):
        """
        >>> sp.var('p q', positive=True)
        (p, q)
        >>> f1 = Firm(q, p, variable_cost=q**2, SFC=0, FC=0)
        >>> f2 = Firm(q, p, variable_cost=2 * q**2, SFC=0, FC=0)
        >>> f3 = Firm(q, p, variable_cost=4 * q**2, SFC=0, FC=0)
        >>> agg = ProducerAggregate((f1, 20), (f2, 40), (f3, 80))
        >>> agg.surplus_at(p, 10)
        1500
        """
        return sp.integrate(self.supply(), (p_var, 0, p_at))


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
