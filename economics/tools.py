#!/usr/bin/env python

import sympy as sp

def extreme(fn, over, maximizing):
    """Maximizes [minimizes] the function fn for 'over'.  Returns the
    first extreme expression and a list of conditions for it to be a
    maximum [minimum].

    >>> sp.var('x p', positive=True)
    (x, p)
    >>> theta = sp.Symbol('theta', positive=True)
    >>> fn = p*x - theta*x*x
    >>> maximize(fn, x)
    (p/(2*theta), 0 < theta)
    >>> maximize(fn.subs(theta, 1), x)
    (p/2, 0 <= p)
    >>> maximize(fn.subs(theta, -1), x)
    (None, False)
    """
    first = sp.diff(fn, over)
    extremes_at = sp.solve(first, over)
    second = sp.diff(first, over)
    for m in extremes_at:
        positive = False
        try:
            ## We only want values of over that are positive.
            positive = sp.solve(sp.Ge(m, 0))
        except:
            ## Inequality solve only works with a single variable.
            ## Assume it is true.  We are missing a condition.
            positive = True

        ## Checking for inequality to False because an inequality will
        ## evaluate as False even if present in positive
        if positive is not False:
            conditions = []
            if positive is not True:
                conditions.append(positive)
            try:
                if maximizing:
                    max_min_cond = sp.solve(sp.Lt(second.subs(over, m), 0))
                else:
                    max_min_cond = sp.solve(sp.Gt(second.subs(over, m), 0))
            except:
                ## Not always works.  Assume it is true.  We are
                ## missing a condition.
                max_min_cond = True
            if max_min_cond:
                if max_min_cond is not True:
                    conditions.append(max_min_cond)
                return m, reduce(sp.And, [True] + conditions)
    return None, False

def maximize(fn, over):
    return extreme(fn, over, maximizing=True)

def minimize(fn, over):
    return extreme(fn, over, maximizing=False)

def implicit(variable, expression):
    """In most cases we want an implicit relationship.  For example,
    when we define demand we say 100-p, and the q= is implicit.  But
    in some cases we want to make the relationship explicit, like for
    example when supply is just a fixed p.
    """
    if isinstance(expression, sp.relational.Relational):
        return expression
    return sp.Eq(expression, variable)

def benefit_from_marginal(x, p, bp):
    """Converts the derivative of the benefit to the benefit.  It
    assumes the derivative to be a p=b'(x) function, where the p= is
    implicit.

    >>> sp.var('x p')
    (x, p)
    >>> sp.simplify(benefit_from_marginal(x, p, 10/(x+1)) - 10*sp.log(x+1))
    0
    >>> sp.simplify(benefit_from_marginal(x, p, sp.Eq(p, 10/(x+1))) - 10*sp.log(x+1))
    0
    """
    return sp.integrate(sp.solve(implicit(p, bp), p)[0], (x, 0, x))

def benefit_from_demand(x, p, demand):
    """Converts the demand curve to the benefit.  It assumes that the
    demand is a x=d(p) function, where the x= is implicit.

    >>> sp.var('x p')
    (x, p)
    >>> sp.simplify(benefit_from_demand(x, p, 10/p -1) -
    ...             10*sp.log(x+1))
    0
    >>> sp.simplify(benefit_from_demand(x, p, sp.Eq(x, 10/p -1)) -
    ...             10*sp.log(x+1))
    0
    >>> sp.simplify(benefit_from_demand(x, p, 100-p) -
    ...             (-x**2/2 + 100*x))
    0
    >>> benefit_from_demand(x, p, sp.Piecewise((0, p < 0),
    ...                                        (-p + 100, p <= 100),
    ...                                        (0, True)))
    -x**2/2 + 100*x
    """
    if isinstance(demand, sp.relational.Relational):
        return sp.integrate(sp.solve(demand, p)[0], (x, 0, x))
    substracting = sp.solve(demand-x, p)
    if substracting:
        toint = substracting[0]
    else:
        substracting = sp.solve(demand, p)
        if substracting:
            toint = substracting[0] - x
        else:
            return None

    return sp.integrate(toint, (x, 0, x))
    #return sp.integrate(sp.solve(implicit(x, demand), p)[0], (x, 0, x))

def min_cost_from_production(q, k, l, r, w, F):
    """Given the production function F find the expression of the
    minimum cost as a function of q.

    >>> sp.var('q k l r w A', positive=True)
    (q, k, l, r, w, A)
    >>> min_cost_from_production(q, k, l, r, w, A*sp.sqrt(l))
    k_min*r + q**2*w/A**2
    """
    tangent = sp.diff(F, k)/sp.diff(F, l) - r/w
    kl_min = sp.solve([tangent, F-q], [k, l], dict=True)[0]
    k_min, l_min = sp.symbols('k_min, l_min')
    if k in kl_min:
        k_min = kl_min[k]
    if l in kl_min:
        l_min = kl_min[l]
    return r*k_min + w*l_min

def cost_from_supply(q, p, supply):
    """Converts the supply curve to cost.  It assumes that the
    supply is a q=d(p) function, where the x= is implicit.

    >>> sp.var('q p a', positive=True)
    (q, p, a)
    >>> sp.simplify(cost_from_supply(q, p, 10*a*p) - q**2/(20*a))
    0
    >>> sp.simplify(cost_from_supply(q, p, sp.Eq(q, 10*a*p)) - q**2/(20*a))
    0
    """
    return sp.integrate(sp.solve(implicit(q, supply), p)[0], (q, 0, q))

def cost_from_marginal(q, p, bp):
    """Converts the derivative of the cost to the cost.  It
    assumes the derivative to be a p=c'(x) function, where the p= is
    implicit.

    >>> sp.var('q p')
    (q, p)
    >>> cost_from_marginal(q, p, 2*q)
    q**2
    >>> cost_from_marginal(q, p, sp.Eq(p, 100))
    100*q
    """
    return sp.integrate(sp.solve(implicit(p, bp), p)[0], (q, 0, q))

def aggregate_iterator(over):
    """Aggregates are lists that might contain tuples (obj, n), or
    just obj, in which case we assume n to be 1.
    """
    for obj in over:
        n = 1
        if isinstance(obj, tuple):
            obj, n = obj
        yield obj, n


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
