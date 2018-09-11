# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and Jake Barnwell (jb16)

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""

    if id_tree.is_leaf():
        #print "classification", id_tree.get_node_classification()
        return id_tree.get_node_classification()
    else:
            id_tree=id_tree.apply_classifier(point)
            return id_tree_classify_point(point,id_tree)
            #print id_tree

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    #print "\n\n\n"
    #print "data: ", data
    #print "classifier: ", classifier
    #print "\n"
    classify_dict={}
    for point in data:
        #print "name: ", classifier.name
        #print "point classification: ", classifier.classify(point)
        #if classifier.classify(point):
        feature=classifier.classify(point)
        if feature not in classify_dict:
            classify_dict[feature]=[point]
        else:
            classify_dict[feature].append(point)
    #print "classiciation dictionary: ", classify_dict

    return classify_dict


#### CALCULATING DISORDER

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    #print '\n\n\n'
    #print "data: ", data
    features= split_on_classifier(data, target_classifier)
    #print "\n split: ", features
    disorder=0
    for feature in features:
        nbc_nb=float(len(features[feature]))/len(data)
        disorder-=(nbc_nb)*log2(nbc_nb)
    return disorder


def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    #print '\n\n\n data', data, '\ntest_classifier', test_classifier, '\ntarget_classifier', target_classifier
    branches=split_on_classifier(data, test_classifier)
    #print '\n ***branches***',branches
    avg_disorder=0
    for branch in branches:
        disorder=branch_disorder(branches[branch],target_classifier)
        #print 'sub-branch: ', split_on_classifier(branches[branch], target_classifier)
        avg_disorder+=(float(len(branches[branch])))/(len(data))*disorder
    #print avg_disorder
    return avg_disorder
## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:
#for classifier in tree_classifiers:
#    print classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type"))


#### CONSTRUCTING AN ID TREE

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    #print '\n\n\nclassifiers: ', possible_classifiers
    min_disorder=INF
    for classifier in possible_classifiers:

        a_disorder=average_test_disorder(data, classifier, target_classifier)
        if a_disorder<min_disorder:
            min_disorder=a_disorder
            best_classifier=classifier
            #print best_classifier, min_disorder
    if len(split_on_classifier(data, best_classifier))==1:
        raise NoGoodClassifiersError
    return best_classifier

## To find the best classifier from 2014 Q2, Part A, uncomment:
#print find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type"))


def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if not id_tree_node:
        id_tree_node = IdentificationTreeNode(target_classifier)
    if len(split_on_classifier(data, target_classifier)) == 1: #leaf node
        id_tree_node.set_node_classification(target_classifier.classify(data[0]))
        return id_tree_node
    try:
        classifyby = find_best_classifier(data, possible_classifiers, target_classifier)
        groups = split_on_classifier(data, classifyby)
        id_tree_node.set_classifier_and_expand(classifyby, groups)
    except NoGoodClassifiersError:
        return id_tree_node

    for (feature,child_node) in id_tree_node.get_branches().items():
        child_data = groups[feature]
        construct_greedy_id_tree(child_data, possible_classifiers, target_classifier, child_node)
    return id_tree_node




## To construct an ID tree for 2014 Q2, Part A:
#print construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
#tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
#print id_tree_classify_point(tree_test_point, tree_tree)

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
#print construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification"))
#print construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class"))


#### MULTIPLE CHOICE

ANSWER_1 = 'bark_texture'
ANSWER_2 = 'leaf_shape'
ANSWER_3 = 'orange_foliage'

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### MULTIPLE CHOICE: DRAWING BOUNDARIES

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### WARM-UP: DISTANCE METRICS

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    tot =0
    for x in xrange(len(u)):
        tot += u[x]*v[x]
    return tot
def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    ans = 0
    for x in v:
        ans += x**2
    return math.sqrt(ans)

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    ans = 0
    point1_cord = point1.coords
    point2_cord = point2.coords
    if len(point1_cord) <= len(point2_cord):
        for x in range(len(point1_cord)):
            ans += (point2_cord[x] - point1_cord[x])**2
    else:
        for x in range(len(point2_cord)):
            ans += (point2_cord[x] - point1_cord[x])**2
    return math.sqrt(ans)


def manhattan_distance(point1, point2):
    ans = 0
    point1_cord = point1.coords
    point2_cord = point2.coords
    if len(point1_cord) <= len(point2_cord):
        for x in xrange(len(point1_cord)):
            ans += abs(point2_cord[x] - point1_cord[x])
    else:
        for x in range(len(point2_cord)):
            ans += abs(point2_cord[x] - point1_cord[x])
    return ans

def hamming_distance(point1, point2):
    ans = 0
    point1_cord = point1.coords
    point2_cord = point2.coords
    if len(point1_cord) <= len(point2_cord):
        for i in xrange(len(point1_cord)):
            if point2_cord[i] != point1_cord[i]:
                ans +=1
    else:
        for i in xrange(len(point2_cord)):
            if point2_cord[i] != point1_cord[i]:
                ans +=1
    return ans


def cosine_distance(point1, point2):

    point1c = point1.coords
    point2c = point2.coords
    equation = (dot_product(point1c, point2c)) / (norm(point1c)* norm(point2c))
    return 1 - equation

#### CLASSIFYING POINTS

def get_k_closest_points(point, data, k, distance_metric):
    dist = []
    for i in data:
        dist.append((i, distance_metric(i, point)))
    dist.sort(key=lambda x: x[0].coords)
    dist.sort(key=lambda x: x[1])
    dist = [i[0] for i in dist][:k]
    return dist

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    nearby = get_k_closest_points(point, data, k, distance_metric)
    points_class = [x.classification for x in nearby]
    #print points_class
    #print nearby
    points = [(x, points_class.count(x)) for x in points_class]


    return max(points, key = lambda k: k[1])[0]


## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
#print knn_classify_point(knn_tree_test_point, knn_tree_data, 5, euclidean_distance)


#### CHOOSING k

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    cc = 0

    for i in data:
        modified_set = data[:]
        modified_set.remove(i)


        classification = knn_classify_point(i, modified_set, k, distance_metric)
        if classification ==  i.classification:
            cc += 1

    return float(cc) / len(data)

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    ans = (0, None)
    optimal = 0
    metrics = [euclidean_distance,
                manhattan_distance,
                hamming_distance,
                cosine_distance]
    for i in xrange(1,10):
        ans, optimal = test_det(data, i, metrics, optimal, ans)
    return ans

def test_det(data, k, metrics, optimal, ans):
    for i in metrics:
            test = cross_validate(data, k, i)
            #print test

            if test > optimal:
                ans = (k, i)
                optimal = test
            #print "test, optimal", test,optimal
    return ans, optimal

## To find the best k and distance metric for 2014 Q2, part B, uncomment:
#print find_best_k_and_metric(knn_tree_data)


#### MORE MULTIPLE CHOICE

kNN_ANSWER_1 = 'Overfitting'
kNN_ANSWER_2 = 'Underfitting'
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3

#### SURVEY ###################################################

NAME = 'Dimitris Koutentakis'
COLLABORATORS = 'Carl Unger'
HOW_MANY_HOURS_THIS_LAB_TOOK = 11
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
