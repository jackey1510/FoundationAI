
import random
def getNextMove(agent):
	moves={0:"left",1:"right",2:"up",3:"down"}
	rng=random.randint(0,3)
	while (rng==0 and agent[0]==0) or (rng==3 and agent[1]==3) or (rng==1 and agent[0]==3) or (rng==2 and agent[1]==0) :#Only moves within the boundaries
		rng=(rng+random.randint(0,10))%4
	return(moves[rng]) 


def move(agent,movement):
	old_pos=list(agent)
	if movement=="left":
		if agent[0]>0:
			agent[0]-=1
	if movement=="right":
		if agent[0]<3:
			agent[0]+=1
	if movement=="up":
		if agent[1]>0:
			agent[1]-=1
	if movement=="down":
		if agent[0]<3:
			agent[1]+=1
	return agent

def swap(agent,prev_pos,block):
	if block == agent:
		return prev_pos
	else:
		return block
		

def goal(A,B,C):
	if A==[1,1] and B==[2,1] and C==[3,1]:
		return True
	else:
		return False


if __name__ == '__main__':
	agent=[3,3]
	A=[0,3]
	B=[1,3]
	C=[2,3]
	moveCount=0
	moveList=list()
	agent_pos_history=[list(agent)]
	while not goal(A,B,C):
	#for i in xrange(100):
		nextMove=getNextMove(agent)
		moveList.append(nextMove)
		agent_pos_history.append(list(move(agent,nextMove)))
		A=swap(agent,agent_pos_history[moveCount],A)
		B=swap(agent,agent_pos_history[moveCount],B)
		C=swap(agent,agent_pos_history[moveCount],C)
		moveCount+=1
		
		#print('Agent: '+str(agent)+' Blocks: '+str(A)+' '+str(B)+' '+str(C))
    
		
	
	#print('The moves are: '+str(moveList))
	print('Agent: '+str(agent)+' A,B,C: '+str(A)+' '+str(B)+' '+str(C))
	print('Total '+str(moveCount)+' steps')
	


