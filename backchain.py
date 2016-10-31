from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
	 match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
	tree = hypothesis
	for rule in rules:
		if not type(rule.consequent()) is str:
			for consequent in rule.consequent():
				matches = match(consequent,hypothesis)
				if (matches!=None):
					if not type(rule.antecedent()) is str:
						curtree = None
						ruletype = False
						if isinstance(rule.antecedent(), AND):
							ruletype = True
						for antecedent in rule.antecedent():
							if curtree == None:
								curtree = backchain_to_goal_tree(rules,populate(antecedent,matches))
							else:
								if ruletype:
									curtree = AND(curtree,backchain_to_goal_tree(rules,populate(antecedent,matches)))
								else:
									curtree = OR(curtree,backchain_to_goal_tree(rules,populate(antecedent,matches)))
						tree = OR(tree,curtree)
					else:
						tree = OR(tree,backchain_to_goal_tree(rules,populate(rule.antecedent(),matches)))
	tree = simplify(tree)    
	return tree

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
