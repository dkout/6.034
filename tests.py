<<<<<<< HEAD
# MIT 6.034 Lab 6: Neural Nets

from tester import make_test, get_tests
from nn_problems import *
from lab6 import sigmoid, ReLU
from random import random, randint
from math import cos, e

lab_number = 6 #for tester.py

def randnum(max_val=100):
    "Generates a random float 0 < n < max_val"
    return random() * randint(1, int(max_val))

def dict_contains(d, pairs):
    "Returns True if d contains all the specified pairs, otherwise False"
    items = d.items()
    return all([p in items for p in pairs])

def dict_approx_equal(dict1, dict2, epsilon=0.00000001):
    """Returns True if two dicts have the same keys and approximately equal
    values, otherwise False"""
    return (set(dict1.keys()) == set(dict2.keys())
            and all([approx_equal(dict1[key], dict2[key], epsilon)
                     for key in dict1.keys()]))


# WIRING A NEURAL NET

nn_half_getargs = 'nn_half'
def nn_half_testanswer(val, original_val = None):  #TEST 1
    if val == []:
        raise NotImplementedError
    return val == [1]
make_test(type = 'VALUE',
          getargs = nn_half_getargs,
          testanswer = nn_half_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_half_getargs)

nn_angle_getargs = 'nn_angle'
def nn_angle_testanswer(val, original_val = None):  #TEST 2
    if val == []:
        raise NotImplementedError
    return val == [2, 1]
make_test(type = 'VALUE',
          getargs = nn_angle_getargs,
          testanswer = nn_angle_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_angle_getargs)

nn_cross_getargs = 'nn_cross'
def nn_cross_testanswer(val, original_val = None):  #TEST 3
    if val == []:
        raise NotImplementedError
    return val == [2, 2, 1]
make_test(type = 'VALUE',
          getargs = nn_cross_getargs,
          testanswer = nn_cross_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_cross_getargs)

nn_stripe_getargs = 'nn_stripe'
def nn_stripe_testanswer(val, original_val = None):  #TEST 4
    if val == []:
        raise NotImplementedError
    return val == [3, 1]
make_test(type = 'VALUE',
          getargs = nn_stripe_getargs,
          testanswer = nn_stripe_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_stripe_getargs)

nn_hexagon_getargs = 'nn_hexagon'
def nn_hexagon_testanswer(val, original_val = None):  #TEST 5
    if val == []:
        raise NotImplementedError
    return val == [6, 1]
make_test(type = 'VALUE',
          getargs = nn_hexagon_getargs,
          testanswer = nn_hexagon_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer)'),
          name = nn_hexagon_getargs)

nn_grid_getargs = 'nn_grid'
def nn_grid_testanswer(val, original_val = None):  #TEST 6
    if val == []:
        raise NotImplementedError
    return val == [4, 2, 1]
make_test(type = 'VALUE',
          getargs = nn_grid_getargs,
          testanswer = nn_grid_testanswer,
          expected_val = ('(list indicating correct minimum number of neurons '
                          + 'per layer) Hint: This one is tricky, but there '
                          + 'exists a neat solution with 7 neurons total.'),
          name = nn_grid_getargs)


## stairstep
#T=0, x>T -> 1
def stairstep_0_getargs() :  #TEST 7
    return [randnum()]
def stairstep_0_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = stairstep_0_getargs,
          testanswer = stairstep_0_testanswer,
          expected_val = "1",
          name = 'stairstep')

#T=0, x<T -> 0
def stairstep_1_getargs() :  #TEST 8
    return [-randnum(), 0]
def stairstep_1_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = stairstep_1_getargs,
          testanswer = stairstep_1_testanswer,
          expected_val = "0",
          name = 'stairstep')

#T>0, x=T -> 1
def stairstep_2_getargs() :  #TEST 9
    T = randnum()
    return [T, T]
def stairstep_2_testanswer(val, original_val = None) :
    return val == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = stairstep_2_getargs,
          testanswer = stairstep_2_testanswer,
          expected_val = "1",
          name = 'stairstep')


## sigmoid
#S=1, M=0, x>>M -> ~1
def sigmoid_0_getargs() :  #TEST 10
    return [10, 1, 0]
def sigmoid_0_testanswer(val, original_val = None) :
    return approx_equal(val, 0.9999, 0.0001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_0_getargs,
          testanswer = sigmoid_0_testanswer,
          expected_val = "~0.9999",
          name = 'sigmoid')

#S=any, M>>0, x=M -> 0.5
def sigmoid_1_getargs() :  #TEST 11
    M = randnum()+10
    return [M, randnum(), M]
def sigmoid_1_testanswer(val, original_val = None) :
    return val == 0.5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_1_getargs,
          testanswer = sigmoid_1_testanswer,
          expected_val = "0.5",
          name = 'sigmoid')

#S=1, M>>0, x=0 -> ~0
def sigmoid_2_getargs() :  #TEST 12
    return [0, 1, 15]
def sigmoid_2_testanswer(val, original_val = None) :
    return approx_equal(val, 0, 0.00001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_2_getargs,
          testanswer = sigmoid_2_testanswer,
          expected_val = "~0",
          name = 'sigmoid')

#S=0.5, M=0.5, x=0 -> ~0.4378 (arbitrary parameters)
def sigmoid_3_getargs() :  #TEST 13
    return [0, 0.5, 0.5]
def sigmoid_3_testanswer(val, original_val = None) :
    return approx_equal(val, 0.4378, 0.0001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = sigmoid_3_getargs,
          testanswer = sigmoid_3_testanswer,
          expected_val = "~0.4378",
          name = 'sigmoid')

## ReLU
# x > 0 -> x
def ReLU_0_getargs() :  #TEST 14
    return [12]
def ReLU_0_testanswer(val, original_val = None) :
    return val == 12
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = ReLU_0_getargs,
          testanswer = ReLU_0_testanswer,
          expected_val = "12",
          name = 'ReLU')

# x > 0 -> x
ReLU_1_arg = randnum()
def ReLU_1_getargs() :  #TEST 15
    return [ReLU_1_arg]
def ReLU_1_testanswer(val, original_val = None) :
    return val == ReLU_1_arg
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = ReLU_1_getargs,
          testanswer = ReLU_1_testanswer,
          expected_val = "{}".format(ReLU_1_arg),
          name = 'ReLU')

ReLU_2_arg = -1 * randnum()
def ReLU_2_getargs() :  #TEST 16
    return [ReLU_2_arg]
def ReLU_2_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = ReLU_2_getargs,
          testanswer = ReLU_2_testanswer,
          expected_val = "0",
          name = 'ReLU')

## accuracy
#d=a -> 0
def accuracy_0_getargs() :  #TEST 17
    d = randnum()-50
    return [d, d]
def accuracy_0_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = accuracy_0_getargs,
          testanswer = accuracy_0_testanswer,
          expected_val = "0",
          name = 'accuracy')

#d=1, a=0 -> -0.5
def accuracy_1_getargs() :  #TEST 18
    return [1, 0]
def accuracy_1_testanswer(val, original_val = None) :
    return val == -0.5
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = accuracy_1_getargs,
          testanswer = accuracy_1_testanswer,
          expected_val = "-0.5",
          name = 'accuracy')

#d=0, a=0.3 -> -0.045 (arbitrary parameters)
def accuracy_2_getargs() :  #TEST 19
    return [0, 0.3]
def accuracy_2_testanswer(val, original_val = None) :
    return val == -0.045
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = accuracy_2_getargs,
          testanswer = accuracy_2_testanswer,
          expected_val = "-0.045",
          name = 'accuracy')


## forward_prop
#basic fwd prop, 1 neuron, constant and variable inputs
def forward_prop_0_getargs() :  #TEST 20
    return [nn_basic.copy(), nn_basic_inputs.copy()]
def forward_prop_0_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, [('neuron', 1)])
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_0_getargs,
          testanswer = forward_prop_0_testanswer,
          expected_val = ("(1, (dict containing key-value pair: "
                          + "('neuron', 1))"),
          name = 'forward_prop')

#1 neuron, edge case: ==T -> 1
def forward_prop_1_getargs() :  #TEST 21
    return [nn_AND.copy(), {'x':1.5, 'y':0}]
def forward_prop_1_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, [('N1', 1)])
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_1_getargs,
          testanswer = forward_prop_1_testanswer,
          expected_val = ("(1, (dict containing key-value pair: "
                          + "('N1', 1)))"),
          name = 'forward_prop')

#5 neurons, XOR of two lines
def forward_prop_2_getargs() :  #TEST 22
    return [nn_XOR_lines.copy(), {'x':0.5, 'y':4}]
forward_prop_2_expected_outputs = [('line1', 0), ('line2', 0),
                                   ('X1', 0), ('X2', 1), ('AND', 0)]
def forward_prop_2_testanswer(val, original_val = None) :
    out, d = val
    return out == 0 and dict_contains(d, forward_prop_2_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_2_getargs,
          testanswer = forward_prop_2_testanswer,
          expected_val = ("(0, (dict containing key-value pairs: "
                          + str(forward_prop_2_expected_outputs) + "))"),
          name = 'forward_prop')

#5 neurons, XOR of two lines; shuffle to check for dependence on list ordering
def forward_prop_3_getargs() :  #TEST 23
    return [nn_XOR_lines.copy().shuffle_lists(), {'x':4, 'y':0.5}]
forward_prop_3_expected_outputs = [('line1', 1), ('line2', 0),
                                   ('X1', 1), ('X2', 1), ('AND', 1)]
def forward_prop_3_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, forward_prop_3_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_3_getargs,
          testanswer = forward_prop_3_testanswer,
          expected_val = ("(1, (dict containing key-value pairs: "
                          + str(forward_prop_3_expected_outputs) + "))"),
          name = 'forward_prop')

#3 neurons, River problem with stairstep function
def forward_prop_4_getargs() :  #TEST 24
    return [get_nn_River(1, -2, 5, 1, -2, 1), nn_River_inputs.copy()]
forward_prop_4_expected_outputs = [('A', 1), ('B', 0), ('C', 0)]
def forward_prop_4_testanswer(val, original_val = None) :
    out, d = val
    return out == 0 and dict_contains(d, forward_prop_4_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_4_getargs,
          testanswer = forward_prop_4_testanswer,
          expected_val = ("(0, (dict containing key-value pairs: "
                          + str(forward_prop_4_expected_outputs) + "))"),
          name = 'forward_prop')

#3 neurons, River problem with stairstep function
def forward_prop_5_getargs() :  #TEST 25
    return [get_nn_River(1, -2, 5, 3, -2, 1), nn_River_inputs.copy()]
forward_prop_5_expected_outputs = [('A', 1), ('B', 0), ('C', 1)]
def forward_prop_5_testanswer(val, original_val = None) :
    out, d = val
    return out == 1 and dict_contains(d, forward_prop_5_expected_outputs)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_5_getargs,
          testanswer = forward_prop_5_testanswer,
          expected_val = ("(1, (dict containing key-value pairs: "
                          + str(forward_prop_5_expected_outputs) + "))"),
          name = 'forward_prop')

#1 neuron, sigmoid
def forward_prop_6_getargs() :  #TEST 26
    return [nn_AND.copy(), {'x':1, 'y':1}, sigmoid]
def forward_prop_6_testanswer(val, original_val = None) :
    out, d = val
    return approx_equal(out, 0.622459, 0.0001) and d['N1'] == out
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_6_getargs,
          testanswer = forward_prop_6_testanswer,
          expected_val = ("(~0.62246, (dict containing key-value pair: "
                          + "('N1', ~0.62246)))"),
          name = 'forward_prop')

#1 neuron, different threshold function
def forward_prop_7_getargs() :  #TEST 27
    return [nn_AND.copy(), {'x':20, 'y':23.5}, ReLU]
def forward_prop_7_testanswer(val, original_val = None) :
    out, d = val
    return out == 42 and d['N1'] == out
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_7_getargs,
          testanswer = forward_prop_7_testanswer,
          expected_val = ("(42, (dict containing key-value pair: "
                          + "('N1', 42)))"),
          name = 'forward_prop')

# checks that the user doesn't modify the neural net
input_net = nn_AND.copy()
not_modified = input_net.copy()
def forward_prop_8_getargs() :  #TEST 28
    return [input_net, {'x':20, 'y':23.5}, ReLU]
def forward_prop_8_testanswer(val, original_val = None) :
    out, d = val
    return out == 42 and d['N1'] == out and input_net == not_modified
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = forward_prop_8_getargs,
          testanswer = forward_prop_8_testanswer,
          expected_val = ("(42, (dict containing key-value pair: "
                          + "('N1', 42))) and also checks for an unmodified neural net"),
          name = 'forward_prop')

#### GRADIENT ASCENT
def funct1(x, y, z):
    return 5 * x + 3 * y ** 3 + cos(e - z ** 2)

def funct2(x, y, z):
    return -x + y + z

def gradient_ascent_step_0_getargs() :  #TEST 29
    return [funct1, [2, -5, 3], 0.1]
def gradient_ascent_step_0_testanswer(val, original_val = None) :
    return approx_equal(val[0], -341.4470010762434, 0.001) and all(approx_equal(a,b,0.01) for (a,b) in zip(val[1], [2.1, -4.9, 3]))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = gradient_ascent_step_0_getargs,
          testanswer = gradient_ascent_step_0_testanswer,
          expected_val = "(-341.4470, [2.1, -4.9, 3])",
          name = 'gradient_ascent_step')

def gradient_ascent_step_1_getargs() :  #TEST 30
    return [funct2, [0, 0, 0], 0.001]
def gradient_ascent_step_1_testanswer(val, original_val = None) :
    return approx_equal(val[0], 0.003, 0.0001) and all(approx_equal(a,b,0.0001) for (a,b) in zip(val[1], [-0.001, 0.001, 0.001]))
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = gradient_ascent_step_1_getargs,
          testanswer = gradient_ascent_step_1_testanswer,
          expected_val = "(0.003, [-0.001, 0.001, 0.001])",
          name = 'gradient_ascent_step')

#### BACK PROP DEPENDENCIES

get_back_prop_dependencies_0_expected = set(["in1", Wire("in1", "neuron", 1), "neuron"])
def get_back_prop_dependencies_0_getargs() :  #TEST 31
    return [nn_basic.copy(), Wire("in1", "neuron", 1)]
def get_back_prop_dependencies_0_testanswer(val, original_val = None) :
    return val == get_back_prop_dependencies_0_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_back_prop_dependencies_0_getargs,
          testanswer = get_back_prop_dependencies_0_testanswer,
          expected_val = "{}".format(get_back_prop_dependencies_0_expected),
          name = 'get_back_prop_dependencies')

get_back_prop_dependencies_1_expected = set([-1, "N1", Wire(-1, "N1", 1.5)])
def get_back_prop_dependencies_1_getargs() :  #TEST 32
    return [nn_AND.copy(), Wire(-1, "N1", 1.5)]
def get_back_prop_dependencies_1_testanswer(val, original_val = None) :
    return val == get_back_prop_dependencies_1_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_back_prop_dependencies_1_getargs,
          testanswer = get_back_prop_dependencies_1_testanswer,
          expected_val = "set of inputs, Wires, and neurons necessary to update this weight",
          name = 'get_back_prop_dependencies')

get_back_prop_dependencies_2_expected = set(["x", "line2", "X1", "X2", "AND", Wire("x", "line2", 1), Wire("line2", "X1", 1), Wire("line2", "X2", -1), Wire("X1", "AND", 1), Wire("X2", "AND", 1)])
def get_back_prop_dependencies_2_getargs() :  #TEST 33
    return [nn_XOR_lines.copy(), Wire("x", "line2", 1)]
def get_back_prop_dependencies_2_testanswer(val, original_val = None) :
    return val == get_back_prop_dependencies_2_expected
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = get_back_prop_dependencies_2_getargs,
          testanswer = get_back_prop_dependencies_2_testanswer,
          expected_val = "set of inputs, Wires, and neurons necessary to update this weight",
          name = 'get_back_prop_dependencies')

#### BACKWARD PROPAGATION

## calculate_deltas
#3 weights to update, final layer only
def calculate_deltas_0_getargs() :  #TEST 34
    return [nn_AND.copy(), 1, {'N1': 0.5}]
def calculate_deltas_0_testanswer(val, original_val = None) :
    return val == {'N1': 0.125}
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_deltas_0_getargs,
          testanswer = calculate_deltas_0_testanswer,
          expected_val = "{'N1': 0.125}",
          name = 'calculate_deltas')

#6 weights to update (River nn); shuffled
def calculate_deltas_2_getargs() :  #TEST 35
    return [get_nn_River(1, -2, 5, 3, -2, 1).shuffle_lists(),
            nn_River_desired, nn_River_fwd_prop1.copy()]
calculate_deltas_2_expected_deltas = {'A': 0.04441976755198489,
                                      'B': -0.01186039570737828,
                                      'C': -0.1129630506644473}
def calculate_deltas_2_testanswer(val, original_val = None) :
    return dict_approx_equal(val, calculate_deltas_2_expected_deltas)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_deltas_2_getargs,
          testanswer = calculate_deltas_2_testanswer,
          expected_val = str(calculate_deltas_2_expected_deltas),
          name = 'calculate_deltas')

# Here's where all the numbers above came from:
#    A = sigmoid(1) = 0.7310585786300049
#    B = sigmoid(-2) = 0.11920292202211757
#    C = sigmoid(A*-2+B+3) = 0.839846413654423
#    delta_C = C*(1-C)*-C = -0.1129630506644473
#    delta_A = A*(1-A)*-2*delta_C = 0.04441976755198489
#    delta_B = B*(1-B)*delta_C = -0.011860395707378284

#requires summation over outgoing neurons C_i
def calculate_deltas_3_getargs() :  #TEST 36
    return [nn_branching.shuffle_lists(), 1, nn_branching_fwd_prop1.copy()]
calculate_deltas_3_expected_deltas = {'N1': 0.033042492944110255, \
    'N2': 0.027644450191861528, 'N3': -0.06291182225171182, \
    'Nin': -0.025101018356825537, 'Nout': 0.1406041318860752}
def calculate_deltas_3_testanswer(val, original_val = None) :
    return dict_approx_equal(val, calculate_deltas_3_expected_deltas)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = calculate_deltas_3_getargs,
          testanswer = calculate_deltas_3_testanswer,
          expected_val = str(calculate_deltas_3_expected_deltas),
          name = 'calculate_deltas')

# Here's where the numbers above came from:
# sigmoid(0) = 0.5
# delta_Nout = out*(1-out)*(1-out)
# delta_N1 = sigmoid(0.5)*(1-sigmoid(0.5))*1*delta_Nout
# delta_N2 = sigmoid(2*0.5)*(1-sigmoid(2*0.5))*1*delta_Nout
# delta_N3 = sigmoid(3*0.5)*(1-sigmoid(3*0.5))*-3*delta_Nout
# delta_Nin = 0.5*(1-0.5)*(delta_N1+2*delta_N2+3*delta_N3)


## update_weights
#3 weights to update, final layer only
def update_weights_0_getargs() :  #TEST 37
    return [nn_AND.copy(), nn_AND_input.copy(), 1, {'N1': 0.5}]
def update_weights_0_testanswer(val, original_val = None) :
    return val == nn_AND_update_iter1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_0_getargs,
          testanswer = update_weights_0_testanswer,
          expected_val = str(nn_AND_update_iter1),
          name = 'update_weights')

#3 weights to update, final layer only, different r
def update_weights_1_getargs() :  #TEST 38
    return [nn_AND.copy(), nn_AND_input.copy(), 1, {'N1': 0.5}, 10]
def update_weights_1_testanswer(val, original_val = None) :
    return val == nn_AND_update_iter1_r10
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_1_getargs,
          testanswer = update_weights_1_testanswer,
          expected_val = str(nn_AND_update_iter1_r10),
          name = 'update_weights')

#6 weights to update (River nn); shuffled
def update_weights_2_getargs() :  #TEST 39
    return [get_nn_River(1, -2, 5, 3, -2, 1).shuffle_lists(),
            nn_River_inputs.copy(), nn_River_desired, nn_River_fwd_prop1.copy()]
update_weights_2_expected_net = get_nn_River(1.0444197675519848, \
    -2.0118603957073784, 5, 2.8870369493355525, -2.08258260725646, \
    0.9865344742802654)
def update_weights_2_testanswer(val, original_val = None) :
    return val == update_weights_2_expected_net
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_2_getargs,
          testanswer = update_weights_2_testanswer,
          expected_val = str(update_weights_2_expected_net),
          name = 'update_weights')

# Here's where all the numbers above came from:
#    A = sigmoid(1) = 0.7310585786300049
#    B = sigmoid(-2) = 0.11920292202211757
#    C = sigmoid(A*-2+B+3) = 0.839846413654423
#    delta_C = C*(1-C)*-C = -0.1129630506644473
#    delta_A = A*(1-A)*-2*delta_C = 0.04441976755198489
#    delta_B = B*(1-B)*delta_C = -0.011860395707378284
#    w1 = 1+delta_A = 1.0444197675519848
#    w2 = -2+delta_B = -2.0118603957073784
#    w3 = 5 + 0 = 5
#    w4 = 3+delta_C = 2.8870369493355525
#    w5 = -2+A*delta_C = -2.08258260725646
#    w6 = 1+B*delta_C = 0.9865344742802654

#requires summation over outgoing neurons C_i
def update_weights_3_getargs() :  #TEST 40
    return [nn_branching.shuffle_lists(), nn_branching_input.copy(), 1, nn_branching_fwd_prop1.copy()]
def update_weights_3_testanswer(val, original_val = None) :
    return val.__eq__(nn_branching_update_iter1, 0.00000001)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = update_weights_3_getargs,
          testanswer = update_weights_3_testanswer,
          expected_val = str(nn_branching_update_iter1),
          name = 'update_weights')

# Here's where the numbers above came from:
# sigmoid(0) = 0.5
# delta_Nout = out*(1-out)*(1-out)
# delta_N1 = sigmoid(0.5)*(1-sigmoid(0.5))*1*delta_Nout
# delta_N2 = sigmoid(2*0.5)*(1-sigmoid(2*0.5))*1*delta_Nout
# delta_N3 = sigmoid(3*0.5)*(1-sigmoid(3*0.5))*-3*delta_Nout
# delta_Nin = 0.5*(1-0.5)*(delta_N1+2*delta_N2+3*delta_N3)
# w_in_to_Nin = 0 + 17*delta_Nin
# w_Nin_to_N1 = 1 + 0.5*delta_N1
# w_Nin_to_N2 = 2 + 0.5*delta_N2
# w_Nin_to_N3 = 3 + 0.5*delta_N3
# w_N1_to_Nout = 0 + sigmoid(0.5) * delta_Nout
# w_N2_to_Nout = 0 + sigmoid(2*0.5) * delta_Nout
# w_N3_to_Nout = 0 + sigmoid(3*0.5) * delta_Nout


## back_prop
#stops after 1 iter, better than default min_acc
def back_prop_0_getargs() :  #TEST 41
    return [nn_AND.copy(), {'x':3.5, 'y':-2}, 1, 10, -0.000001]
def back_prop_0_testanswer(val, original_val = None) :
    net, count = val
    return net == nn_AND_update_iter1_r10 and count == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_0_getargs,
          testanswer = back_prop_0_testanswer,
          expected_val = "(" + str(nn_AND_update_iter1_r10) + ", 1)",
          name = 'back_prop')

#stops after 1 iter, not as good as default min_acc
def back_prop_1_getargs() :  #TEST 42
    return [nn_AND.copy(), {'x':3.5, 'y':-2}, 1, 1, -0.01]
def back_prop_1_testanswer(val, original_val = None) :
    net, count = val
    return net == nn_AND_update_iter1 and count == 1
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_1_getargs,
          testanswer = back_prop_1_testanswer,
          expected_val = "(" + str(nn_AND_update_iter1) + ", 1)",
          name = 'back_prop')

#already high enough accuracy; stops after 0 iter
def back_prop_2_getargs() :  #TEST 43
    return [nn_AND.copy(), {'x':-10, 'y':-10}, 0]
def back_prop_2_testanswer(val, original_val = None) :
    net, count = val
    return net == nn_AND and count == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_2_getargs,
          testanswer = back_prop_2_testanswer,
          expected_val = "((original neural net, unchanged), 0)",
          name = 'back_prop')


#three iterations
def back_prop_4_getargs() :  #TEST 44
    return [nn_AND.copy(), {'x':3.5, 'y':-2}, 1, 1, -0.0035]
def back_prop_4_testanswer(val, original_val = None) :
    net, count = val
    return nn_AND_update_iter3.__eq__(net, 0.000000000001) and count == 3
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = back_prop_4_getargs,
          testanswer = back_prop_4_testanswer,
          expected_val = "(" + str(nn_AND_update_iter3) + ", 3)",
          name = 'back_prop')


#### Training a neural net

#ANSWER_1
ANSWER_1_getargs = 'ANSWER_1'  #TEST 45
def ANSWER_1_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 11 <= val <= 60
make_test(type = 'VALUE',
          getargs = ANSWER_1_getargs,
          testanswer = ANSWER_1_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_1_getargs)

#ANSWER_2
ANSWER_2_getargs = 'ANSWER_2'  #TEST 46
def ANSWER_2_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 11 <= val <= 60
make_test(type = 'VALUE',
          getargs = ANSWER_2_getargs,
          testanswer = ANSWER_2_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_2_getargs)

#ANSWER_3
ANSWER_3_getargs = 'ANSWER_3'  #TEST 47
def ANSWER_3_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 2 <= val <= 10
make_test(type = 'VALUE',
          getargs = ANSWER_3_getargs,
          testanswer = ANSWER_3_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_3_getargs)

#ANSWER_4
ANSWER_4_getargs = 'ANSWER_4'  #TEST 48
def ANSWER_4_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 60 <= val <= 350
make_test(type = 'VALUE',
          getargs = ANSWER_4_getargs,
          testanswer = ANSWER_4_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_4_getargs)

#ANSWER_5
ANSWER_5_getargs = 'ANSWER_5'  #TEST 49
def ANSWER_5_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, int) and 10 <= val <= 70
make_test(type = 'VALUE',
          getargs = ANSWER_5_getargs,
          testanswer = ANSWER_5_testanswer,
          expected_val = "an int in the correct range",
          name = ANSWER_5_getargs)

#ANSWER_6
ANSWER_6_getargs = 'ANSWER_6'  #TEST 50
def ANSWER_6_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val == 1
make_test(type = 'VALUE',
          getargs = ANSWER_6_getargs,
          testanswer = ANSWER_6_testanswer,
          expected_val = "an int representing the resolution",
          name = ANSWER_6_getargs)

#ANSWER_7
ANSWER_7_getargs = 'ANSWER_7'  #TEST 51
def ANSWER_7_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return isinstance(val, str) and val.lower() == 'checkerboard'
make_test(type = 'VALUE',
          getargs = ANSWER_7_getargs,
          testanswer = ANSWER_7_testanswer,
          expected_val = "the name of a dataset, as a string",
          name = ANSWER_7_getargs)

#ANSWER_8
ANSWER_8_getargs = 'ANSWER_8'  #TEST 52
def ANSWER_8_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return set([s.lower() for s in val]) == set(['small', 'medium', 'large'])
    except Exception:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_8_getargs,
          testanswer = ANSWER_8_testanswer,
          expected_val = "a list containing one or more of the strings 'small', 'medium', 'large'",
          name = ANSWER_8_getargs)

#ANSWER_9
ANSWER_9_getargs = 'ANSWER_9'  #TEST 53
def ANSWER_9_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val in list('Bb')
make_test(type = 'VALUE',
          getargs = ANSWER_9_getargs,
          testanswer = ANSWER_9_testanswer,
          expected_val = "a string ('A', 'B', 'C', or 'D')",
          name = ANSWER_9_getargs)

#ANSWER_10
ANSWER_10_getargs = 'ANSWER_10'  #TEST 54
def ANSWER_10_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    return val in list('Dd')
make_test(type = 'VALUE',
          getargs = ANSWER_10_getargs,
          testanswer = ANSWER_10_testanswer,
          expected_val = "a string ('A', 'B', 'C', 'D', or 'E')",
          name = ANSWER_10_getargs)

#ANSWER_11
ANSWER_11_getargs = 'ANSWER_11'  #TEST 55
def ANSWER_11_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return set([s.upper() for s in val]) == set('AC')
    except Exception:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_11_getargs,
          testanswer = ANSWER_11_testanswer,
          expected_val = "a list of one or more strings, selected from " + str(list('ABCD')),
          name = ANSWER_11_getargs)

#ANSWER_12
ANSWER_12_getargs = 'ANSWER_12'  #TEST 56
def ANSWER_12_testanswer(val, original_val = None):
    if val == None:
        raise NotImplementedError
    try:
        return set([s.upper() for s in val]) == set('AE')
    except Exception:
        return False
make_test(type = 'VALUE',
          getargs = ANSWER_12_getargs,
          testanswer = ANSWER_12_testanswer,
          expected_val = "a list of one or more strings, selected from " + str(list('ABCDE')),
          name = ANSWER_12_getargs)
=======
# MIT 6.034 Lab 2: Search

from tester import make_test, get_tests
from search import UndirectedGraph, Edge
from lab2 import (generic_dfs, generic_bfs, generic_hill_climbing,
                  generic_best_first, generic_branch_and_bound,
                  generic_branch_and_bound_with_heuristic,
                  generic_branch_and_bound_with_extended_set, generic_a_star,
                  is_admissible, is_consistent,
                  TEST_GENERIC_BEAM, TEST_HEURISTICS)

lab_number = 2
from read_graphs import get_graphs
all_graphs = get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']
GRAPH_FOR_HEURISTICS_TRICKY = all_graphs['GRAPH_FOR_HEURISTICS_TRICKY']

##########################################################################
### OFFLINE TESTS (HARDCODED ANSWERS)

#### PART 1: Helper Functions #########################################

make_test(type = 'FUNCTION',  #TEST 1
          getargs = [GRAPH_1, ['a', 'c', 'b', 'd']],
          testanswer = lambda val, original_val=None: val == 11,
          expected_val = 11,
          name = 'path_length')

make_test(type = 'FUNCTION',  #TEST 2
          getargs = [GRAPH_2, ['D', 'C', 'A', 'D', 'E', 'G', 'F']],
          testanswer = lambda val, original_val=None: val == 53,
          expected_val = 53,
          name = 'path_length')

make_test(type = 'FUNCTION',  #TEST 3
          getargs = [GRAPH_1, ['a']],
          testanswer = lambda val, original_val=None: val == 0,
          expected_val = 0,
          name = 'path_length')


make_test(type = 'FUNCTION',  #TEST 4
          getargs = [['node1', 'node3', 'node2']],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'has_loops')

make_test(type = 'FUNCTION',  #TEST 5
          getargs = [['d', 'a', 'c', 'a', 'b']],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'has_loops')

make_test(type = 'FUNCTION',  #TEST 6
          getargs = [list('SBCA')],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'has_loops')

make_test(type = 'FUNCTION',  #TEST 7
          getargs = [['X']],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'has_loops')


extensions_test1_answer = [['n2', 'n1'], ['n2', 'n3']]
make_test(type = 'FUNCTION',  #TEST 8
          getargs = [GRAPH_0, ['n2']],
          testanswer = lambda val, original_val=None: val == extensions_test1_answer,
          expected_val = extensions_test1_answer,
          name = 'extensions')

extensions_test2_answer = [['n2', 'n3', 'n4']]
make_test(type = 'FUNCTION',  #TEST 9
          getargs = [GRAPH_0, ['n2', 'n3']],
          testanswer = lambda val, original_val=None: val == extensions_test2_answer,
          expected_val = extensions_test2_answer,
          name = 'extensions')

extensions_test3_answer = [['S', 'A', 'C', 'E', 'D'],
                           ['S', 'A', 'C', 'E', 'F'],
                           ['S', 'A', 'C', 'E', 'G']]
make_test(type = 'FUNCTION',  #TEST 10
          getargs = [GRAPH_2, ['S', 'A', 'C', 'E']],
          testanswer = lambda val, original_val=None: val == extensions_test3_answer,
          expected_val = extensions_test3_answer,
          name = 'extensions')

# Checks intentionally-unordered neighbors in extensions
extensions_test4_graph = UndirectedGraph(list("abcdefgh"), edges=[Edge("a",l,0) for l in "hgfebcd"])
extensions_test4_answer = [["a",l] for l in "bcdefgh"]
make_test(type = 'FUNCTION',  #TEST 11
          getargs = [extensions_test4_graph, ["a"]],
          testanswer = lambda val, original_val=None: val == extensions_test4_answer,
          expected_val = extensions_test4_answer,
          name = 'extensions')

sortby_test1_answer = ['c', 'a', 'b', 'd']
make_test(type = 'FUNCTION',  #TEST 12
          getargs = [GRAPH_1, 'c', ['d', 'a', 'b', 'c']],
          testanswer = lambda val, original_val=None: val == sortby_test1_answer,
          expected_val = sortby_test1_answer,
          name = 'sort_by_heuristic')

sortby_test2_answer = ['H', 'D', 'F', 'C', 'C', 'A', 'B']
make_test(type = 'FUNCTION',  #TEST 13
          getargs = [GRAPH_2, 'G', ['D', 'C', 'B', 'H', 'A', 'F', 'C']],
          testanswer = lambda val, original_val=None: val == sortby_test2_answer,
          expected_val = sortby_test2_answer,
          name = 'sort_by_heuristic')

sortby_test3_answer = ['G', 'X', 'Y', 'F']
make_test(type = 'FUNCTION',  #TEST 14
          getargs = [GRAPH_2, 'G', ['X', 'Y', 'G', 'F']],
          testanswer = lambda val, original_val=None: val == sortby_test3_answer,
          expected_val = sortby_test3_answer,
          name = 'sort_by_heuristic')

#### PART 2: Basic Search #########################################

basic_dfs_1_answer = list('abcd')
make_test(type = 'FUNCTION',  #TEST 15
          getargs = [GRAPH_1, 'a', 'd'],
          testanswer = lambda val, original_val=None: val == basic_dfs_1_answer,
          expected_val = basic_dfs_1_answer,
          name = 'basic_dfs')

basic_dfs_2_answer = list('SACDEFG')
make_test(type = 'FUNCTION',  #TEST 16
          getargs = [GRAPH_2, 'S', 'G'],
          testanswer = lambda val, original_val=None: val == basic_dfs_2_answer,
          expected_val = basic_dfs_2_answer,
          name = 'basic_dfs')

basic_dfs_3_answer = list('HDACBY')
make_test(type = 'FUNCTION',  #TEST 17
          getargs = [GRAPH_2, 'H', 'Y'],
          testanswer = lambda val, original_val=None: val == basic_dfs_3_answer,
          expected_val = basic_dfs_3_answer,
          name = 'basic_dfs')

make_test(type = 'FUNCTION',  #TEST 18
          getargs = [GRAPH_1, 'a', 'z'],
          testanswer = lambda val, original_val=None: val == None,
          expected_val = None,
          name = 'basic_dfs')

basic_bfs_1_answer = list('abd')
make_test(type = 'FUNCTION',  #TEST 19
          getargs = [GRAPH_1, 'a', 'd'],
          testanswer = lambda val, original_val=None: val == basic_bfs_1_answer,
          expected_val = basic_bfs_1_answer,
          name = 'basic_bfs')

basic_bfs_2_answer = list('SACEG')
make_test(type = 'FUNCTION',  #TEST 20
          getargs = [GRAPH_2, 'S', 'G'],
          testanswer = lambda val, original_val=None: val == basic_bfs_2_answer,
          expected_val = basic_bfs_2_answer,
          name = 'basic_bfs')

basic_bfs_3_answer = list('HDCY')
make_test(type = 'FUNCTION',  #TEST 21
          getargs = [GRAPH_2, 'H', 'Y'],
          testanswer = lambda val, original_val=None: val == basic_bfs_3_answer,
          expected_val = basic_bfs_3_answer,
          name = 'basic_bfs')

make_test(type = 'FUNCTION',  #TEST 22
          getargs = [GRAPH_1, 'a', 'z'],
          testanswer = lambda val, original_val=None: val == None,
          expected_val = None,
          name = 'basic_bfs')

#### PART 3: Generic Search #######################################

search_args = {"dfs": generic_dfs,
               "bfs": generic_bfs,
               "hill_climbing": generic_hill_climbing,
               "best_first": generic_best_first,
               "branch_and_bound": generic_branch_and_bound,
               "branch_and_bound_with_heuristic": generic_branch_and_bound_with_heuristic,
               "branch_and_bound_with_extended_set": generic_branch_and_bound_with_extended_set,
               "a_star": generic_a_star}

# Tests 23-42
search_tests = [['dfs', GRAPH_1, 'a', 'd', 'abcd'],
                ['dfs', GRAPH_2, 'S', 'G', 'SACDEFG'],
                ['bfs', GRAPH_1, 'a', 'd', 'abd'],
                ['bfs', GRAPH_2, 'S', 'G', 'SACEG'],
                # ['hill_climbing', GRAPH_1, 'a', 'd', 'abcd'], # depends on lexicographic tie-breaking
                ['hill_climbing', GRAPH_2, 'S', 'G', 'SADHFG'],
                ['hill_climbing', GRAPH_3, 's', 'g', 'sywg'],
                # ['best_first', GRAPH_1, 'a', 'd', 'abcd'], # depends on lexicographic tie-breaking
                ['best_first', GRAPH_2, 'S', 'G', 'SADEG'],
                ['best_first', GRAPH_3, 's', 'g', 'sywg'],
                ['branch_and_bound', GRAPH_1, 'a', 'd', 'acd'],
                ['branch_and_bound', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['branch_and_bound', GRAPH_3, 's', 'g', 'sxwg'],
                ['branch_and_bound_with_heuristic', GRAPH_1, 'a', 'd', 'acd'],
                ['branch_and_bound_with_heuristic', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['branch_and_bound_with_heuristic', GRAPH_3, 's', 'g', 'szwg'],
                ['branch_and_bound_with_extended_set', GRAPH_1, 'a', 'd', 'acd'],
                ['branch_and_bound_with_extended_set', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['branch_and_bound_with_extended_set', GRAPH_3, 's', 'g', 'sxwg'],
                ['a_star', GRAPH_1, 'a', 'd', 'acd'],
                ['a_star', GRAPH_2, 'S', 'G', 'SBCEG'],
                ['a_star', GRAPH_3, 's', 'g', 'sywg']]

# Execute the tests
for arg_list in search_tests:
    if arg_list[0] != 'beam':
        (lambda method, graph, startNode, endNode, answer_string :
         make_test(type = 'NESTED_FUNCTION',
                   getargs = [search_args[method], [graph, startNode, endNode]],
                   testanswer = (lambda val, original_val=None:
                                 val == list(answer_string)),
                   expected_val = "({} search result) {}".format(method, list(answer_string)),
                   name = 'generic_search')
         )(*arg_list[:5])

bb_uses_extended_set_tests = [["generic_branch_and_bound", False],
                              ["generic_branch_and_bound_with_heuristic", False],
                              ["generic_branch_and_bound_with_extended_set", True]]
def get_bb_extended_testanswer_fn(answer):
    def bb_extended_testanswer(val, original_val=None):
        if val == [None, None, None, None]:
            raise NotImplementedError
        return val[3] == answer
    return bb_extended_testanswer

for arg_list in bb_uses_extended_set_tests:  #Tests 43-45
    (lambda method, answer :
     make_test(type = 'VALUE',
               getargs = method,
               testanswer = get_bb_extended_testanswer_fn(answer),
               expected_val = "Correct boolean value indicating whether search uses extended set",
               name = method)
     )(*arg_list)

# Checks that non-existent goal node --> no path found. 
for search_method in search_args: #Tests 46-53
    (lambda method :
        make_test(type = 'NESTED_FUNCTION',
                  getargs = [search_args[method], [GRAPH_1, 'a', 'z']],
                  testanswer = (lambda val, original_val=None: val == None),
                  expected_val = None,
                  name = "generic_search")
    )(search_method)


#### PART 4: Heuristics ###################################################

make_test(type = 'FUNCTION',  #TEST 54
          getargs = [GRAPH_1, 'd'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_admissible')

make_test(type = 'FUNCTION',  #TEST 55
          getargs = [GRAPH_1, 'c'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_admissible')

make_test(type = 'FUNCTION',  #TEST 56
          getargs = [GRAPH_2, 'G'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_admissible')

make_test(type = 'FUNCTION',  #TEST 57
          getargs = [GRAPH_3, 'g'],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'is_admissible')

test_admissible_graph = GRAPH_FOR_HEURISTICS_TRICKY.copy()
test_admissible_graph.set_heuristic({'G': {'S': 0, 'A': 10, 'B': 5, 'C': 0, 'D': 0, 'G': 0}})
make_test(type = 'FUNCTION',  #TEST 58
          getargs = [test_admissible_graph, 'G'],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = "{} (This one's tricky! How are you checking a node's admissibility?)".format(False),
          name = 'is_admissible')

make_test(type = 'FUNCTION',  #TEST 59
          getargs = [GRAPH_1, 'd'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_consistent')

make_test(type = 'FUNCTION',  #TEST 60
          getargs = [GRAPH_1, 'c'],
          testanswer = lambda val, original_val=None: val == True,
          expected_val = True,
          name = 'is_consistent')

make_test(type = 'FUNCTION',  #TEST 61
          getargs = [GRAPH_2, 'G'],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'is_consistent')

make_test(type = 'FUNCTION',  #TEST 62
          getargs = [GRAPH_3, 'g'],
          testanswer = lambda val, original_val=None: val == False,
          expected_val = False,
          name = 'is_consistent')


#### PART 5: Multiple Choice ###################################################

# British Museum gives an exhaustive listing of all rooms in 
# the house. The other three algorithms would stop after
# finding one bedroom.
ANSWER_1_getargs = "ANSWER_1"
def ANSWER_1_testanswer(val, original_val = None):
    if val == '':
        raise NotImplementedError
    return str(val) == '2'
make_test(type = 'VALUE',  #TEST 63
          getargs = ANSWER_1_getargs,
          testanswer = ANSWER_1_testanswer,
          expected_val = "correct value of ANSWER_1 ('1', '2', '3', or '4')",
          name = ANSWER_1_getargs)

# Of 1, 2, and 4, Branch and Bound with Extended Set is the 
# winner here. Having access to an extended set is a massive
# advantage when stuck in a maze; BFS would just
# continually extend redundant nodes. 
# A* is out because we don't have access to a heuristic, and
# hence it's no better than BB with Extended Set. You could
# argue that the answer could be A* with a heuristic that is
# always 0; this is a true, but the simpler answer is BB with
# Extended Set. 
ANSWER_2_getargs = "ANSWER_2"
def ANSWER_2_testanswer(val, original_val = None):
    if val == '':
        raise NotImplementedError
    return str(val) == '4'
make_test(type = 'VALUE',  #TEST 64
          getargs = ANSWER_2_getargs,
          testanswer = ANSWER_2_testanswer,
          expected_val = "correct value of ANSWER_2 ('1', '2', '3', or '4')",
          name = ANSWER_2_getargs)

# "As few towns as possible" should stick out to you. Recall 
# that BFS always gives an optimal path in terms of the number
# of nodes visited (not in terms of path length).
ANSWER_3_getargs = "ANSWER_3"
def ANSWER_3_testanswer(val, original_val = None):
    if val == '':
        raise NotImplementedError
    return str(val) == '1'
make_test(type = 'VALUE',  #TEST 65
          getargs = ANSWER_3_getargs,
          testanswer = ANSWER_3_testanswer,
          expected_val = "correct value of ANSWER_3 ('1', '2', '3', or '4')",
          name = ANSWER_3_getargs)

# A* is the clear winner, because you have access to a heuristic 
# and can remember how far you've travelled.
ANSWER_4_getargs = "ANSWER_4"
def ANSWER_4_testanswer(val, original_val = None):
    if val == '':
        raise NotImplementedError
    return str(val) == '3'
make_test(type = 'VALUE',  #TEST 66
          getargs = ANSWER_4_getargs,
          testanswer = ANSWER_4_testanswer,
          expected_val = "correct value of ANSWER_4 ('1', '2', '3', or '4')",
          name = ANSWER_4_getargs)


#### Optional tests ############################################################

beam_search_tests = [['beam', GRAPH_2, 'S', 'G', 2, 'SBYCEG'],
                     # ['beam', GRAPH_1, 'a', 'd', 2, 'abd'], #depends on lexicographic tie-breaking
                     ['beam', GRAPH_2, 'S', 'G', 1, 'SADHFG'],
                     ['beam', GRAPH_2, 'S', 'G', 3, 'SADEG']]

if TEST_GENERIC_BEAM:
    from lab2 import generic_beam, beam
    # no-path-found test for beam:
    make_test(type = 'FUNCTION',
              getargs = [GRAPH_2, 'C', 'G', 1],
              testanswer = (lambda val, original_val=None: val == None),
              expected_val = None,
              name = 'beam')

    for arg_list in beam_search_tests:
        (lambda method, graph, startNode, endNode, beam_width, answer_string :
         make_test(type = 'NESTED_FUNCTION',
                   getargs = [generic_beam,
                              [graph, startNode, endNode, beam_width]],
                   testanswer = (lambda val, original_val=None:
                                 val == list(answer_string)),
                   expected_val = list(answer_string),
                   name = 'generic_search')
         )(*arg_list[:6])


if TEST_HEURISTICS:
    from lab2 import a_star

    def test_heuristic(heuristic_dict, should_be_admissible, should_be_consistent,
                       should_be_optimal_a_star):
        if None in list(heuristic_dict['G'].values()): return False
        shortest_path = ['S', 'A', 'C', 'G']
        GRAPH_FOR_HEURISTICS.set_heuristic(heuristic_dict)
        match_adm = should_be_admissible == None or should_be_admissible == is_admissible(GRAPH_FOR_HEURISTICS, 'G')
        match_con = should_be_consistent == None or should_be_consistent == is_consistent(GRAPH_FOR_HEURISTICS, 'G')
        a_star_result = a_star(GRAPH_FOR_HEURISTICS, 'S', 'G')
        match_opt = should_be_optimal_a_star == None \
            or (should_be_optimal_a_star == (a_star_result == shortest_path))
        return match_adm and match_con and match_opt 

    make_test(type = 'VALUE',
              getargs = 'heuristic_1',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, True, None)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_1')

    make_test(type = 'VALUE',
              getargs = 'heuristic_2',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, False, None)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_2')

    make_test(type = 'VALUE',
              getargs = 'heuristic_3',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, None, False)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_3')

    make_test(type = 'VALUE',
              getargs = 'heuristic_4',
              testanswer = (lambda val, original_val=None:
                            test_heuristic(val, True, False, True)),
              expected_val = 'Correct numerical values for heuristic to fit specifications',
              name = 'heuristic_4')
>>>>>>> e1a94a6b927048e5f95b4fecaee29e64dd3928e6
