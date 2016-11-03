# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *


def get_descendants(net, var) :
    "Return a set containing the descendants of var"
    raise NotImplementedError

def get_nondescendants(net, var):
    "Return a set containing the non-descendants of var"
    raise NotImplementedError

def remove_nondescendants_given_parents(net, var, givens):
    """If all parents are given, removes any non-descendants of var (except
    parents) from the list of givens. Otherwise, returns False. Does not modify
    original givens."""
    raise NotImplementedError


def probability_lookup(net, hypothesis, givens=None) :
    "Looks up a probability in the Bayes net."
    raise NotImplementedError

def probability_joint(net, hypothesis) :
    "Uses the chain rule to compute a joint probability"
    raise NotImplementedError

def probability_marginal(net, hypothesis) :
    "Computes a marginal probability as a sum of joint probabilities"
    raise NotImplementedError

def probability_conditional(net, hypothesis, givens=None) :
    "Computes a conditional probability as a ratio of marginal probabilities"
    raise NotImplementedError

def probability(net, hypothesis, givens=None) :
    "Calls previous functions to compute any probability"
    raise NotImplementedError


def number_of_parameters(net) :
    "Computes minimum number of parameters required for net"
    raise NotImplementedError


def is_independent(net, var1, var2, givens=None) :
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence only (not structural
    independence)."""
    raise NotImplementedError
