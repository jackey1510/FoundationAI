import sys
import random
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
		self.state = state
		self.parent = parent
		self.move = move
		self.depth = depth
		self.heuristic = heuristic #Heuristic estimated cost
	def __repr__(self):
                return repr((self.state, self.parent, self.move, self.depth, self.heuristic))
	
def expand(node, goal):
	expanded_nodes = []
	up = move_up( node.state )
	down = move_down( node.state )
	left = move_left( node.state )
	right = move_right( node.state )
	if up:
		expanded_nodes.append( Node( up, node, "up", node.depth + 1, node.depth + 1 + heuristic( up, goal) ) )
	if down:
		expanded_nodes.append( Node( down, node, "down", node.depth + 1, node.depth + 1 + heuristic( down, goal) ) )
	if left:
		expanded_nodes.append( Node( left, node, "left", node.depth + 1, node.depth + 1 + heuristic( left, goal) ) )
	if right:
		expanded_nodes.append( Node( right, node, "right", node.depth + 1, node.depth + 1 + heuristic( right, goal) ) )
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

def getNextMove(agent):
	moves={0:"up",1:"down",2:"left",3:"right"}
	rng=random.randint(0,3)
	while (rng==0 and (agent in [0, 1, 2, 3])) or (rng==1 and (agent in [12, 13, 14, 15])) or (rng==2 and (agent in [0, 4, 8, 12])) or (rng==3 and (agent in [3, 7, 11, 15])) :#Only moves within the boundaries
		rng=random.randint(0,3)
	return(moves[rng]) 

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
		
def dfs(start, goal):
	state = start
	moveCount = 0
	moveList = list()
	print 'start'
	display_board(state)
	while not is_goal(state,goal):
		#for i in xrange(100):
		nextMove=getNextMove(state.index('@'))
		#print nextMove
		moveList.append(nextMove)
		if nextMove=="up":
			state=move_up(state)	
		if nextMove=="down":
			state=move_down(state)
		if nextMove=="left":
			state=move_left(state)
		if nextMove=="right":
			state=move_right(state)
		#state = move(state,nextMove)
		#print "After"
		#display_board(state)
		moveCount+=1
	display_board(state)
	print('Total '+str(moveCount)+' steps')
	print('Nodes expanded: '+str(moveCount))
	
def bfs(start, goal):
	"""Performs a breadth first search from the start state to the goal"""
	# A list (can act as a queue) for the nodes.
	nodes = []
	count = 0
	visited = 0
	# Create the queue with the root node in it.
	nodes.append( Node( start, None, None, 0, heuristic(start, goal) ) )
	print 'Start'
	display_board(start)
	while True:
		# We've run out of states, no solution.
		if len( nodes ) == 0: return None
		for i in xrange( len(nodes) ):
			if is_goal(nodes[i].state, goal):
				print('Goal! The search depth is '+str(nodes[i].depth))
				print('Nodes expanded:' + str(count))
				print('Nodes visited: ' + str(visited))
				display_board(nodes[i].state)
				moves = []
				temp = nodes[i]
				while True:
					moves.insert(0, temp.move)
					if temp.depth == 1: 
						break
					temp = temp.parent
				return moves
		expanded_nodes = []
		while len(nodes) > 0:
			node = nodes.pop(0)
			expanded_nodes.extend(expand( node, goal ))
			visited += 1
			if count%100000 == 0:
				print ('No.of nodes expanded: '+str(count))
			#display_board(node.state)
		count += len(expanded_nodes)
		nodes.extend( expanded_nodes )
			
def ids(start, goal):
	"""Performs a breadth first search from the start state to the goal"""
	# A list (can act as a queue) for the nodes.
	nodes = []
	count = 0
	visited = 0
	depth_limit = 0
	print 'Start'
	# Create the queue with the root node in it.
	nodes.append( Node( start, None, None, 0, heuristic(start, goal) ) )
	while True:
		for i in xrange( len(nodes) ):
			if is_goal(nodes[i].state, goal):
				print('Goal! The search depth is '+str(nodes[i].depth))
				print('Nodes expanded:' + str(count))
				print('Nodes visited: ' + str(visited))
				#print(nodes[1].state)
				display_board(nodes[i].state)
				moves = []
				temp = nodes[i]
				while True:
					moves.insert(0, temp.move)
					if temp.depth == 1: 
						break
					temp = temp.parent
				return moves				
			# Expand the node and add all the expansions to the front of the stack
				# take the node from the front of the queue				
		# Expand the node and add all the expansions to the front of the stack
		expanded_nodes = []
		while len(nodes)>0:
			node = nodes.pop(0)
			if node.depth < depth_limit:
				expanded_nodes.extend(expand( node, goal ))
				visited += 1
		expanded_nodes.extend( nodes )
		count += len(expanded_nodes)
		nodes = expanded_nodes
			
		# We've run out of states, no solution.
		# Increse depth_limit
		if len(nodes) == 0:
			depth_limit += 1
			count = 0
			#print('Searching depth '+str(depth_limit))
			nodes.append( Node( start, None, None, 0, heuristic(start, goal) ) )

def astar(start, goal):
	nodes = []
	count = 0
	visited = 0
	# Create the queue with the root node in it.
	nodes.append( Node( start, None, None, 0, heuristic(start, goal) ) )
	print 'Start'
	display_board( start )
	while True:
		# We've run out of states, no solution.
		if len( nodes ) == 0: return None
		# Append the move we made to moves
		# if this node is the goal, return the moves it took to get here.
		for i in xrange( len(nodes) ):
			if is_goal(nodes[i].state, goal):
				print('Goal! The search depth is '+str(nodes[i].depth))
				print('Nodes expanded:' + str(count))
				print('Nodes visited: ' + str(visited))
				display_board(nodes[i].state)
				moves = []
				temp = nodes[i]
				while True:
					moves.insert(0, temp.move)
					if temp.depth == 1: 
						break
					temp = temp.parent
				return moves				
			# Expand the node and add all the expansions to the front of the stack
				# take the node from the front of the queue
		expanded_nodes = []
		node = nodes.pop(nodes.index(min(nodes, key = attrgetter('heuristic'))))
		expanded_nodes.extend(expand( node, goal ))
		visited += 1
		count += len( expanded_nodes )
		nodes.extend( expanded_nodes )
			
def heuristic(state, goal): #Sum of the Manhattan Distance between A B C in the current state and the goal
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
	print ('Performing depth first search')
	print(dfs(start, goal))
	print ('Performing breadth first search')
	print(bfs(start, goal))
	print('\n\n\n')
	print ('Iterative deepening search')
	print(ids(start, goal))
	print('\n\n\n')
	print ('A* search')
	print(astar(start, goal))
	

if __name__ == "__main__":
	main();
	
	
	

		

	


		

		
