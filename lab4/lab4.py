# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"

    for element in csp.domains.values():
        if not element:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    # for constraint in csp.constraints:
    #     if csp.get_assigned_value(constraint.var1) != None and csp.get_assigned_value(constraint.var2) != None:
    #         if not constraint.check(csp.get_assigned_value(constraint.var1), csp.get_assigned_value(constraint.var2)):
    #             return False
    # return True
    for element in csp.constraints:
        c1=csp.get_assigned_value(element.var1)
        c2=csp.get_assigned_value(element.var2)
        if not (c1==None or c2==None):
            if not element.check(c1,c2):
                return False
    return True
#TODO:
def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""
    counter=0
    queue=[problem]
    while len(queue)>0:
        newprob=queue.pop(0)
        counter+=1
        if not has_empty_domains(newprob) and check_all_constraints(newprob):

            if len(newprob.unassigned_vars)==0:
                return (newprob.assigned_values,counter)
            newlist=[]
            b=newprob.pop_next_unassigned_var()
            for i in newprob.get_domain(b):
                newlist.append(newprob.copy().set_assigned_value(b, i))
            queue=(newlist + queue)
    return (None, counter)


#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""
    valid=set()

    nog=csp.get_neighbors(var)

    for neighbor in nog:
        for nvalue in list(csp.get_domain(neighbor)):
            countv=0
            for val in list(csp.get_domain(var)):
                for constraint in csp.constraints_between(neighbor, var):
                    if not constraint.check(nvalue,val):
                        countv+=1
                        #innest loop here

            #start if statement

            if countv==len(csp.domains[var]):
                csp.eliminate(neighbor, nvalue)
                #print ("eliminating ", val, " from ", neighbor)
                if  len(csp.domains[neighbor])==0:
                    return None
                valid.add(neighbor)
                #enq

    return sorted(list(valid))



def domain_reduction(csp, queue=None) :

    if queue is None:
        queue = list(csp.variables)

    q2=list()

    while queue:
        iteration = queue.pop(0)
        q2.append(iteration)
        nextval = eliminate_from_neighbors(csp, iteration)

##
        if nextval== None:
            return None


        for j in nextval:
            if j not in queue:
                queue.append(j)

    return q2

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?




ANSWER_1 = solve_constraint_dfs(get_pokemon_problem())[1]

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?
extensionproblem= get_pokemon_problem()
domain_reduction(extensionproblem)


ANSWER_2 = solve_constraint_dfs(extensionproblem)[1]


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :

    counter=0
    queue=[problem]
    while len(queue)>0:
        newprob=queue.pop(0)
        counter+=1
        if not has_empty_domains(newprob) and check_all_constraints(newprob):

            if len(newprob.unassigned_vars)==0:
                return (newprob.assigned_values,counter)
            newlist=[]
            b=newprob.pop_next_unassigned_var()
            for i in newprob.get_domain(b):
                newcsp=newprob.copy().set_assigned_value(b, i)

                domain_reduction(newcsp, [b])
                newlist.append(newcsp)
            queue=(newlist + queue)
    return (None, counter)


# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)

ANSWER_3 = solve_constraint_propagate_reduced_domains(get_pokemon_problem())[1]


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
            if queue is None:
                queue = list(csp.variables)

            q2=list()

            while queue:
                iteration = queue.pop(0)
                q2.append(iteration)
                nextval = eliminate_from_neighbors(csp, iteration)


                if nextval== None:
                    return None


                for j in nextval:
                    if len(csp.domains[j])==1:

                        if j not in queue:
                            queue.append(j)

            return q2

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""


# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)

    counter=0
    queue=[problem]
    while len(queue)>0:
        newprob=queue.pop(0)
        counter+=1
        if not has_empty_domains(newprob) and check_all_constraints(newprob):

            if len(newprob.unassigned_vars)==0:
                return (newprob.assigned_values,counter)
            newlist=[]
            b=newprob.pop_next_unassigned_var()
            for i in newprob.get_domain(b):
                newcsp=newprob.copy().set_assigned_value(b, i)

                domain_reduction_singleton_domains(newcsp, [b])
                newlist.append(newcsp)
            queue=(newlist + queue)
    return (None, counter)

ANSWER_4 = solve_constraint_propagate_singleton_domains(get_pokemon_problem())[1]


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    if queue is None:
        queue = list(csp.variables)

    q2=list()

    while queue:
        iteration = queue.pop(0)
        q2.append(iteration)
        nextval = eliminate_from_neighbors(csp, iteration)


        if nextval== None:
            return None


        for j in nextval:
            if enqueue_condition_fn(csp,j):

                if j not in queue:
                    queue.append(j)

    return q2


def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var))==1

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :

    counter=0
    queue=[problem]
    while len(queue)>0:
        newprob=queue.pop(0)
        counter+=1
        if not has_empty_domains(newprob) and check_all_constraints(newprob):

            if len(newprob.unassigned_vars)==0:
                return (newprob.assigned_values,counter)
            newlist=[]
            b=newprob.pop_next_unassigned_var()
            for i in newprob.get_domain(b):
                newcsp=newprob.copy().set_assigned_value(b, i)

                if enqueue_condition != None:
                    propagate(enqueue_condition, newcsp, [b])
                newlist.append(newcsp)
            queue=(newlist + queue)
    return (None, counter)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)

ANSWER_5 = solve_constraint_generic(get_pokemon_problem(), condition_forward_checking)[1]


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m-n)==1

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return not constraint_adjacent(m,n)

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints=list()

    number = len(variables)
    for i in range(number):
        #first loop

        for j in range(i+1,number):
                #second loop
            appendition =   Constraint(variables[i],variables[j],constraint_different)
            constraints.append(appendition)


    return sorted(list(constraints))

#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = 'Dimitris Koutentakis'
COLLABORATORS = 'Carl Unger'
HOW_MANY_HOURS_THIS_LAB_TOOK = 12
WHAT_I_FOUND_INTERESTING = 'constraint propagation'
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = 'shorter labs :)'


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
