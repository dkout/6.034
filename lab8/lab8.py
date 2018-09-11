# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *
import itertools


#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    parents = net.get_parents(var)
    queue=parents
    while queue:
    	nextvar=queue.pop()
    	parents.add(nextvar)
    	queue=queue|get_ancestors(net,nextvar)

    return parents

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    children = net.get_children(var)
    queue=children
    while queue:
    	nextvar=queue.pop()
    	children.add(nextvar)
    	queue=queue|get_descendants(net,nextvar)

    return children

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    # print set(net.get_variables())-set(var)
    # print get_descendants(net,var)
    # print var
    return (set(net.get_variables())-set(var))-get_descendants(net, var)

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""

    if net.get_parents(var).issubset(givens):
        for i in get_descendants(net, var):
            if i in givens:
                return givens
        ans = {}
        for parent in net.get_parents(var):
            ans[parent] = givens[parent]
        return ans
    return givens  


#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    #print (hypothesis)
    try:
    	if givens is None:
    		ans = net.get_probability(hypothesis)
    	else: 
    		ans = net.get_probability(hypothesis,simplify_givens(net, (hypothesis.keys())[0], givens))
    	return ans
    except:
    	raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    p=1
    vars=net.topological_sort()[::-1]
    n=len(vars)
    for x in range (n):
    	hyp={vars[x]:hypothesis[vars[x]]}
    	givens=dict()
    	for y in xrange(x+1, n):
    		cond=vars[y]
    		givens[cond]=hypothesis[cond]
    	p = p*probability_lookup(net,hyp, givens)
    return p

def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    ans=0
    for p in net.combinations(net.get_variables(),hypothesis):
    	ans= ans + probability_joint(net, p)
    return ans

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    #print hypothesis
    #print givens
    if hypothesis==givens:
		return 1
    if givens is not None:
    	for i in hypothesis:
    		if i in givens and hypothesis[i] != givens[i]:
    			return 0
    try:
    	return probability_lookup(net, hypothesis, givens)
    except LookupError:
    	if givens==None:
    		return probability_marginal(net,hypothesis)
    	return float(probability_marginal(net, dict(hypothesis, **givens)))/probability_marginal(net, givens)

def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net, hypothesis, givens)


#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    vars=net.topological_sort()[::-1]
   # print vars
    #print net

    combs=net.combinations(net.get_variables())[0]

   # print combs
    ans=0

    for x in xrange(0, len(vars)):
    	givens=dict()
    	for y in range(x+1, len(vars)):
    		givens[vars[y]]=combs[vars[y]]

    	l=[]
    	for given in simplify_givens(net, vars[x], givens):
    		l.append(len(net.get_domain(given)))
    	p=product(l)
    	ans = ans+(len(net.get_domain(vars[x]))-1)*p
    return ans

def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""
    for d1 in net.get_domain(var1):
        for d2 in net.get_domain(var2):
            prob1 = probability(net, {var1: d1}, givens)
            prob2 = probability(net, {var2: d2}, givens)
            joint = probability(net, {var1: d1, var2: d2}, givens)
            if not approx_equal(prob1*prob2,joint):
                return False
    return True


def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""
    vars = set([var1,var2])
    #print net
    #print vars
    #print given
    if var1 == var2:
        return False
    vars.update(get_ancestors(net,var1))
    vars.update(get_ancestors(net,var2))
    if givens is not None:
        for x in givens:
            vars.add(x)
            vars.update(get_ancestors(net,x))
    subnet = net.subnet(list(vars))

    #print subnet

    c = []
    for var in subnet.get_variables():
        parents = subnet.get_parents(var)
        c.extend(itertools.combinations(parents, 2))
    for x in c:
        subnet.link(x[0],x[1])
    subnet = subnet.make_bidirectional()

    if givens is not None:
        for x in givens:
            subnet.remove_variable(x)
    return subnet.find_path(var1, var2) == None



#### SURVEY ####################################################################

NAME = "Dimitris Koutentakis"
COLLABORATORS = "Luana Lopes"
HOW_MANY_HOURS_THIS_LAB_TOOK = 10
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
