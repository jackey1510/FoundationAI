import random
def getNextMove(agent):
	moves={0:"up",1:"down",2:"left",3:"right"}
	rng=random.randint(0,3)
	while (rng==0 and (agent in [0, 1, 2, 3])) or (rng==1 and (agent in [12, 13, 14, 15])) or (rng==2 and (agent in [0, 4, 8, 12])) or (rng==3 and (agent in [3, 7, 11, 15])) :#Only moves within the boundaries
		rng=random.randint(0,3)
	return(moves[rng]) 


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
		
"""def move(state, nextMove):
	new_state = state[:]
	index = new_state.index( '@' )
	if nextMove=="up":
		temp = new_state[index - 4]
		new_state[index - 4] = new_state[index]
		new_state[index] = temp
		return new_state	
	if nextMove=="down":
		temp = new_state[index + 4]
		new_state[index + 4] = new_state[index]
		new_state[index] = temp
		return new_state
	if nextMove=="left":
		temp = new_state[index - 1]
		new_state[index - 1] = new_state[index]
		new_state[index] = temp
		return new_state
	if nextMove=="right":
		temp = new_state[index + 1]
		new_state[index + 1] = new_state[index]
		new_state[index] = temp
		return new_state"""

def is_goal(state, goal):
	#print (str(state.index('A'))+','+str(state.index('B'))+','+str(state.index('C')))
	if state[goal['A']]=='A' and state[goal['B']]=='B' and state[goal['C']]=='C':
		return True
	else:
		return False


if __name__ == '__main__':
	start = [' ',' ','A',' ',' ',' ',' ',' ','B',' ',' ',' ',' ','C',' ','@']
	state = start
	goal = {'A':5, 'B':9, 'C':13}
	moveCount = 0
	moveList = list()
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
	


