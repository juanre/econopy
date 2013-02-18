#!/usr/bin/env python

import tools
import sympy as sp

class Consumer(object):
    def __init__(self, x, p, benefit, decision_benefit=None,
                 W=None, other=None):
        """A consumer utility has a benefit from acquiring x, plus
        another that will, by default, be W-p*x.

        >>> sp.var('x p')
        (x, p)
        >>> cu = Consumer(x, p, benefit=tools.benefit_from_demand(x, p, 9/p - 1))
        >>> sp.simplify(cu.benefit() - 9*sp.log(x + 1))
        0
        """
        self.x = x
        self.p = p
        if W is None:
            W = sp.Symbol('W')
        self.W = W
        self._benefit = benefit
        if decision_benefit is None:
            decision_benefit = benefit
        self._decision_benefit = decision_benefit
        if other is None:
            other = W - p*x
        self._other = other

    def utility(self, rational=True):
        if rational:
            return self.benefit() + self._other
        return self.decision_benefit() + self._other

    def benefit(self):
        return self._benefit

    def decision_benefit(self):
        return self._decision_benefit

    def utility_at(self, x, rational=True):
        return self.utility(rational).subs(self.x, x)

    def demand(self, rational=True):
        """Compute the demand as the maximization of the utility function.

        >>> sp.var('x p')
        (x, p)
        >>> cu = Consumer(x, p, benefit=tools.benefit_from_demand(x, p, 9/p - 1))
        >>> sp.simplify(cu.benefit() - 9*sp.log(x + 1))
        0
        >>> cu.demand()
        Piecewise((0, p < 0), ((-p + 9)/p, True))
        >>> tau = sp.Symbol('tau')
        >>> cu_rat = Consumer(x, p, benefit=2*sp.sqrt(x))
        >>> cu_del = Consumer(x, p, benefit=2*sp.sqrt(x),
        ...                   decision_benefit=20*sp.sqrt(x),
        ...                   other=-(1+tau)*p*x)
        >>> sp.solve(cu_del.demand(rational=False)-cu_rat.demand(), tau)
        [-11, 9]
        """
        maxima, condition = tools.maximize(self.utility(rational), over=self.x)
        if maxima is None:
            maxima = 0
        return sp.Piecewise((0, sp.Lt(self.p, 0)),
                            (maxima, condition),
                            (0, True))

    def demand_at(self, p, rational=True):
        """Compute the demand as the maximization of the utility function.

        >>> sp.var('x p', positive=True)
        (x, p)
        >>> cu = Consumer(x, p, benefit=tools.benefit_from_demand(x, p, 100-p))
        >>> cu.demand()
        Piecewise((0, p < 0), (-p + 100, p <= 100), (0, True))
        >>> cu.demand_at(p=110)
        0
        >>> cu.demand_at(p=80)
        20
        """
        return self.demand(rational).subs(self.p, p)

    def surplus(self, rational=True):
        """Compute the consumer surplus as the difference between the
        utility at the optimum and the utility of doing nothing.

        >>> sp.var('x p', positive=True)
        (x, p)
        >>> A = sp.Symbol('A')
        >>> cu = Consumer(x, p, benefit=2*A*sp.sqrt(x))
        >>> sp.piecewise_fold(cu.surplus())
        Piecewise((0, p < 0), (-A**2/p + 2*A*sqrt(A**2)/p, True))
        >>> cu = Consumer(x, p, benefit=tools.benefit_from_demand(x, p, 100-p))
        >>> sp.simplify(cu.benefit() - (-x**2/2 + 100*x))
        0
        >>> sp.piecewise_fold(cu.surplus())
        Piecewise((0, p < 0), (-p*(-p + 100) - 100*p - (-p + 100)**2/2 + 10000, p <= 100), (0, True))
        """
        demand = self.demand(rational)
        return (self.utility_at(demand, rational) -
                self.utility_at(0, rational))

    def surplus_at(self, p, rational=True):
        """
        >>> sp.var('x p', positive=True)
        (x, p)
        >>> cu = Consumer(x, p, benefit=tools.benefit_from_demand(x, p, 100-p))
        >>> cu.surplus_at(p=110)
        0
        >>> cu.surplus_at(p=80)
        200
        """
        return self.surplus(rational).subs(self.p, p)

    def benefit_at_p(self, rational=True):
        return self.benefit().subs(self.x, self.demand(rational))


class ConsumerAggregate(object):
    def __init__(self, *consumers):
        self._consumers = consumers

    def consumers(self):
        return tools.aggregate_iterator(self._consumers)

    def demand(self, rational=True):
        aggregate = sp.Piecewise((0, True))
        for consumer, n in self.consumers():
            aggregate = sp.piecewise_fold(aggregate +
                                          n*consumer.demand(rational))
        return aggregate

    def surplus_at(self, p_var, p_at, rational=True):
        """
        >>> sp.var('x p', positive=True)
        (x, p)
        >>> cu1 = Consumer(x, p, benefit=tools.benefit_from_demand(x, p, 100-p))
        >>> cu2 = Consumer(x, p, benefit=tools.benefit_from_demand(x, p, 50-p))
        >>> agg = ConsumerAggregate((cu1, 100), (cu2, 100))
        >>> agg.surplus_at(p, 25)
        312500
        """
        return sp.integrate(self.demand(rational), (p_var, p_at, sp.oo))

    def total_benefit(self):
        out = 0
        for consumer, n in self.consumers():
            out = out + n*consumer.benefit()
        return out

    def total_benefit_at_p(self):
        out = 0
        for consumer, n in self.consumers():
            out = out + n*consumer.benefit_at_p()
        return out


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
