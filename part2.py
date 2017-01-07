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
	def __init__(self, state, parent, move, depth, score):
		self.state = state
		self.parent = parent
		self.move = move
		self.depth = depth
		self.score = score # Evalutated score
	def __repr__(self):
		return repr((self.name, self.state, self.parent, self.move, self.depth, self.score))
	
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

def move(state, col, side):
	new_state = state[:]
	for i in xrange(5):
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
	return Score

def pos(state, side):
	position = []
	for row in xrange(6):
		for col in xrange(7):
			if state[row][col] == side:
				position.append([row,col])
	return position

def threat(state, side): # 3 connected already
	th1 = [' ', side, side, side]
	th2 = [side, ' ', side, side]
	th3 = [side, side, ' ', side]
	th4 = [side, side, side, ' ']
	th = [th1, th2, th3, th4]
	threats = 0
	for i in xrange(6): # Horizontally
		for j in xrange(4):
			for k in xrange(4):
				if [state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]] == th[k]:
					threats+=1
	for i in xrange(3): # Vertically connected 4
		for j in xrange(7):
			for k in xrange(4):
				if [state[i][j], state[i+1][j], state[i+2][j], state[i+3][j]] == th[k]:
					threats+=1
				
	for i in xrange(3):
		for j in xrange(4):
			for k in xrange(4):
				if [state[i][j], state[i+1][j+1], state[i+2][j+2], state[i+3][j+3]] == th[k]:
					threats+=1
				
	for i in xrange(3):
		for j in xrange(4):
			for k in xrange(4):
				if [state[i][6-j], state[i+1][5-j], state[i+2][4-j], state[i+3][3-j]] == th[k]:
					threats+=1

	return threats
	
def zugzwang(state, side):
	if threat(state, side) > 1:
		return True
	return False




def win(state=[],side=''):
	connect4 = [side,side,side,side]
	for i in xrange(6): # Horizontally connected 4
		for j in xrange(4):
			if [state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]] == connect4:
				return True
	
	for i in xrange(3): # Vertically connected 4
		for j in xrange(7):
			if [state[i][j], state[i+1][j], state[i+2][j], state[i+3][j]] == connect4:
				return True
				
	for i in xrange(3):
		for j in xrange(4):
			if [state[i][j], state[i+1][j+1], state[i+2][j+2], state[i+3][j+3]] == connect4:
				return True
				
	for i in xrange(3):
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
	#print ' 0  1  2  3  4  5  6  '
			
	

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