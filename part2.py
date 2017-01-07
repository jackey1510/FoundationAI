"""
[ ][ ][ ][ ][ ][ ][ ] 0
[ ][ ][ ][ ][ ][ ][ ] 1
[ ][ ][ ][ ][ ][ ][ ] 2
[ ][ ][ ][ ][ ][ ][ ] 3
[ ][ ][ ][ ][ ][ ][ ] 4
[ ][ ][ ][ ][ ][ ][ ] 5
 0  1  2  3  4  5  6
"""
class Node:
	def __init__(self, state, parent, move, depth, alpha, beta, side):
		self.state = state
		self.parent = parent
		self.move = move
		self.depth = depth
		self.alpha = alpha
		self.beta = beta
		self.side = side
	def __repr__(self):
		return repr((self.state, self.parent, self.move, self.depth, self.alpha, self.beta, self.side))
	
def expand(node, goal, side):
	expanded_nodes = []
	new_depth = node.depth + 1
	new_name = node.name
	col0 = move(node.state, 0, side)
	col1 = move(node.state, 1, side)
	col2 = move(node.state, 2, side)
	col3 = move(node.state, 3, side)
	col4 = move(node.state, 4, side)
	col5 = move(node.state, 5, side)
	col6 = move(node.state, 6, side)
	col = [col0, col1, col2, col3, col4, col5, col6]
	for i in xrange(6):
		if col[i]:
			expanded_nodes.append(Node(col[i], node, i, new_depth, new_depth))
	return expanded_nodes

def alphabeta(start, side):
	nodes = [] # Node stack
	count = 0 # Number of nodes expanded
	visited = 0 # Number of nodes visited
	nodes.append(Node(start, None, None, 0, float("-inf"), float("inf"), side)) # Root
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
			display(node.state)
			moves=solution(node)
			print ('Solution Checking')		
		expanded_nodes = []
		if node.depth < depth_limit: #Expand only if the node is less than the depth limit
			expanded_nodes = (expand(node, goal))# expand
			nodes.extend(expanded_nodes) #put the expanded node at the top of the stack			
			count += len(expanded_nodes)

def move(state, col, side):
	new_state = state[:]
	if col < 7:
		for i in xrange(6):
			if new_state[5-i][col] == ' ':
				new_state[5-i][col] = side
				return new_state
	return None

def eval(state, side):
	score = 0
	if win(state, side):
		score = 1000
	if zugzwang(state, side):
		score = 100
	if threat(state, side) == 1:
		score = 10
	if perfect_start(state, side):
		score = 50
	if counter_perfect_start(state, side):
		score = 50
	score += connect2(state, side)*2 + sepearated2(state,side)
	return score

def pos(state, side):
	position = []
	for row in xrange(6):
		for col in xrange(7):
			if state[row][col] == side:
				position.append([row,col])
	return position

def sepearated2(state, side): # 2 sepearated men with nothing in between that can form threat
	case1 = [side, ' ', side]
	case2 = [side, ' ', ' ', side]
	sp2 = [case1, case2]
	sep2 = 0
	for i in xrange(6): # Horizontally 
		for j in xrange(4):
			if [state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]] == sp2[1]:
				sep2+=1
	for i in xrange(3): # Vertically 
		for j in xrange(7):
			if [state[i][j], state[i+1][j], state[i+2][j], state[i+3][j]] == sp2[1]:
				sep2+=1
	for i in xrange(3): # Top left to bottom right  
		for j in xrange(4):
			if [state[i][j], state[i+1][j+1], state[i+2][j+2], state[i+3][j+3]] == sp2[1]:
				sep2+=1
	for i in xrange(3): # Bottom left to top right
		for j in xrange(4):
			if [state[i][6-j], state[i+1][5-j], state[i+2][4-j], state[i+3][3-j]] == sp2[1]:
				sep2+=1
	
	for i in xrange(6): # Horizontally
		for j in xrange(5):
			if [state[i][j], state[i][j+1], state[i][j+2]] == sp2[0]:
				sep2 += 1
	for i in xrange(4): # Vertically
		for j in xrange(7):
			if [state[i][j], state[i+1][j], state[i+2][j]] == sp2[0]:
				sep2 += 1
	for i in xrange(4): # Top left to bottom right 
		for j in xrange(5):
			if [state[i][j], state[i+1][j+1], state[i+2][j+2]] == sp2[0]:
				sep2 += 1
	for i in xrange(4): # Bottom left to top right
		for j in xrange(5):
			if [state[i][6-j], state[i+1][5-j], state[i+2][4-j]] == sp2[0]:
				sep2 += 1
	
	return sep2
	
def connect2(state, side): # 2 connected already with space next to it
	case1=[' ', side, side]
	case2=[side, side, ' ']
	c2=[case1, case2]
	con2 = 0
	for i in xrange(6): # Horizontally
		for j in xrange(5):
			for k in xrange(2):
				if [state[i][j], state[i][j+1], state[i][j+2]] == c2[k]:
					con2 += 1
	for i in xrange(4): # Vertically
		for j in xrange(7):
			for k in xrange(4):
				if [state[i][j], state[i+1][j], state[i+2][j]] == c2[k]:
					con2 += 1
	for i in xrange(4): # Top left to bottom right 
		for j in xrange(5):
			for k in xrange(2):
				if [state[i][j], state[i+1][j+1], state[i+2][j+2]] == c2[k]:
					con2 += 1
	for i in xrange(4): # Bottom left to top right
		for j in xrange(5):
			for k in xrange(4):
				if [state[i][6-j], state[i+1][5-j], state[i+2][4-j]] == c2[k]:
					con2 += 1
	return con2

def threat(state, side): # 3 connected already
	case1 = [' ', side, side, side]
	case2 = [side, ' ', side, side]
	case3 = [side, side, ' ', side]
	case4 = [side, side, side, ' ']
	th = [case1, case2, case3, case4]
	threats = 0
	for i in xrange(6): # Horizontally
		for j in xrange(4):
			for k in xrange(4):
				if [state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]] == th[k]:
					threats+=1
	for i in xrange(3): # Vertically
		for j in xrange(7):
			for k in xrange(4):
				if [state[i][j], state[i+1][j], state[i+2][j], state[i+3][j]] == th[k]:
					threats+=1
				
	for i in xrange(3): # Top left to bottom right 
		for j in xrange(4):
			for k in xrange(4):
				if [state[i][j], state[i+1][j+1], state[i+2][j+2], state[i+3][j+3]] == th[k]:
					threats+=1
				
	for i in xrange(3): # Bottom left to top right
		for j in xrange(4):
			for k in xrange(4):
				if [state[i][6-j], state[i+1][5-j], state[i+2][4-j], state[i+3][3-j]] == th[k]:
					threats+=1

	return threats
	
def zugzwang(state, side):
	if threat(state, side) > 1:
		return True
	return False

def perfect_start(state, side):
	if state == [ [' ',' ',' ',' ',' ',' ',' '],
	              [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',' ',side,' ',' ',' ']]:
		return True
	return False

def counter_perfect_start(state, side):
	
	if side == 'O':
		opponent = 'X'
	if side == 'X':
		opponent = 'O'
	if state == [ [' ',' ',' ',' ',' ',' ',' '],
	              [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',' ',' ',' ',' ',' '],
			      [' ',' ',side,opponent,' ',' ',' ']] or state == [ [' ',' ',' ',' ',' ',' ',' '],
	                                                                 [' ',' ',' ',' ',' ',' ',' '],
	                                                                 [' ',' ',' ',' ',' ',' ',' '],
	                                                                 [' ',' ',' ',' ',' ',' ',' '],
	                                                                 [' ',' ',' ',' ',' ',' ',' '],
	                                                                 [' ',' ',' ',opponent,side,' ',' ']]:
		return True
	return False
				  



def win(state=[],side=''):
	connect4 = [side,side,side,side]
	for i in xrange(6): # Horizontally
		for j in xrange(4):
			if [state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]] == connect4:
				return True
	
	for i in xrange(3): # Vertically
		for j in xrange(7):
			if [state[i][j], state[i+1][j], state[i+2][j], state[i+3][j]] == connect4:
				return True
				
	for i in xrange(3): # Top left to bottom right 
		for j in xrange(4):
			if [state[i][j], state[i+1][j+1], state[i+2][j+2], state[i+3][j+3]] == connect4:
				return True
				
	for i in xrange(3): # Bottom left to top right
		for j in xrange(4):
			if [state[i][6-j], state[i+1][5-j], state[i+2][4-j], state[i+3][3-j]] == connect4:
				return True
	return False
	
def display(state):
	print '[{}][{}][{}][{}][{}][{}][{}]'.format(state[0][0], state[0][1], state[0][2], state[0][3], state[0][4], state[0][5], state[0][6])
	print '[{}][{}][{}][{}][{}][{}][{}]'.format(state[1][0], state[1][1], state[1][2], state[1][3], state[1][4], state[1][5], state[1][6])
	print '[{}][{}][{}][{}][{}][{}][{}]'.format(state[2][0], state[2][1], state[2][2], state[2][3], state[2][4], state[2][5], state[2][6])
	print '[{}][{}][{}][{}][{}][{}][{}]'.format(state[3][0], state[3][1], state[3][2], state[3][3], state[3][4], state[3][5], state[3][6])
	print '[{}][{}][{}][{}][{}][{}][{}]'.format(state[4][0], state[4][1], state[4][2], state[4][3], state[4][4], state[4][5], state[4][6])
	print '[{}][{}][{}][{}][{}][{}][{}]'.format(state[5][0], state[5][1], state[5][2], state[5][3], state[5][4], state[5][5], state[5][6])
	print '\n'
			
	

def main():
	start = [ [' ',' ',' ',' ',' ',' ',' '],
	          [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  ['X','X','X','X',' ',' ',' ']]
	print(start[5][4])
	display(start)
	print threat(start,'X')
	side = 'X'
	if win(start, side):
		print 'Player '+side + ' wins'
	return False

if __name__ == "__main__":
	main();