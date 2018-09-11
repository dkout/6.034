# MIT 6.034 Lab 7: Support Vector Machines
# Written by Jessica Noss (jmn) and 6.034 staff

from svm_data import *

# Vector math
def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    sum =0
    for i in xrange(len(u)):
        sum+=u[i]*v[i]

    return sum

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    sum =0
    for i in v:
        sum+=i**2
    return sum**0.5

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    return dot_product(svm.w, point.coords) + svm.b

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's true
    classification is unknown.  Returns +1 or -1, or 0 if point is on boundary"""

    if positiveness(svm, point)>0:
        return 1
    elif positiveness(svm, point)<0:
        return -1
    else:
        return 0

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2.0/norm(svm.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    failingpoints=set()
    for point in svm.training_points:
        if abs(positiveness(svm, point))<1:
            failingpoints.add(point)
        if point in svm.support_vectors:
            if positiveness(svm, point)!=point.classification:
                failingpoints.add(point)
    return failingpoints


# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    violateset=set()
    for point in svm.training_points:
        if point not in svm.support_vectors:
            if point.alpha!=0:
                violateset.add(point)
        else:
            if point.alpha<=0:
                violateset.add(point)
    return violateset
def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    sum=0
    w=scalar_mult(0,svm.w)
    for point in svm.training_points:
        sum += point.alpha*point.classification
        w=vector_add(w, scalar_mult(point.alpha*point.classification, point.coords))
    if w==svm.w and sum ==0:
        return True
    return False

# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    incorrectlyclassified=set()
    for point in svm.training_points:
        if classify(svm, point)!=point.classification:
            incorrectlyclassified.add(point)
    return incorrectlyclassified

# Training
def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b.  Return the updated SVM."""
    support_vectors=[]
    for point in svm.training_points:
        if point.alpha>0:
            support_vectors.append(point)
    svm.support_vectors=support_vectors
    w=(0,0)
    for v in svm.training_points:
        w=vector_add(w, scalar_mult(v.alpha*v.classification, v.coords))
    svm.w=w
    b_min=100000
    b_max=-100000
    for v in svm.support_vectors:
        b = -dot_product(svm.w, v)+v.classification
        if v.classification==1:
            if b>b_max:
                b_max=b
        if v.classification==-1:
            if b<b_min:
                b_min=b
    print "B MIN, MAX: ", b_min, b_max
    svm.b=(b_min+b_max)/2.0

    return svm


# Multiple choice
ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ['A','D']
ANSWER_6 = ['A','B','D']
ANSWER_7 = ['A','B','D']
ANSWER_8 = []
ANSWER_9 = ['A','B','D']
ANSWER_10 = ['A','B','D']

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1,3,6,8]
ANSWER_18 = [1,2,4,5,6,7,8]
ANSWER_19 = [1,2,4,5,6,7,8]
ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = 'Dimitris Koutentakis'
COLLABORATORS = 'Luana Lopes Lara, Carl Unger'
HOW_MANY_HOURS_THIS_LAB_TOOK = 6
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
