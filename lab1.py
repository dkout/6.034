# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)', '(?y) beats (?z)'), THEN('(?x) beats (?z)') )

# You can test your rule by uncommenting these print statements:
#print forward_chain([transitive_rule], abc_data)
#print forward_chain([transitive_rule], poker_data)
#print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:

self=IF('person (?x)', THEN( 'self (?x) (?x)'))

sibling1 = IF( AND('parent (?x) (?y)', 'parent (?x) (?z)', NOT ('self (?z) (?y)')), THEN ('sibling (?y) (?z)'))
sibling2 = IF( AND('parent (?x) (?y)', 'parent (?x) (?z)', NOT ('self (?z) (?y)')), THEN ('sibling (?z) (?y)'))
child = IF('parent (?x) (?y)', THEN( 'child (?y) (?x)'))
cousin1 = IF(AND('parent (?x) (?y)', 'parent (?z) (?u)', 'sibling (?x) (?z)', NOT ('sibling (?y) (?u)')), THEN ('cousin (?y) (?u)'))
cousin2 = IF(AND('parent (?x) (?y)', 'parent (?z) (?u)', 'sibling (?x) (?z)', NOT ('sibling (?y) (?u)')), THEN ('cousin (?u) (?y)'))
grandparent = IF( AND( 'parent (?x) (?y)', 'parent (?z) (?x)'), THEN ('grandparent (?z) (?y)'))
grandchild = IF ('grandparent (?x) (?y)', THEN('grandchild (?y) (?x)'))

# Add your rules to this list:
family_rules = [self, child, sibling1, sibling2, cousin1, cousin2, grandparent, grandchild ]

# Uncomment this to test your data on the Simpsons family:
#print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """

    tree = OR(hypothesis)
    
    if len(rules)==0:
        return hypothesis

    for rule in rules:
        if match(rule.consequent()[0], hypothesis) is not None:
            popRule = populate(rule.antecedent(), match(rule.consequent()[0], hypothesis))
            if isinstance(popRule, (AND, OR)):
                for i in xrange(len(popRule)):
                    popRule[i]=backchain_to_goal_tree(rules, popRule[i])
                tree.append(popRule)
            else:
                new_tree=backchain_to_goal_tree(rules, popRule)
                tree.append(new_tree)
    return simplify(tree)
                    
    

# Uncomment this to run your backward chainer:
print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = 'Dimitris Koutentakis'
COLLABORATORS = 'Carl Unger'
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = 'family rules'
WHAT_I_FOUND_BORING = 'backward chaining was hard to implement'
SUGGESTIONS = 'None'


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
