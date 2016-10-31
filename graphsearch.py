# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
	agenda = [[start]]
	for elem in agenda:
		if elem[-1]==goal:
			return elem
		for node in graph.get_connected_nodes(elem[-1]):
			agenda.append(elem+[node])
	return []

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
	agenda = [[start]]
	visited = [start]
	while agenda:
		elem = agenda[0]
		if elem[-1]==goal:
			return elem
		for node in graph.get_connected_nodes(elem[-1]):
			if not node in visited:
				visited.append(node)
				agenda.insert(0,elem+[node])
		agenda.remove(elem)
	return []

## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
	agenda = [[start]]
	while agenda:
		elem = agenda[0]
		if elem[-1]==goal:
			return elem
		temp = []
		for node in graph.get_connected_nodes(elem[-1]):
			if not node in elem:
				temp.append(elem+[node])
		agenda.remove(elem)
		temp = [(i,graph.get_heuristic(i[-1], goal)) for i in temp]
		temp = sorted(temp,key=lambda x: x[1])
		temp = [i[0] for i in temp]
		agenda = temp + agenda
	return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
	agenda = [[start]]
	toexpand = 1
	while agenda:
		while toexpand:
			elem = agenda[0]
			if elem[-1]==goal:
				return elem
			for node in graph.get_connected_nodes(elem[-1]):
				if not node in elem:
					agenda.append(elem+[node])
			agenda.remove(elem)
			toexpand-=1
		agenda = [(i,graph.get_heuristic(i[-1], goal)) for i in agenda]
		agenda = sorted(agenda,key=lambda x: x[1])
		agenda = [i[0] for i in agenda]
		agenda = agenda[:beam_width]
		toexpand = len(agenda)
	return []
## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
	length = 0
	prev = node_names[0]
	for node in node_names[1:]:
		length+=graph.get_edge(prev, node).length
		prev = node
	return length

def branch_and_bound(graph, start, goal):
	agenda = [[start]]
	while agenda:
		elem = agenda[0]
		if elem[-1]==goal:
			return elem
		for node in graph.get_connected_nodes(elem[-1]):
			if not node in elem:
				agenda.append(elem+[node])
		agenda.remove(elem)
		agenda = [(i,path_length(graph,i)) for i in agenda]
		agenda = sorted(agenda,key=lambda x: x[1])
		agenda = [i[0] for i in agenda]
	return []

def a_star(graph, start, goal):
	agenda = [[start]]
	visited = []
	while agenda:
		elem = agenda[0]
		if elem[-1]==goal:
			return elem
		if elem[-1] in visited:
			agenda.remove(elem)
		else:
			visited.append(elem[-1])
			for node in graph.get_connected_nodes(elem[-1]):
				if not node in elem:
					agenda.append(elem+[node])
			agenda.remove(elem)
			agenda = [(i,path_length(graph,i)+graph.get_heuristic(i[-1], goal)) for i in agenda]
			agenda = sorted(agenda,key=lambda x: x[1])
			agenda = [i[0] for i in agenda]
	return []

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
	for node in graph.nodes:
		if path_length(graph,branch_and_bound(graph,node,goal))<graph.get_heuristic(node,goal):
			return False
	return True

def is_consistent(graph, goal):
	for node in graph.nodes:
		for neighbour in graph.get_connected_nodes(node):
			if graph.get_heuristic(node,goal)>graph.get_edge(node, neighbour).length+graph.get_heuristic(neighbour,goal):
				return False
	return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'Searches and Graphs'
WHAT_I_FOUND_BORING = 'Multiple Choice'
