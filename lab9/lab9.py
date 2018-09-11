# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
from utils import *


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    weights={}
    N=len(training_points)
    w=1.0/N
    #print w
    for i in range(N):
    	weights[training_points[i]]=make_fraction(w)
    return weights


def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    errorRates=dict()
    # print classifier_to_misclassified
    # print point_to_weight
    for classifier in classifier_to_misclassified:
    	errorRates[classifier]=0
    	for point in classifier_to_misclassified[classifier]:
    		if classifier in errorRates:
    			errorRates[classifier]+=point_to_weight[point]
    		else:
    			errorRates[classifier]=point_to_weight[point]
    return errorRates

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""

    if use_smallest_error:
    	best=min(classifier_to_error_rate, key=lambda x: (classifier_to_error_rate[x], x))
    	if classifier_to_error_rate[best]==make_fraction(0.5):
    		raise NoGoodClassifiersError
    else:
    	best=min(classifier_to_error_rate, key=lambda x: (-abs(classifier_to_error_rate[x]-make_fraction(0.5)), x))
    	if classifier_to_error_rate[best]==make_fraction(0.5):
    		raise NoGoodClassifiersError
    return best


def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 0:
        power = INF
    elif error_rate == 1:
        power = -INF
    else:
        power = make_fraction(1,2) * ln(make_fraction((1 - error_rate),error_rate))
    return power

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    d = {}
    answer = set()
    for point in training_points:
        d[point] = 0

    for classifier in H:
        for point in classifier_to_misclassified[classifier[0]]:
            d[point] -= (classifier[1])
        for point in training_points:
            if point not in classifier_to_misclassified[classifier[0]]:
                d[point] += classifier[1]
    #print d
    for i in d:
    #print i
        if d[i] <= 0:
            answer.add(i)
    return answer

def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    mis = get_overall_misclassifications(H, training_points, classifier_to_misclassified)
    if len(mis) <= mistake_tolerance:
        return True
    return False

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    ans = {}
    for mispoint in misclassified_points:
        new_weight = make_fraction(1,2) * make_fraction(1, error_rate) * point_to_weight[mispoint]
        ans[mispoint] = new_weight
    for j in point_to_weight.keys():
        if j not in misclassified_points:
            new_weight = make_fraction(1,2) * make_fraction(1, (1 - error_rate)) * point_to_weight[j]
            ans[j] = new_weight
    return ans

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    weights = initialize_weights(training_points)
    H = []
    r = 0
    while r < max_rounds:
        #print r
        #print H

        if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
            return H
        error_rates = calculate_error_rates(weights, classifier_to_misclassified)
        try:
            best_class = pick_best_classifier(error_rates, use_smallest_error)
        except:
            return H
    #    print best_class
        voting_power = calculate_voting_power(error_rates[best_class])
        H.append((best_class, voting_power))
        weights = update_weights(weights, classifier_to_misclassified[best_class], error_rates[best_class])

        r += 1
    return H



#### SURVEY ####################################################################

NAME = 'Dimitris Koutentakis'
COLLABORATORS = 'Carl Unger, Luana Lopes Lara, Meia Aslup'
HOW_MANY_HOURS_THIS_LAB_TOOK = 6
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
