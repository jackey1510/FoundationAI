import random
from random import shuffle
import copy
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
	col0 = move(node.state, 0, side)
	col1 = move(node.state, 1, side)
	col2 = move(node.state, 2, side)
	col3 = move(node.state, 3, side)
	col4 = move(node.state, 4, side)
	col5 = move(node.state, 5, side)
	col6 = move(node.state, 6, side)
	col = [col0, col1, col2, col3, col4, col5, col6]
	for i in xrange(7):
		if col[i]:
			expanded_nodes.append(Node(col[i], i, new_depth, -100000, 100000, opponent))
	return expanded_nodes

def getNextMove(state):
	no_of_moves = len(legal_move(state))
	col = random.randint(0,no_of_moves-1)
	return col

def move(state, col, side):
	new_state = copy.deepcopy(state)
	if col < 7: # sanity check
		for i in xrange(6):
			if new_state[5-i][col] == ' ':
				new_state[5-i][col] = side
				return new_state
	
	return None
	raise NotImplementedError()
	
def eval(state):
	side = 'O'
	opponent = 'X'
	score = 0
	opponent_score = 0
	if zugzwang(state, side):
		score = 100
	if threat(state, side) == 1:
		score = 10
	if perfect_start(state, side):
		score = 50
	# if counter_perfect_start(state, side):
		# score = 50
	if threat(state, side) == 0:
		score += connect2(state, side)*2 + sepearated2(state,side)
	if win(state, side):
		score = 10000
	#return score

	if zugzwang(state, opponent):
		opponent_score = 100
	if threat(state, opponent) == 1:
		opponent_score = 10
	if perfect_start(state, opponent):
		opponent_score = 50
	# if counter_perfect_start(state, opponent):
		# opponent_score = 50
	if threat(state, opponent) == 0:
		opponent_score += connect2(state, opponent)*2 + sepearated2(state,opponent)
	if win(state, opponent):
		opponent_score = 10000
	final_score = score - opponent_score*1.5
	return final_score
	
def eval2(state):
	opponent = 'O'
	side = 'X'
	score = 0
	opponent_score = 0
	if zugzwang(state, side):
		score = 100
	if threat(state, side) == 1:
		score = 10
	if perfect_start(state, side):
		score = 50
	#if counter_perfect_start(state, side):
		# score = 50
	if threat(state, side) == 0:
		score += connect2(state, side)*2 + sepearated2(state,side)
	if win(state, side):
		score = 1000
	#return score

	if zugzwang(state, opponent):
		opponent_score = 100
	if threat(state, opponent) == 1:
		opponent_score = 10
	if perfect_start(state, opponent):
		opponent_score = 50
	# if counter_perfect_start(state, opponent):
		# opponent_score = 50
	if threat(state, opponent) == 0:
		opponent_score += connect2(state, opponent)*2 + sepearated2(state,opponent)
	if win(state, opponent):
		opponent_score = 1000
	final_score = score - opponent_score
	return final_score


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

# def counter_perfect_start(state, side):
	
	# if side == 'O':
		# opponent = 'X'
	# if side == 'X':
		# opponent = 'O'
	# if state == [ [' ',' ',' ',' ',' ',' ',' '],
	              # [' ',' ',' ',' ',' ',' ',' '],
			      # [' ',' ',' ',' ',' ',' ',' '],
			      # [' ',' ',' ',' ',' ',' ',' '],
			      # [' ',' ',' ',' ',' ',' ',' '],
			      # [' ',' ',side,opponent,' ',' ',' ']] or state == [ [' ',' ',' ',' ',' ',' ',' '],
	                                                                 # [' ',' ',' ',' ',' ',' ',' '],
	                                                                 # [' ',' ',' ',' ',' ',' ',' '],
	                                                                 # [' ',' ',' ',' ',' ',' ',' '],
	                                                                 # [' ',' ',' ',' ',' ',' ',' '],
	                                                                 # [' ',' ',' ',opponent,side,' ',' ']]:
		# return True
	# return False

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
	legal=[]
	if not win(state, 'O') and not win(state, 'X'): # If a player has won already you cannot move
		for col in xrange (7):
			for i in xrange(6):
				if state[i][col] == ' ':
					legal.append(col)
		legal=list(set(legal)) # remove duplicate
	return legal
		
	
def cutoff(state, depth, ply):
	if depth == ply:
		return True
	if not legal_move(state):
		return True
	return False
	
def sum_score(node):
	nd = node
	score = eval(nd.state)
	while nd.parent:
			temp = nd.parent
			score += eval(temp.state)
			nd = temp
	return score
		

def alphabeta_node(node, ply):
	side = node.side
	if side == 'O':
		opponent = 'X'
	if side == 'X':
		opponent = 'O'
	if cutoff(node.state, node.depth, ply): 
		#print '1. eval: ',
		#print eval(node.state)
		#print sum_score(node)
		return (sum_score(node), None)
	best = None
	legal = legal_move(node.state)
	shuffle(legal)
	if node.side == 'O': # side of alphabeta AI
		for i in xrange(len(legal)):
			action = legal[i]
			child_node = Node(move(node.state, action, node.side), node, action, node.depth+1, node.alpha, node.beta, opponent)
			#print '2. Child :',
			#print child_node
			value = alphabeta_node(child_node, ply)
			#print '3. Value: ',
			#print value
			if value[0] > node.alpha:
				node.alpha = value[0]
				best = action
			if node.beta <= node.alpha: break
		return (node.alpha, best) #beta cutoff
	
	if node.side == 'X': # side of opponent
		for i in xrange(len(legal)):
			action = legal[i]
			child_node = Node(move(node.state, action, node.side), node, action, node.depth+1, node.alpha, node.beta, opponent)
			#print '2. Child :',
			#print child_node
			value = alphabeta_node(child_node, ply)
			if value[0] < node.beta:
				node.beta = value[0]
				best = action
			if node.beta <= node.alpha: break
		return (node.beta, best) #alpha cutoff
				
def alphabeta(state, depth, alpha, beta, side, ply):
	if side == 'O':
		opponent = 'X'
	if side == 'X':
		opponent = 'O'
	if cutoff(state, depth, ply):
		#print 'depth: ',
		#print depth
		score = eval(state)
		print score
		#display(state)
		return (score, None)
	best = None 
	if side == 'O':
		for i in xrange(len(legal_move(state))):
			action = legal_move(state)[i]
			child = move(state, action, side)
			value = alphabeta(child, depth+1, alpha, beta, opponent, ply)
			#print value
			if value[0] > alpha:
				alpha = value[0]
				best = action
			if beta <= alpha: break
		return (alpha, best)
	if side ==  'X':
		for i in xrange(len(legal_move(state))):
			action = legal_move(state)[i]
			child = move(state, action, side)
			value = alphabeta(child, depth+1, alpha, beta, opponent, ply)
			if value[0] < beta:
				beta = value[0]
				best = action
			if beta <= alpha: break
		return (beta, best)
		
		


"""def alphabeta(state, depth, alpha, beta, side, ply):
	if side == 'O':
		opponent = 'X'
	if side == 'X':
		opponent = 'O'
	if cutoff(state, depth, ply):
		print eval(state, side)
		return eval(state, side)
	if side == 'O':
		for i in xrange(len(legal_move(state))):
			beta = max(beta, alphabeta(move(state,legal_move(state)[i], side),depth+1, alpha, beta, opponent, ply))
			if beta <= alpha: break
			return alpha
	if side == 'X':
		for i in xrange(len(legal_move(state))):
			alpha = min(alpha, alphabeta(move(state,legal_move(state)[i], side),depth+1, alpha, beta, opponent, ply))
			if beta <= alpha: break
			return beta"""
		
	
def display(state):
	print '[{}][{}][{}][{}][{}][{}][{}] 0'.format(state[0][0], state[0][1], state[0][2], state[0][3], state[0][4], state[0][5], state[0][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 1'.format(state[1][0], state[1][1], state[1][2], state[1][3], state[1][4], state[1][5], state[1][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 2'.format(state[2][0], state[2][1], state[2][2], state[2][3], state[2][4], state[2][5], state[2][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 3'.format(state[3][0], state[3][1], state[3][2], state[3][3], state[3][4], state[3][5], state[3][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 4'.format(state[4][0], state[4][1], state[4][2], state[4][3], state[4][4], state[4][5], state[4][6])
	print '[{}][{}][{}][{}][{}][{}][{}] 5'.format(state[5][0], state[5][1], state[5][2], state[5][3], state[5][4], state[5][5], state[5][6])
	print ' 0  1  2  3  4  5  6  '
	print '\n'

def mutigame(ply1, ply2, games):
	p1win = 0
	p2win = 0
	draw = 0
	p1first = True
	for i in xrange(games):
		start = [ [' ',' ',' ',' ',' ',' ',' '],
				  [' ',' ',' ',' ',' ',' ',' '],
				  [' ',' ',' ',' ',' ',' ',' '],
				  [' ',' ',' ',' ',' ',' ',' '],
				  [' ',' ',' ',' ',' ',' ',' '],
				  [' ',' ',' ',' ',' ',' ',' ']]
		infinity = 10000000
		state = list(start)
		start = []
		player1 = 'O' # ai player
		player2 = 'X' # random player
		depth = 0
		root = Node(state, None, None, depth, -infinity, infinity, player1)
		node = root
		print 'player 1 is ply %i and player 2 is ply %i'%(ply1, ply2)
		#print state
		while legal_move(state) and not win(state, player1) and not win(state, player2):
			if p1first:
				if not win(state, player2):
					node = Node(state, None, None, depth, float("-inf"), float("inf"), player1)
					#print legal_move(state)
					p1move = alphabeta_node(node, ply1)[1]
					#p1move = alphabeta(state, 0, -infinity, infinity, player1, ply)[1]
					#print (p1move)
					state = move(state, p1move, player1)
					print 'Player 1 put a man in column %i'%(p1move)
					display(state)
				if not win(state, player1):
					node = Node(state, None, None, depth, float("-inf"), float("inf"), player2)
					# p2move = alphabeta(state, 0, -infinity, infinity, player2, 1)[1]
					p2move = alphabeta_node(node, ply2)[1]
					#p2move= getNextMove(state)
					state = move(state, p2move, player2)
					print 'Player 2 put a man in column %i'%(p2move)
					display(state)
			else:
				if not win(state, player1):
					node = Node(state, None, None, depth, float("-inf"), float("inf"), player2)
					# p2move = alphabeta(state, 0, -infinity, infinity, player2, 1)[1]
					p2move = alphabeta_node(node, ply2)[1]
					#p2move= getNextMove(state)
					state = move(state, p2move, player2)
					print 'Player 2 put a man in column %i'%(p2move)
					display(state)
				if not win(state, player2):
					node = Node(state, None, None, depth, float("-inf"), float("inf"), player1)
					#print legal_move(state)
					p1move = alphabeta_node(node, ply1)[1]
					#p1move = alphabeta(state, 0, -infinity, infinity, player1, ply)[1]
					#print (p1move)
					state = move(state, p1move, player1)
					print 'Player 1 put a man in column %i'%(p1move)
					display(state)
				
				
		if win(state, player1):
			print 'Player 1 won!'
			p1win += 1
		elif win(state, player2):
			print 'Player 2 won!'
			p2win += 1
		else:
			print 'Draw'
			draw += 1
		p1first = not p1first
	return (p1win, p2win, draw)
	

def main():
	"""start = [ [' ',' ',' ',' ',' ',' ',' '],
	          [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' ']]
	start = [ [' ',' ',' ',' ',' ',' ',' '],
	          [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ','X','O',' ',' '],
			  [' ','O','O','O','O',' ',' '],
			  ['X','X','O','X','X',' ',' ']]
	start = [ [' ',' ',' ',' ',' ',' ',' '],
	          [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ',' ',' ',' ',' '],
			  [' ',' ',' ','O',' ',' ',' ']]
	state = list(start)
	side = 'X'
	start = move(state, 1, side)
	display(state)
	print 'Threats: ',
	print threat(start, side)
	print 'Connect2: ',
	print connect2(start, side)
	print 'Separated2: ',
	print sepearated2(start, side)
	print 'Zugzwang: ',
	print zugzwang(start, side)
	print connect2(start, "O")
	if win(start, side):
		print 'Player '+side + ' wins'
	print eval(state)
	print eval2(state)"""
	
	print '1 vs 2'
	r1 = mutigame(1,2,20) 
	print '1 vs 3'
	r2 = mutigame(1,3,20)
	print '1 vs 4'
	r3 = mutigame(1,4,20)
	print '1 vs 5'
	r4 = mutigame(1,5,20)
	
	print '2 vs 3'
	r5 = mutigame(2,3,20)
	print '2 vs 4'
	r6 = mutigame(2,4,20)
	print '2 vs 5'
	r7 = mutigame(2,5,20)
	
	print '3 vs 4'
	r8 = mutigame(3,4,20)
	print '3 vs 5'
	r9 = mutigame(3,5,20)
	
	print '4 vs 5'
	r10 = mutigame(4,5,20)
	
	result = [r1, r2, r3, r4, r5, r6 ,r7, r8, r9, r10]
	print result
	
	
	#print ('player 1 won %i times and player 2 won %i times, %i draws'%(result[0], result[1], result[2]))
	return False

if __name__ == "__main__":
	main();