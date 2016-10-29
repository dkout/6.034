#!/usr/bin/env python2

# MIT 6.034 Lab 7: Support Vector Machines
# This file is based on code originally written by Crystal Pan.

from lab7 import *
from display_svm import create_svm_graph
INF = float('inf')
from time import time


"""
sample_data_1:

 + 5     /
   4 +  /  -
   3   /
   2  /  -
   1 /       -
-1 0 1 2 3 4 5


sample_data_2:

6   \             +
5    \   +
4     \
3  -   \
2       \   +
1  -     \
0  1  2  3  4  5  6
"""


def train_svm(training_points, kernel_fn=dot_product, max_iter=500,
              show_graph=True, animate=True, animation_delay=0.5):
    """Performs SMO using all of the training points until there are no changed
    alphas or until the max iteration depth is reached""" #todo wiki NO changed alphas
    # Define alias for kernel function, converting Points to coordinates just in case
    K = lambda p1, p2: kernel_fn(p1.coords, p2.coords)

    # Initialize SVM
    svm = SupportVectorMachine([0,0], 0, training_points, [])

    if show_graph:
        update_svm_plot = create_svm_graph(training_points)

        if animate and animation_delay > 0:
            # Keep track of last update time
            last_update_time = time()

    b = 0
    changed_alphas = True
    iteration = 0

    while changed_alphas and iteration < max_iter:
        changed_alphas = False

        # Two nested summations, as in lecture
        for i in training_points:
            for j in training_points:

                # If the points are the same or have the same coordinates, skip this pair
                if i.name == j.name or i.coords == j.coords:
                    continue

                # Compute lower and upper bounds on j.alpha
                if i.classification == j.classification:
                    if i.alpha == 0 and j.alpha == 0:
                        # Skip this pair, because they are both non-SVs of the same class,
                        # so no need to update their alphas or make one become a SV
                        continue
                    lower_bound = 0
                    upper_bound = i.alpha + j.alpha
                else:
                    lower_bound = max(0, j.alpha - i.alpha)
                    upper_bound = INF

                # Compute current error of alpha_i and alpha_j
                error_i = reduce(lambda total,pt: total + (pt.classification * pt.alpha * K(i,pt) + b), training_points, 0) - i.classification
                error_j = reduce(lambda total,pt: total + (pt.classification * pt.alpha * K(j,pt) + b), training_points, 0) - j.classification

                # Store old alpha values before updating
                old_alpha_i = i.alpha
                old_alpha_j = j.alpha

                # Update j.alpha, but keep it between lower and upper bounds
                n = 2 * K(i,j) - K(i,i) - K(j,j) # Note: if K is dot_product, n = -||i-j||^2
                j.alpha = old_alpha_j - ( j.classification * (error_i - error_j) / float(n) )
                if j.alpha > upper_bound:
                    j.alpha = upper_bound
                elif j.alpha < lower_bound:
                    j.alpha = lower_bound

                # If j.alpha hasn't changed *at all*, continue
                if j.alpha == old_alpha_j:
                    continue

                # Else, note that alphas have changed
                changed_alphas = True

                # Update i.alpha, but ensure it stays non-negative
                i.alpha = max(0, old_alpha_i + (i.classification * j.classification) * (old_alpha_j - j.alpha))

                if show_graph and animate and animation_delay > 0:
                    # Store old values
                    old_w = svm.w[:]
                    old_support_vectors = svm.support_vectors[:]
                    old_b = svm.b

                # Update w, b, and SVs based on alphas
                svm = update_svm_from_alphas(svm) # Note: kernel_fn is hardcoded as dot_product

                # Update b
                b = svm.b

            if show_graph and animate and changed_alphas:
                skip_delay = False
                if animation_delay > 0:
                    # If values have not changed perceptibly, don't delay for this update
                    if (map(lambda sv: sv.name, svm.support_vectors) == map(lambda sv: sv.name, old_support_vectors)
                        and list_approx_equal(scalar_mult(1./b, svm.w), scalar_mult(1./old_b, old_w), 0.001)):
                        skip_delay=True
                    else:
                        while time() - last_update_time < animation_delay:
                            pass
                        last_update_time = time()

                if skip_delay:
                    # Set values back to old values as a baseline for whether to delay next animation
                    svm.w = old_w[:]
                    svm.b = old_b
                    svm.support_vectors = old_support_vectors[:]
                else:
                    update_svm_plot(svm)

        iteration += 1

    print '# iterations:', iteration

    # Compute final w, b, and SVs based on alphas
    svm = update_svm_from_alphas(svm) # Note: kernel_fn is hardcoded as dot_product

    # Check training
    misclassified = misclassified_training_points(svm)
    print "SVM with decision boundary %.3f*x + %.3f*y + %.3f >= 0 misclassified %i points." % (svm.w[0], svm.w[1], svm.b, len(misclassified))

    if show_graph:
        # Update graph with final values
        update_svm_plot(svm, final_update=True)

    # Return the trained SVM
    return svm


if __name__ == '__main__':
    # Uncomment below to train on a different dataset.  Feel free to use different arguments!
    train_svm(sample_data_1)
#    train_svm(sample_data_2)
#    train_svm(recit_data)
#    train_svm(harvard_mit_data)
#    train_svm(unseparable_data, animation_delay=0)
