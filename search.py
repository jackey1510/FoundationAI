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
	def __init__(self, name, state, parent, move, depth, heuristic):
		self.name = name
		self.state = state
		self.parent = parent
		self.move = move
		self.depth = depth
		self.heuristic = heuristic # Estimated cost
	def __repr__(self):
		return repr((self.name, self.state, self.parent, self.move, self.depth, self.heuristic))
	
def expand(node, goal):
	expanded_nodes = []
	up = move(node.state, 'up')
	down = move(node.state, 'down')
	left = move(node.state, 'left')
	right = move(node.state, 'right')
	new_depth = node.depth + 1
	new_name = node.name
	
	if up:
		expanded_nodes.append(Node(new_name+'.u', up, node, "up", new_depth, new_depth + heuristic( up, goal)))
	if down:
		expanded_nodes.append(Node(new_name+'.down', down, node, "down", new_depth, new_depth + heuristic( down, goal)))
	if left:
		expanded_nodes.append(Node(new_name+'.left', left, node, "left", new_depth, new_depth + heuristic( left, goal)))
	if right:
		expanded_nodes.append(Node(new_name+'.right', right, node, "right", new_depth, new_depth + heuristic( right, goal)))
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
	return True

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
	while temp.move:
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
	order = ['root'] # visiting order
	while not is_goal(state,goal):
		nextMove=getNextMove(state.index('@'))
		#order.append(order[len(order)-1]+'.'+nextMove)
		moveList.append(nextMove)
		state=move(state,nextMove)
		moveCount+=1
	print('End')
	display(state)
	print ('Goal! The search Depth is: '+str(moveCount))
	print('Total '+str(moveCount)+' steps')
	print('Nodes expanded: '+str(moveCount))
	print ('Solution Checking')
	if solution_check(start, goal, moveList):
		#print('The first 10 visiting order is: ')
		#for i in xrange(10):
			#print(order[i])
		#return moveList
		return moveCount
	
def dfs_limit(start,goal, depth_limit):
	nodes = [] # Node stack
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	order = [] # pop order
	nodes.append(Node('root', start, None, None, 0, heuristic(start, goal))) # Root
	print 'Start'
	display(start)
	while True:
		if len(nodes) == 0: 
			print('No solution! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			print('The search order is:')
			print(order)
			return None #No solution
		node = nodes.pop() #Pop the top node
		order.append(node.name) # Record the visiting order
		visited += 1
		if is_goal(node.state, goal):
			print('End')
			display(node.state)
			print('Goal! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			#print('The search order is:')
			#print(order)
			moves=solution(node)
			print ('Solution Checking')
			if solution_check(start, goal, moves):
				return moves			
		expanded_nodes = []
		if node.depth < depth_limit: #Expand only if the node is less than the depth limit
			expanded_nodes = (expand(node, goal))# expand
			nodes.extend(expanded_nodes) #put the expanded node at the top of the stack
			#nodes = expanded_nodes 			
			count += len(expanded_nodes)
			
def bfs(start, goal):
	nodes = [] # Node queue
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	order = [] # pop order
	nodes.append(Node('root', start, None, None, 0, heuristic(start, goal))) # Root
	print 'Start'
	display(start)
	while True:
		if len(nodes) == 0: 
			print('No solution! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			print('The search order is:')
			print(order)
			return None #No solution
		for i in xrange(len(nodes)): # Check if there is solution in the nodes
			order.append(nodes[i].name) # Record the visiting order
			visited += 1
			if is_goal(nodes[i].state, goal):
				print('End')
				display(nodes[i].state)
				print('Goal! The search depth is '+str(nodes[i].depth))
				print('Nodes expanded:' + str(count))
				print('Nodes visited: ' + str(visited))
				#print('The search order is:')
				#print(order)
				moves=solution(nodes[i])
				print ('Solution Checking')
				if solution_check(start, goal, moves):
					return moves
		expanded_nodes = []
		while len(nodes) > 0: # Pop and expand until there is no nodes
			node = nodes.pop(0)
			expanded_nodes.extend(expand( node, goal ))
			#display(node.state)
		count += len(expanded_nodes)
		nodes.extend( expanded_nodes )
			
def ids(start, goal):
	nodes = [] # Node stack
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	depth_limit = 1
	order = [] # pop order
	nodes.append(Node('root', start, None, None, 0, heuristic(start, goal))) # Root
	print 'Start'
	display(start)
	while True:
		node = nodes.pop() #Pop the top node
		order.append(node.name) # Record the visiting order
		visited += 1
		if is_goal(node.state, goal):
			print('End')
			display(node.state)
			print('Goal! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			#print('The search order is:')
			#print(order)
			moves=solution(node)
			print ('Solution Checking')
			if solution_check(start, goal, moves):
				return moves				
		expanded_nodes = []
		if node.depth < depth_limit: #Expand only if the node is less than the depth limit
			expanded_nodes = (expand(node, goal))# expand
			nodes.extend(expanded_nodes) #put the expanded node at the top of the stack
			#nodes = expanded_nodes 			
			count += len(expanded_nodes)
		if len(nodes) == 0:  # No solution. Increse depth_limit
			depth_limit += 1
			nodes.append(Node('root', start, None, None, 0, heuristic(start, goal))) # Root
			


def astar(start, goal):
	nodes = [] # Node queue
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	order = [] # pop order
	nodes.append(Node('root', start, None, None, 0, heuristic(start, goal))) # Root
	print 'Start'
	display(start)
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
		if len(nodes) == 0: 
			print('No solution! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			print('The search order is:')
			print(order)
			return None #No solution
		node = nodes.pop(nodes.index(min(nodes, key = attrgetter('heuristic')))) # Pop and expand the node with the least estimated cost
		order.append(node.heuristic) # Record the visiting order
		visited += 1
		if is_goal(node.state, goal): #check if the node poped is the goal
			print('End')
			display(node.state)
			print('Goal! The search depth is '+str(node.depth))
			print('Nodes expanded:' + str(count))
			print('Nodes visited: ' + str(visited))
			#print('The order of the estimated cost of the nodes visited is:')
			#print(order)
			moves=solution(node)
			print ('Solution Checking')
			if solution_check(start, goal, moves):
				return moves				
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
	if is_goal(start,goal):
		print ('The solution is correct')
		return True
	if solution:
		state = start
		#display(state)
		for i in xrange(len(solution)):
			state = move(state, solution[i])
			#display(state)
		if is_goal(state,goal):
			print ('The solution is correct')
			return True
		else:
			print ('The solution is wrong')
			return False
	else:
		print('No solution')
		return False
		
def avg(start,goal):
	count = 0
	for i in xrange(100):
		count+=dfs_random(start,goal)
	avg = count//100
	print 'The average is',
	return avg
	

		
		
def main():
	#start = [' ',' ',' ',' ',' ','A',' ',' ','B',' ',' ','@',' ','C',' ',' '] # Distance from goal is 3
	#start = [' ',' ',' ','@',' ','A',' ',' ','B',' ',' ',' ',' ','C',' ',' '] # Distance from goal is 5
	#start = [' ',' ','A',' ',' ',' ','@',' ','B',' ',' ',' ',' ','C',' ',' '] # Distance from goal is 7
	#start = [' ',' ','A',' ',' ',' ',' ',' ','B',' ',' ',' ',' ','C','@',' '] # Distance from goal is 9
	#start = [' ',' ','A',' ',' ',' ',' ',' ',' ',' ','B',' ',' ','C',' ','@'] # Distance from goal is 11
	#start = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A','B','C','@'] # Distance from goal is 14
	start = ['A','B',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','C','@'] # Distance from goal is 14
	#start = [' ',' ',' ',' ',' ','A',' ',' ',' ','B',' ','@',' ','C',' ',' ']
	goal = {'A':5, 'B':9, 'C':13}
	#print(avg(start, goal))
	"""print ('Randomized depth first search')
	solution=(dfs_random(start, goal))
	#print 'The solution is: ',
	#print solution
	print('\n')"""
	
	"""print ('Depth-first search with depth limit')
	solution=(dfs_limit(start, goal, 20))
	print 'The solution is: ',
	print solution
	print('\n')
	
	print ('Performing breadth first search')
	solution=(bfs(start, goal))
	print 'The solution is: ',
	print solution
	print('\n')
	
	print ('Iterative deepening search')
	solution=(ids(start, goal))
	print 'The solution is: ',
	print solution
	print('\n')"""
	
	print ('A* search')
	solution=(astar(start, goal))
	print 'The solution is: ',
	print solution
	print('\n')

	

if __name__ == "__main__":
	main();
	
	
	

		

	


		

		
