# MIT 6.034 Lab 6: Neural Nets
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), Jake Barnwell (jb16), and 6.034 staff

from nn_problems import *
from math import e
INF = float('inf')

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    if x >= threshold:
        return 1
    else:
        return 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1.0/(1+e**(-steepness*(x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    if x<0:
        return 0
    else:
        return x

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -0.5*(desired_output-actual_output)**2
# Forward propagation

def node_value(node, input_values, neuron_outputs):  # STAFF PROVIDED
    """Given a node, a dictionary mapping input names to their values, and a
    dictionary mapping neuron names to their outputs, returns the output value
    of the node."""
    if isinstance(node, basestring):
        return input_values[node] if node in input_values else neuron_outputs[node]
    return node  # constant input, such as -1

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""

    mapdic=dict()
    sortedNet=net.topological_sort()
    for node in sortedNet:
        s=0
        neighborsIn=net.get_incoming_neighbors(node)
        for neighbor in neighborsIn:
            value=node_value(neighbor, input_values, mapdic)
            edge_weight=net.get_wires(neighbor, node)[0].weight
            s+=value*edge_weight
        output=float(threshold_fn(s))
        input_values[node]=output
        mapdic[node]=output
    ans=(mapdic[sortedNet[-1]],mapdic)
    return ans

# Backward propagation warm-up
def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    compare=-INF
    for action in [0, step_size, -step_size]:
        a=inputs[0]+action
        for action2 in [0, step_size, -step_size]:
            b=inputs[1]+action2
            for action3 in [0, step_size, -step_size]:
                c=inputs[2]+action3
                out=func(a,b,c)
                if out>compare:
                    currentBest=[a,b,c]
                    compare=out
    return (compare,currentBest)

def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    nodes=[]
    nodes.append(wire.endNode)
    output=set()
    while not len(nodes)==0:
        neighborsOut=net.get_outgoing_neighbors(nodes[0])
        node = nodes.pop(0)
        output.add(node)
        if net.is_output_neuron(node):
            output.add(wire)
            output.add(wire.startNode)
        else:
            for neighbor in neighborsOut:
                nodes.append(neighbor)
                output.add(neighbor)
                output.add(net.get_wires(node,neighbor)[0])
    return output
# Backward propagation
def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    mapdic = {}
    net_s = net.topological_sort()
    for node in reversed(net_s):
        if net.is_output_neuron(node):
            mapdic[node] = float((neuron_outputs[node]) *(1 - neuron_outputs[node]) * (desired_output - neuron_outputs[node]))
        else:
            sum = 0
            for wire in net.get_wires(node):
                weight = wire.get_weight()
                sum+= weight*mapdic[wire.endNode]
            mapdic[node] = float((neuron_outputs[node]) * (1-neuron_outputs[node]) *(sum))
    return mapdic

def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""
    wires=net.get_wires()
    deltas=calculate_deltas(net,desired_output,neuron_outputs)
    for wire in wires:
        sn = wire.startNode
        en = wire.endNode
        if sn in set(net.inputs) and sn in input_values:
            wire.set_weight(wire.get_weight() + r*input_values[sn]*deltas[en])
        elif sn not in neuron_outputs:
            wire.set_weight(wire.get_weight() + r*wire.startNode*deltas[en])
        else:
            wire.set_weight(wire.get_weight() + r*neuron_outputs[sn]*deltas[en])
    return net

def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    counter=0
    (f, out) = forward_prop(net, input_values, sigmoid)
    while accuracy(desired_output, f) <= minimum_accuracy:

        update_weights(net, input_values, desired_output, out, r)
        (f, out) = forward_prop(net, input_values, sigmoid)
        counter += 1
    return (net, counter)



# Training a neural net

ANSWER_1 = 20
ANSWER_2 = 35
ANSWER_3 = 10
ANSWER_4 = 150
ANSWER_5 = 63

ANSWER_6 = 1
ANSWER_7 = 'checkerboard'
ANSWER_8 = ['small','medium','large']
ANSWER_9 = 'b'

ANSWER_10 = 'd'
ANSWER_11 = 'AC'
ANSWER_12 = 'AE'


#### SURVEY ####################################################################

NAME = 'Dimitris Koutentakis'
COLLABORATORS = 'Luana Lopes Lara, Carl Unger'
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
