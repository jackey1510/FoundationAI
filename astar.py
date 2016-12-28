import sys
from operator import attrgetter

"""
Start State (@ is the agent)
-----------------
|   |   | A |   |
-----------------
|   |   |   |   |
-----------------
| B |   |   |   |
-----------------
|   | C |   | @ |
-----------------

Goal State
-----------------
|   |   |   |   |
-----------------
|   | A |   |   |
-----------------
|   | B |   |   |
-----------------
|   | C |   |   | (agent can be anywhere)
-----------------
"""

class Node:
	def __init__(self, state, parent, move, depth, heuristic):
		# Contains the state of the node
		self.state = state
		# Contains the node that generated this node
		self.parent = parent
		# Contains the operation that generated this node from the parent
		self.move = move
		# Contains the depth of this node (parent.depth +1)
		self.depth = depth
		self.heuristic = heuristic
	#def __repr__(self):
                #return repr((self.state, self.parent, self.move, self.depth, self.heuristic))
				
def create_node(state, parent, move, depth, heuristic):
	return Node(state, parent, move, depth, heuristic)
	
def expand_node(node, goal):
	expanded_nodes = []
	up = move_up( node.state )
	down = move_down( node.state )
	left = move_left( node.state )
	right = move_right( node.state )
	if up:
		expanded_nodes.append( create_node( up, node, "up", node.depth + 1, node.depth + 1 + heuristic( up, goal) ) )
	if down:
		expanded_nodes.append( create_node( down, node, "down", node.depth + 1, node.depth + 1 + heuristic( down, goal) ) )
	if left:
		expanded_nodes.append( create_node( left, node, "left", node.depth + 1, node.depth + 1 + heuristic( left, goal) ) )
	if right:
		expanded_nodes.append( create_node( right, node, "right", node.depth + 1, node.depth + 1 + heuristic( right, goal) ) )
	# Filter the list and remove the nodes that are impossible (move function returned None)
	expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
	return expanded_nodes

def display_board(state):
	print "-----------------"
	print "| {} | {} | {} | {} |".format(state[0], state[1], state[2], state[3])
	print "-----------------"
	print "| {} | {} | {} | {} |".format(state[4], state[5], state[6], state[7])
	print "-----------------"
	print "| {} | {} | {} | {} |".format(state[8], state[9], state[10], state[11])
	print "-----------------"
	print "| {} | {} | {} | {} |".format(state[12], state[13], state[14], state[15])
	print "-----------------"

def move_up(state):
	"""Moves the       tile up on the board. Returns a new state as a list."""
	# Perform an object copy
	new_state = state[:]
	index = new_state.index( '@' )
	# Sanity check
	if index not in [0, 1, 2, 3]:
		# Swap the values.
		temp = new_state[index - 4]
		new_state[index - 4] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None (Pythons NULL)
		return None

def move_down(state):
	"""Moves the       tile down on the board. Returns a new state as a list."""
	# Perform object copy
	new_state = state[:]
	index = new_state.index( '@' )
	# Sanity check
	if index not in [12, 13, 14, 15]:
		# Swap the values.
		temp = new_state[index + 4]
		new_state[index + 4] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None.
		return None

def move_left(state):
	"""Moves the       tile left on the board. Returns a new state as a list."""
	new_state = state[:]
	index = new_state.index( '@' )
	# Sanity check
	if index not in [0, 4, 8, 12]:
		# Swap the values.
		temp = new_state[index - 1]
		new_state[index - 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move it, return None
		return None

def move_right(state):
	"""Moves the       tile right on the board. Returns a new state as a list."""
	# Performs an object copy. Python passes by reference.
	new_state = state[:]
	index = new_state.index( '@' )
	# Sanity check
	if index not in [3, 7, 11, 15]:
		# Swap the values.
		temp = new_state[index + 1]
		new_state[index + 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None
		return None
		
def is_goal(state, goal):
	#print (str(state.index('A'))+','+str(state.index('B'))+','+str(state.index('C')))
	if state[goal['A']]=='A' and state[goal['B']]=='B' and state[goal['C']]=='C':
		return True
	else:
		return False

def astar(start, goal):
	"""Performs a breadth first search from the start state to the goal"""
	# A list (can act as a queue) for the nodes.
	nodes = []
	count = 0
	visited = 0
	# Create the queue with the root node in it.
	nodes.append( create_node( start, None, None, 0, heuristic(start, goal) ) )
	print 'Start'
	while True:
		
		# We've run out of states, no solution.
		if len( nodes ) == 0: return None
		# take the node with the least heuristic value
		node = nodes.pop(nodes.index(min(nodes, key = attrgetter('heuristic'))))
		if count%1000 == 0:
			print ('No.of nodes expanded: '+str(count))
			#display_board(node.state)
		# Append the move we made to moves
		# if this node is the goal, return the moves it took to get here.
		
		if is_goal(node.state, goal):
			print('Goal! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			display_board(node.state)
			moves = []
			temp = node
			while True:
				moves.insert(0, temp.move)
				if temp.depth == 1: 
					break
				temp = temp.parent
			return moves			
		# Expand the node and add all the expansions to the front of the stack
		else:
			expanded_nodes = expand_node( node, goal )
			nodes.extend( expanded_nodes )
			#nodes = sorted( nodes, key=attrgetter('heuristic','depth'))
			visited += 1
			count += len(expanded_nodes)
			
def heuristic(state, goal):
	if state != None:
		A = state.index('A')
		B = state.index('B')
		C = state.index('C')
		dist = abs(A%4-goal['A']%4)+abs(A/4-goal['A']/4)+abs(B%4-goal['B']%4)+abs(B/4-goal['B']/4)+abs(C%4-goal['C']%4)+abs(C/4-goal['C']/4)
		return dist
	else:
		return None
		
def main():
	start = [' ',' ','A',' ',' ',' ',' ',' ','B',' ',' ',' ',' ','C',' ','@']
	test = [' ',' ',' ',' ',' ',' ',' ',' ','B',' ',' ','A',' ','C',' ','@']
	goal = {'A':5, 'B':9, 'C':13}
	hard_start = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A','B','C','@']
	print ('Performing breadth first search')
	#print(bfs(start, goal))
	print('\n\n\n')
	print ('Iterative deepening search')
	#print(ids(start, goal))
	print('\n\n\n')
	print ('A* search')
	print(astar(start, goal))
	#print heuristic(test,goal)
	

if __name__ == "__main__":
	main();