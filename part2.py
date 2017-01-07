import random
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
	
def expand(node):
	side = node.side
	opponent = ' '
	if side == 'O':
		opponent = 'X'
	if side == 'X':
		opponent = 'O'
	expanded_nodes = []
	new_depth = node.depth + 1
	col0 = list(move(node.state, 0, side))
	col1 = list(move(node.state, 1, side))
	col2 = list(move(node.state, 2, side))
	col3 = list(move(node.state, 3, side))
	col4 = list(move(node.state, 4, side))
	col5 = list(move(node.state, 5, side))
	col6 = list(move(node.state, 6, side))
	col = [col0, col1, col2, col3, col4, col5, col6]
	for i in xrange(7):
		if col[i]:
			expanded_nodes.append(Node(col[i], node, i, new_depth, -100000, 100000, opponent))
	return expanded_nodes

def getNextMove(state):
	no_of_moves = len(legal_move(state))
	col=random.randint(0,no_of_moves)
	return col

def actmove(state, col, side):
	new_state = list(state)
	print 'New state:'
	print new_state
	if col < 7: # sanity check
		for i in xrange(6):
			if new_state[5-i][col] == ' ':
				new_state[5-i][col] = side
				return new_state
	return None
	
def eval(state, side):
	opponent = ''
	if side == 'O':
		opponent = 'X'
	if side == 'X':
		opponent = 'O'
	score = 0
	opponent_score = 0
	if zugzwang(state, side):
		score = 100
	if threat(state, side) == 1:
		score = 10
	if perfect_start(state, side):
		score = 50
	if counter_perfect_start(state, side):
		score = 50
	if threat == 0:
		score += connect2(state, side)*2 + sepearated2(state,side)
	if win(state, side):
		score = 1000

	if zugzwang(state, opponent):
		opponent_score = 100
	if threat(state, opponent) == 1:
		opponent_score = 10
	if perfect_start(state, opponent):
		opponent_score = 50
	if counter_perfect_start(state, opponent):
		opponent_score = 50
	if threat == 0:
		opponent_score += connect2(state, opponent)*2 + sepearated2(state,opponent)
	if win(state, opponent):
		opponent_score = 1000
	return score-opponent_score


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
			for k in xrange(2):
				if [state[i][j], state[i+1][j], state[i+2][j]] == c2[k]:
					con2 += 1
	for i in xrange(4): # Top left to bottom right 
		for j in xrange(5):
			for k in xrange(2):
				if [state[i][j], state[i+1][j+1], state[i+2][j+2]] == c2[k]:
					con2 += 1
	for i in xrange(4): # Bottom left to top right
		for j in xrange(5):
			for k in xrange(2):
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

def legal_move(state): # check if there is any empty slot in the board
	new_state = state[:]
	legal=[]
	for col in xrange (7):
		for i in xrange(6):
			if new_state[i][col] == ' ':
				legal.append(col)
	legal=list(set(legal)) # remove duplicate
	return legal
		
	
def cutoff(state, depth, ply):
	if depth == ply:
		return True
	if not legal_move(state):
		return True
	return False

def alphabeta(node, ply):
	if cutoff(node.state, node.depth, ply): 
		return (eval(node.state, node.side), None)
	best = None
	expanded_nodes = expand(node)
	for i in xrange(len(expanded_nodes)):
		child_node = expanded_nodes.pop()
		value = alphabeta(child_node, ply)
		if node.side == 'O': # side of alphabeta AI
			if value > node.alpha:
				node.alpha = value
				best = child_node.move
			if node.beta <= node.alpha:
				return best #beta cutoff
		if node.side == 'X': # side of opponent
			if value < node.beta:
				node.beta = value
				best = child_node.move
			if node.beta <= node.alpha: 
				return best #alpha cutoff
		 
	
def display(state):
	print '[{}][{}][{}][{}][{}][{}][{}] 0'.format(state[0][0], state[0][1], state[0][2], state[0][3], state[0][4], state[0][5], state[0][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 1'.format(state[1][0], state[1][1], state[1][2], state[1][3], state[1][4], state[1][5], state[1][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 2'.format(state[2][0], state[2][1], state[2][2], state[2][3], state[2][4], state[2][5], state[2][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 3'.format(state[3][0], state[3][1], state[3][2], state[3][3], state[3][4], state[3][5], state[3][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 4'.format(state[4][0], state[4][1], state[4][2], state[4][3], state[4][4], state[4][5], state[4][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 5'.format(state[5][0], state[5][1], state[5][2], state[5][3], state[5][4], state[5][5], state[5][6])
	print ' 0  1  2  3  4  5  6  '
	print '\n'

def game():
	start = [ [' ',' ',' ',' ',' ',' ',' '],
	          [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' ']]
	state = list(start)
	player1 = 'O' # ai player
	player2 = 'X' # random player
	depth = 0
	root = Node(start, None, None, depth, float("-inf"), float("inf"), player1)
	node = root
	ply = 2
	print state
	for i in xrange(21):
		print legal_move(state)
		p1move = alphabeta(node, ply)
		state = move(state, p1move, player1)
		print 'Player 1 put a man in column %i'%(p1move)
		display(state)
		p2move = getNextMove(state)
		state = move(state, p2move, player2)
		print 'Player 2 put a man in column %i'%(p2move)
		display(state)
		depth += 1
		node = Node(state, None, p1move, depth, float("-inf"), float("inf"), player1)
	if win(state, player1):
		print 'Player 1 won!'
	elif win(state, player2):
		print 'Player 2 won!'
	else:
		print 'Draw'
	

def main():
	"""start = [ [' ',' ',' ',' ',' ',' ',' '],
	          [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ','X',' ',' ',' '],
			  [' ',' ',' ','X','X',' ',' '],
			  ['X','X',' ','X',' ',' ',' ']]
	start = [ [' ',' ',' ',' ',' ',' ',' '],
	          [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' ']]
	state = list(start)
	side = 'X'
	state = move(state, 1, side)
	display(state)
	print 'Threats: ',
	print threat(start, side)
	print 'Connect2: ',
	print connect2(start, side)
	print 'Separated2: ',
	print sepearated2(start, side)
	print 'Zugzwang: ',
	print zugzwang(start, side)
	print 'Score: ',
	print eval(start, side)
	if win(start, side):
		print 'Player '+side + ' wins'"""
	game()
	return False

if __name__ == "__main__":
	main();