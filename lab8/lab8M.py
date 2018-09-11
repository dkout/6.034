# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *
import itertools


#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    queue = [var]
    anc = set()
    seen = set()
    while len(queue) > 0:
        v = queue.pop()
        for par in net.get_parents(v):
            if par not in seen:
                seen.add(par)
                queue.append(par)
                anc.add(par)
    return anc

def get_descendants(net, var):
    queue = [var]
    des = set()
    seen = set()
    while len(queue) > 0:
        v = queue.pop()
        for chi in net.get_children(v):
            if chi not in seen:
                seen.add(chi)
                queue.append(chi)
                des.add(chi)
    return des

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    all = set(net.get_variables())
    return all.difference(get_descendants(net,var)).difference(var)

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""

    if net.get_parents(var).issubset(givens):
        for descendant in get_descendants(net, var):
            if descendant in givens:
                return givens
        new = {}
        for item in net.get_parents(var):
            new[item] = givens[item]
        return new
    return givens



#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    try:
        if givens == None:
            return net.get_probability(hypothesis)
        else:
            return net.get_probability(hypothesis, simplify_givens(net, hypothesis.keys()[0], givens))
    except:
        raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    prob = 1
    variables = net.topological_sort()[::-1]
    numvars = len(variables)
    for i in range(numvars):
        tempHypothesis = {variables[i]: hypothesis[variables[i]]}
        givens = {}
        for j in range(i+1,numvars):
            condition = variables[j]
            givens[condition] = hypothesis[condition]
        prob *= probability_lookup(net, tempHypothesis, givens)
    return prob

def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    combos = net.combinations(net.get_variables(), hypothesis)
    res = 0
    for joint in combos:
        res += probability_joint(net, joint)
    return res

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    if hypothesis == givens:
        return 1
    if givens != None:
        for var in hypothesis:
            if var in givens and hypothesis[var] != givens[var]:
                return 0
    try:
        return probability_lookup(net, hypothesis, givens)
    except LookupError:
        if givens == None:
            return probability_marginal(net,hypothesis)
        return 1.0*probability_marginal(net,dict(hypothesis,**givens))/probability_marginal(net,givens)

def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net, hypothesis, givens)


#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    variables = net.topological_sort()[::-1]
    numvars = len(variables)
    combos = net.combinations(net.get_variables())[0]
    res = 0
    for i in range(0,numvars):
        givens = {}
        for j in range(i+1,numvars):
            condition = variables[j]
            givens[condition] = combos[condition]
        res += (len(net.get_domain(variables[i]))-1)*product([len(net.get_domain(given)) for given in simplify_givens(net, variables[i], givens)])
    return res


def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""
    for domain1 in net.get_domain(var1):
        for domain2 in net.get_domain(var2):
            prob1 = probability(net, {var1: domain1}, givens)
            prob2 = probability(net, {var2: domain2}, givens)
            joint = probability(net, {var1: domain1, var2: domain2}, givens)
            if not approx_equal(prob1*prob2,joint):
                return False
    return True

def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""
    variables = set([var1,var2])
    if var1 == var2:
        return False
    variables.update(get_ancestors(net,var1))
    variables.update(get_ancestors(net,var2))
    if givens != None:
        for given in givens:
            variables.add(given)
            variables.update(get_ancestors(net,given))
    sub = net.subnet(list(variables))
    combinations = []
    for var in sub.get_variables():
        parents = sub.get_parents(var)
        combinations.extend(itertools.combinations(parents, 2))
    for combo in combinations:
        sub.link(combo[0],combo[1])
    subnet = sub.make_bidirectional()
    if givens != None:
        for given in givens:
            subnet.remove_variable(given)
    return subnet.find_path(var1, var2) == None


#### SURVEY ####################################################################

NAME = "Meia Alsup"
COLLABORATORS = "Grace Yin, Jennifer McCleary, Katherine Wang"
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
