# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
from utils import *


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    N = len(training_points)
    w = {}
    for i in training_points:
        w[i] = make_fraction(1,N)
    return w

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    d = {}
    for i in classifier_to_misclassified.keys():
        w = 0
        for j in classifier_to_misclassified[i]:
            w += make_fraction(point_to_weight[j])
        d[i] = w
    return d

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    error_rates = classifier_to_error_rate

    if use_smallest_error:
        best_class = min(error_rates, key = lambda x: (error_rates[x],x))
        if classifier_to_error_rate[best_class] != make_fraction(1,2):
            return best_class
        raise NoGoodClassifiersError('sorry, 1/2')

    else:
        best_class =  min(error_rates, key = lambda x: (-abs(error_rates[x]-make_fraction(1,2)),x))
        if classifier_to_error_rate[best_class] != make_fraction(1,2):
            return best_class
        raise NoGoodClassifiersError('sorry, 1/2')


def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 0:
        vp = INF
    elif error_rate == 1:
        vp = -INF
    else:
        vp = make_fraction(1,2) * ln(make_fraction((1 - error_rate),error_rate))
    return vp

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

    for i in d:
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
    misclass = get_overall_misclassifications(H, training_points, classifier_to_misclassified)
    if len(misclass) > mistake_tolerance:
        return False
    return True

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    answer = {}
    for i in misclassified_points:
        nw = make_fraction(1,2) * make_fraction(1, error_rate) * point_to_weight[i]
        answer[i] = nw
    for j in point_to_weight.keys():
        if j not in misclassified_points:
            nw = make_fraction(1,2) * make_fraction(1, (1 - error_rate)) * point_to_weight[j]
            answer[j] = nw
    return answer

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    weights = initialize_weights(training_points)
    H = []
    rounds = 0

    while rounds < max_rounds:
        if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
            return H
        error_rates = calculate_error_rates(weights, classifier_to_misclassified)
        try:
            best_class = pick_best_classifier(error_rates, use_smallest_error)
        except:
            return H
        voting_power = calculate_voting_power(error_rates[best_class])
        H.append((best_class, voting_power))
        weights = update_weights(weights, classifier_to_misclassified[best_class], error_rates[best_class])
        rounds += 1

    return H


#### SURVEY ####################################################################

NAME = 'Luana Lopes Lara'
COLLABORATORS = 'Dimitris Koutentakis, Carl Unger, Nicole Chesnokov'
HOW_MANY_HOURS_THIS_LAB_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'I now feel like I really understand what adaboost does'
WHAT_I_FOUND_BORING = 'Too long'
SUGGESTIONS = 'None'
