# MIT 6.034 Lab 7: Support Vector Machines

from tester import make_test, get_tests
from svm_problems import *
from random import random, randint

lab_number = 7 #for tester.py

def randnum(max_val=100):
    "Generates a random float 0 < n < max_val"
    return random() * randint(1, int(max_val))


## dot_product
def dot_product_0_getargs() :  #TEST 30
    return [(3, -7), [2.5, 10]]
def dot_product_0_testanswer(val, original_val = None) :
    return val == -62.5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_0_getargs,
          testanswer = dot_product_0_testanswer,
          expected_val = "-62.5",
          name = 'dot_product')

def dot_product_1_getargs() :  #TEST 31
    return [[4], (5,)]
def dot_product_1_testanswer(val, original_val = None) :
    return val == 20
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_1_getargs,
          testanswer = dot_product_1_testanswer,
          expected_val = "20",
          name = 'dot_product')

def dot_product_2_getargs() :  #TEST 32
    return [(1,2,3,4,2), (1, 10, 1000, 100, 10000)]
def dot_product_2_testanswer(val, original_val = None) :
    return val == 23421
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dot_product_2_getargs,
          testanswer = dot_product_2_testanswer,
          expected_val = "23421",
          name = 'dot_product')


## norm
def norm_0_getargs() :  #TEST 33
    return [(-3, 4)]
def norm_0_testanswer(val, original_val = None) :
    return val == 5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_0_getargs,
          testanswer = norm_0_testanswer,
          expected_val = "5",
          name = 'norm')

def norm_1_getargs() :  #TEST 34
    return [(17.2,)]
def norm_1_testanswer(val, original_val = None) :
    return val == 17.2
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_1_getargs,
          testanswer = norm_1_testanswer,
          expected_val = "17.2",
          name = 'norm')

def norm_2_getargs() :  #TEST 35
    return [[6, 2, 11, -2, 2]]
def norm_2_testanswer(val, original_val = None) :
    return val == 13
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = norm_2_getargs,
          testanswer = norm_2_testanswer,
          expected_val = "13",
          name = 'norm')


## positiveness
def positiveness_0_getargs() :  #TEST 36
    return [svm_basic.copy(), Point('p', (0, 0))]
def positiveness_0_testanswer(val, original_val = None) :
    return val == 3
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = positiveness_0_getargs,
          testanswer = positiveness_0_testanswer,
          expected_val = "3",
          name = 'positiveness')

def positiveness_1_getargs() :  #TEST 37
    return [SVM(Boundary([2, 5, -1, 1, 0, -0.1], 0.01)),
            Point('v', [3, -2, -7, -10, 99, 8])]
def positiveness_1_testanswer(val, original_val = None) :
    return val == -7.79
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = positiveness_1_getargs,
          testanswer = positiveness_1_testanswer,
          expected_val = "-7.79",
          name = 'positiveness')

def positiveness_2_getargs() :  #TEST 38
    return [svm_untrained.copy(), ptD]
def positiveness_2_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = positiveness_2_getargs,
          testanswer = positiveness_2_testanswer,
          expected_val = "0",
          name = 'positiveness')


## classify
#point doesn't have classification
def classify_0_getargs() :  #TEST 39
    return [svm_basic.copy(), Point('test_point', (0, 0))]
def classify_0_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_0_getargs,
          testanswer = classify_0_testanswer,
          expected_val = "+1",
          name = 'classify')

#point has classification; misclassified
def classify_1_getargs() :  #TEST 40
    return [svm_untrained.copy(), ptF]
def classify_1_testanswer(val, original_val = None) :
    return val == -1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_1_getargs,
          testanswer = classify_1_testanswer,
          expected_val = "-1",
          name = 'classify')

#point has classification; classified correctly
def classify_2_getargs() :  #TEST 41
    return [svm_basic.copy(), ptD]
def classify_2_testanswer(val, original_val = None) :
    return val == -1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_2_getargs,
          testanswer = classify_2_testanswer,
          expected_val = "-1",
          name = 'classify')

# point on boundary
def classify_3_getargs() :  #TEST 42
    return [svm_basic.copy(), Point('x', [1.5, randnum()])]
def classify_3_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_3_getargs,
          testanswer = classify_3_testanswer,
          expected_val = "0",
          name = 'classify')

#point within margin, not on boundary
def classify_4_getargs() :  #TEST 43
    return [svm_basic.copy(), Point('x', [1.6, randnum()])]
def classify_4_testanswer(val, original_val = None) :
    return val == -1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = classify_4_getargs,
          testanswer = classify_4_testanswer,
          expected_val = "-1",
          name = 'classify')


## margin_width
# w=[-3,4], so norm=5 -> 0.4
def margin_width_0_getargs() :  #TEST 44
    return [SVM(Boundary((-3, 4), -13.78))]
def margin_width_0_testanswer(val, original_val = None) :
    return val == 0.4
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_0_getargs,
          testanswer = margin_width_0_testanswer,
          expected_val = "0.4",
          name = 'margin_width')

# w=[1,0], point on boundary, point misclassified -> 2 (ignore points)
def margin_width_1_getargs() :  #TEST 45
    return [svm_untrained.copy()]
def margin_width_1_testanswer(val, original_val = None) :
    return val == 2
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_1_getargs,
          testanswer = margin_width_1_testanswer,
          expected_val = "2",
          name = 'margin_width')

# 1D
def margin_width_2_getargs() :  #TEST 46
    return [SVM(Boundary([0.25], 0))]
def margin_width_2_testanswer(val, original_val = None) :
    return val == 8
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_2_getargs,
          testanswer = margin_width_2_testanswer,
          expected_val = "8",
          name = 'margin_width')

# higher number of dimensions
def margin_width_3_getargs() :  #TEST 47
    return [SVM(Boundary([0, -5, 0, 12], 1))]
def margin_width_3_testanswer(val, original_val = None) :
    return approx_equal(val, 2./13, 0.000001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = margin_width_3_getargs,
          testanswer = margin_width_3_testanswer,
          expected_val = "~" + str(2./13),
          name = 'margin_width')


## check_gutter_constraint
# pass -> empty set
def check_gutter_constraint_0_getargs() :  #TEST 48
    return [svm_basic.copy()]
def check_gutter_constraint_0_testanswer(val, original_val = None) :
    return val == set()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_gutter_constraint_0_getargs,
          testanswer = check_gutter_constraint_0_testanswer,
          expected_val = set(),
          name = 'check_gutter_constraint')

# fail gutter constraint equation
def check_gutter_constraint_1_getargs() :  #TEST 49
    return [svm_basic.copy().set_boundary(Boundary([1, 0], -1.5))]
check_gutter_constraint_1_expected = set([ptA, ptB, ptD])
def check_gutter_constraint_1_testanswer(val, original_val = None) :
    return equality_by_string(val, check_gutter_constraint_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_gutter_constraint_1_getargs,
          testanswer = check_gutter_constraint_1_testanswer,
          expected_val = check_gutter_constraint_1_expected,
          name = 'check_gutter_constraint')

# fail with point in gutter
def check_gutter_constraint_2_getargs() :  #TEST 50
    svm = svm_basic.copy()
    svm.training_points.append(ptL)
    return [svm]
check_gutter_constraint_2_expected = set([ptL])
def check_gutter_constraint_2_testanswer(val, original_val = None) :
    return equality_by_string(val, check_gutter_constraint_2_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_gutter_constraint_2_getargs,
          testanswer = check_gutter_constraint_2_testanswer,
          expected_val = check_gutter_constraint_2_expected,
          name = 'check_gutter_constraint')


## check_alpha_signs
# set should include: sv w alpha=0, sv w alpha<0, pt w alpha < 0, pt w alpha > 0
# set should not include: sv w alpha > 0, pt w alpha = 0
def check_alpha_signs_0_getargs() :  #TEST 51
    return [svm_alphas.copy()]
check_alpha_signs_0_expected = set([ptF, ptG, ptJ, ptH, ptD])
def check_alpha_signs_0_testanswer(val, original_val = None) :
    return equality_by_string(val, check_alpha_signs_0_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_signs_0_getargs,
          testanswer = check_alpha_signs_0_testanswer,
          expected_val = str(check_alpha_signs_0_expected),
          name = 'check_alpha_signs')

# return empty set
def check_alpha_signs_1_getargs() :  #TEST 52
    return [svm_basic.copy()]
def check_alpha_signs_1_testanswer(val, original_val = None) :
    return val == set()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_signs_1_getargs,
          testanswer = check_alpha_signs_1_testanswer,
          expected_val = set(),
          name = 'check_alpha_signs')


## check_alpha_equations
# both equations hold -> True
def check_alpha_equations_0_getargs() :  #TEST 53
    return [svm_basic.copy()]
def check_alpha_equations_0_testanswer(val, original_val = None) :
    return val == True
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_0_getargs,
          testanswer = check_alpha_equations_0_testanswer,
          expected_val = "True",
          name = 'check_alpha_equations')

# Eq 4 fails
def check_alpha_equations_1_getargs() :  #TEST 54
    return [svm_fail_eq4.copy()]
def check_alpha_equations_1_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_1_getargs,
          testanswer = check_alpha_equations_1_testanswer,
          expected_val = "False",
          name = 'check_alpha_equations')

# Eq 5 fails
def check_alpha_equations_2_getargs() :  #TEST 55
    return [svm_fail_eq5.copy()]
def check_alpha_equations_2_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = check_alpha_equations_2_getargs,
          testanswer = check_alpha_equations_2_testanswer,
          expected_val = "False",
          name = 'check_alpha_equations')


## misclassified_training_points
def misclassified_training_points_0_getargs() :  #TEST 56
    return [svm_basic.copy()]
def misclassified_training_points_0_testanswer(val, original_val = None) :
    return val == set()
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = misclassified_training_points_0_getargs,
          testanswer = misclassified_training_points_0_testanswer,
          expected_val = set(),
          name = 'misclassified_training_points')

def misclassified_training_points_1_getargs() :  #TEST 57
    return [svm_untrained.copy()]
misclassified_training_points_1_expected = set([ptD, ptF])
def misclassified_training_points_1_testanswer(val, original_val = None) :
    return equality_by_string(val, misclassified_training_points_1_expected)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = misclassified_training_points_1_getargs,
          testanswer = misclassified_training_points_1_testanswer,
          expected_val = str(misclassified_training_points_1_expected),
          name = 'misclassified_training_points')
