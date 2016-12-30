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
	up = move(node.state, 'up')
	down = move(node.state, 'down')
	left = move(node.state, 'left')
	right = move(node.state, 'right')
	new_depth = node.depth + 1
	if up:
		expanded_nodes.append(Node(up, node, "up", new_depth, new_depth + heuristic( up, goal)))
	if down:
		expanded_nodes.append(Node(down, node, "down", new_depth, new_depth + heuristic( down, goal)))
	if left:
		expanded_nodes.append(Node(left, node, "left", new_depth, new_depth + heuristic( left, goal)))
	if right:
		expanded_nodes.append(Node(right, node, "right", new_depth, new_depth + heuristic( right, goal)))
	return expanded_nodes

def display(state):
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
	
def move(state, direction):
	new_state = state[:]
	index = new_state.index( '@' )
	if direction == 'up':
		if index not in [0, 1, 2, 3]: # Can't go up
			temp = new_state[index - 4]
			new_state[index - 4] = new_state[index]
			new_state[index] = temp
			return new_state
		else:
			return None
	if direction == 'down':
		if index not in [12, 13, 14, 15]: # Can't go down
			temp = new_state[index + 4]
			new_state[index + 4] = new_state[index]
			new_state[index] = temp
			return new_state
		else:
			return None
	if direction == 'left':
		if index not in [0, 4, 8, 12]: # Can't go left
			temp = new_state[index - 1]
			new_state[index - 1] = new_state[index]
			new_state[index] = temp
			return new_state
		else:
			return None
	if direction == 'right':
		if index not in [3, 7, 11, 15]: # Can't go right
			temp = new_state[index + 1]
			new_state[index + 1] = new_state[index]
			new_state[index] = temp
			return new_state
		else:
			return None
		
def is_goal(state, goal):
	if state[goal['A']]=='A' and state[goal['B']]=='B' and state[goal['C']]=='C':
		return True
	else:
		return False	

def solution(node):
	moves = []
	temp = node
	while True:
		moves.insert(0, temp.move)
		if temp.depth == 1: 
			break
		temp = temp.parent
	return moves
		
def dfs_random(start, goal):
	state = start
	moveCount = 0
	moveList = list()
	print 'start'
	display(state)
	while not is_goal(state,goal):
		nextMove=getNextMove(state.index('@'))
		moveList.append(nextMove)
		state=move(state,nextMove)
		moveCount+=1
	display(state)
	print('Total '+str(moveCount)+' steps')
	print('Nodes expanded: '+str(moveCount))
	return moveList
	
def dfs_limit(start,goal, depth_limit):
	nodes = [] # Node queue
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	nodes.append(Node(start, None, None, 0, heuristic(start, goal))) # Root
	print 'Start'
	display(start)
	while True:
		if len(nodes) == 0: return None #No solution
		node = nodes.pop(0) #Pop the first node
		visited += 1
		if is_goal(node.state, goal):
			print('Goal! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			display(node.state)
			return solution(node)				
		expanded_nodes = []
		if node.depth < depth_limit: #Expand only if the node is less than the depth limit
			expanded_nodes.extend(expand(node, goal))# expand
			expanded_nodes.extend(nodes) #put the nodes in the front of the queue
			nodes = expanded_nodes 			
			count += len(expanded_nodes)
			
def bfs(start, goal):
	nodes = [] # Node queue
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	nodes.append(Node(start, None, None, 0, heuristic(start, goal))) # Root
	print 'Start'
	display(start)
	while True:
		if len(nodes) == 0: return None #No solution
		for i in xrange(len(nodes)): # Check if there is solution in the nodes
			if is_goal(nodes[i].state, goal):
				print('Goal! The search depth is '+str(nodes[i].depth))
				print('Nodes expanded:' + str(count))
				print('Nodes visited: ' + str(visited))
				display(nodes[i].state)
				return solution(nodes[i])
		expanded_nodes = []
		while len(nodes) > 0: # Pop and expand until there is no nodes
			node = nodes.pop(0)
			expanded_nodes.extend(expand( node, goal ))
			visited += 1
			#display(node.state)
		count += len(expanded_nodes)
		nodes.extend( expanded_nodes )
			
def ids(start, goal):
	nodes = [] # Node queue
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	depth_limit = 0
	print 'Start'
	nodes.append(Node(start, None, None, 0, heuristic(start, goal))) # Root
	while True:
		for i in xrange(len(nodes)): # Check if there is solution in the nodes
			if is_goal(nodes[i].state, goal):
				print('Goal! The search depth is '+str(nodes[i].depth))
				print('Nodes expanded:' + str(count))
				print('Nodes visited: ' + str(visited))
				display(nodes[i].state)
				return solution(nodes[i])				
		expanded_nodes = []
		while len(nodes)> 0: # Pop and expand until there is no nodes
			node = nodes.pop(0)
			if node.depth < depth_limit:
				expanded_nodes.extend(expand( node, goal ))
				visited += 1
		expanded_nodes.extend( nodes )
		count += len(expanded_nodes)
		nodes = expanded_nodes
		if len(nodes) == 0:  # No solution. Increse depth_limit
			depth_limit += 1
			#count = 0
			#print('Searching depth '+str(depth_limit))
			nodes.append(Node(start, None, None, 0, heuristic(start, goal))) # Root

def astar(start, goal):
	nodes = [] # Node queue
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	nodes.append(Node(start, None, None, 0, heuristic(start, goal))) # Root
	print 'Start'
	display( start )
	"""while True:
		if len(nodes) == 0: return None
		for i in xrange(len(nodes)): # Check if there is solution in the nodes
			if is_goal(nodes[i].state, goal):
				print('Goal! The search depth is '+str(nodes[i].depth))
				print('Nodes expanded:' + str(count))
				print('Nodes visited: ' + str(visited))
				display(nodes[i].state)
				return solution(nodes[i])				
		expanded_nodes = []
		node = nodes.pop(nodes.index(min(nodes, key = attrgetter('heuristic')))) # Pop and expand the node with the best heuristic estimated cost
		expanded_nodes.extend(expand(node, goal))
		visited += 1
		count += len(expanded_nodes)
		nodes.extend(expanded_nodes)"""
	while True:
		if len(nodes) == 0: return None
		node = nodes.pop(nodes.index(min(nodes, key = attrgetter('heuristic')))) # Pop and expand the node with the best heuristic estimated cost
		visited += 1
		if is_goal(node.state, goal): #check if the node poped is the goal
			print('Goal! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			display(node.state)
			return solution(node)				
		expanded_nodes = []
		expanded_nodes.extend(expand(node, goal)) #expand
		count += len(expanded_nodes)
		nodes.extend(expanded_nodes)# Add the expanded node at the back of the queue
			
def heuristic(state, goal): #Sum of the Manhattan Distance between A B C in the current state and that in the goal state
	if state:
		A = state.index('A')
		B = state.index('B')
		C = state.index('C')
		dist = abs(A%4-goal['A']%4)+abs(A/4-goal['A']/4)+abs(B%4-goal['B']%4)+abs(B/4-goal['B']/4)+abs(C%4-goal['C']%4)+abs(C/4-goal['C']/4)
		return dist
	else:
		return None
		
def solution_check(start, goal, solution):
	if solution:
		state = start
		for i in xrange(len(solution)):
			state = move(state, solution[i])	
		if is_goal(state,goal):
			print ('The solution is correct')
		else:
			print ('The solution is wrong')
	else:
		print('No solution')
	return False
		
		
		
def main():
	#start = [' ',' ',' ',' ',' ','A',' ',' ','B',' ',' ',' ',' ','C',' ','@'] # easy
	#start = [' ',' ','A',' ',' ',' ',' ',' ','B',' ',' ',' ',' ','C',' ','@'] # intermediate
	start = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A','B','C','@'] # hard
	goal = {'A':5, 'B':9, 'C':13}
	print ('Randomized depth first search')
	solution=(dfs_random(start, goal))
	print ('Solution Checking')
	solution_check(start, goal, solution)
	print('\n')
	solution=(dfs_limit(start, goal, 12))
	print solution
	print ('Solution Checking')
	solution_check(start, goal, solution)
	print('\n')
	print ('Performing breadth first search')
	solution=(bfs(start, goal))
	print solution
	print ('Solution Checking')
	solution_check(start, goal, solution)
	print('\n')
	print ('Iterative deepening search')
	solution=(ids(start, goal))
	print solution
	print ('Solution Checking')
	solution_check(start, goal, solution)
	print('\n')
	print ('A* search')
	solution=(astar(start, goal))
	print solution
	print ('Solution Checking')
	solution_check(start, goal, solution)
	

if __name__ == "__main__":
	main();
	
	
	

		

	


		

		
