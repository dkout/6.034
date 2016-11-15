# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *


def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    raise NotImplementedError

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    raise NotImplementedError

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    raise NotImplementedError

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, removes any
    non-descendants of var (except parents) from list of givens, then returns
    simplified givens.  Can modify original givens (or not).

    Otherwise, if not all parents are given, or if a descendant is given,
    returns original givens."""
    raise NotImplementedError


def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    raise NotImplementedError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    raise NotImplementedError

def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    raise NotImplementedError

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    raise NotImplementedError

def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    raise NotImplementedError


def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    raise NotImplementedError


def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.
    Uses numerical independence only (not structural independence)."""
    raise NotImplementedError

def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""
    raise NotImplementedError
