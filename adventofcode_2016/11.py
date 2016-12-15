#!/usr/bin/env python

import sys
import hashlib
from itertools import chain,combinations
import json

Ag=1<<1
Bg=1<<2
Cg=1<<3
Dg=1<<4
Eg=1<<5
Am=1<<6
Bm=1<<7
Cm=1<<8
Dm=1<<9
Em=1<<10

g_mask=Ag|Bg|Cg|Dg|Eg
m_mask=Am|Bm|Cm|Dm|Em

g_list=[Ag,Bg,Cg,Dg,Eg]
m_list=[Am,Bm,Cm,Dm,Em]
gm_list=[Ag|Am,Bg|Bm,Cg|Cm,Dg|Dm,Eg|Em]

max_moves=sys.maxint

# States are bitwise OR of present devices arranged as a list (floors 0=>3) of lists (generator,chips)
if len(sys.argv) == 2 and sys.argv[1] == 'test':
	state=[ 1,
			Am|Bm,
			Ag,
			Bg,
			0 ]
	end=[ 4, 0, 0, 0, Ag|Bg|Am|Bm ]
else:
	state=[ 1,
			Ag|Bg|Cg|Dg|Eg|Bm|Dm|Em,
			Am|Cm,
			0,
			0 ]
	end=[ 4, 0, 0, 0, Ag|Bg|Cg|Dg|Eg|Am|Bm|Cm|Dm|Em ]

# Elevator (index into state)
E=0
solves={}

def hash(state):
	# using hexdigest for possible debugging:  binary digest should be safe in this environment
	return hashlib.md5(json.dumps(state, sort_keys=True)).hexdigest()

def moves_from(state):
	global E

	# what is elegible to move (on the floor with the elevator)?
	gs=[ state[state[E]] & x for x in g_list ] # all generators on the floor
	gs=[ x for x in gs if x ] # strip empty entries
	ms=[ state[state[E]] & x for x in m_list ] # all microchips on the floor
	ms=[ x for x in ms if x ] # strip empty entries
	gms=[ state[state[E]] & x for x in gm_list ] # all generator-microchip pairs on the floor
	gms=[ x for x in gms if x in gm_list ] # strip invalid entries

	moves=[]
	moves += [ x[0] for x in combinations(gs,1) ]  # 1 generator
	moves += [ x|y for x,y in combinations(gs,2) ] # 2 generators
	moves += [ x[0] for x in combinations(ms,1) ]  # 1 microchip
	moves += [ x|y for x,y in combinations(ms,2) ] # 2 microchips
	# create tuples with the direction of the movement

	moves = [ (x,1) for x in moves ] + [ (x,-1) for x in moves ]
	valid_moves=[ x for x in moves if valid_move(x,state) ]


	gm_up_moves = [ (x,1) for x in gms if valid_move( (x,1), state) ]
	gm_dn_moves = [ (x,-1) for x in gms if valid_move( (x,-1), state) ]

	# Pair interchangeability optimization
#	if len(gms) > 1:
#		gms=[ gms[0] ]


	# returned states are tuples of state and equivalent states
	states=[]
	for move in valid_moves:
		states.append( ( state_from(move,state), None ) )

	if len(gm_up_moves) == 1:
		states.append( ( state_from(gm_up_moves[0],state), None ) )
	else:
		for move in gm_up_moves[1:]:
			states.append( ( state_from(move,state), state_from(gm_up_moves[0],state) ) )

	if len(gm_dn_moves) == 1:
		states.append( ( state_from(gm_dn_moves[0],state), None ) )
	else:
		for move in gm_dn_moves[1:]:
			states.append( ( state_from(move,state), state_from(gm_dn_moves[0],state) ) )

	return states

def state_from(move,state):
	global E

	new_state=list(state)
	floor = state[E]
	new_state[floor] -= move[0]
	floor = state[E] + move[1]
	new_state[floor] += move[0]
	new_state[E] = floor

	return new_state

def valid_move(move,state):
	global g_mask,m_mask

	# No Basement!
	if state[E]==1 and move[1]==-1:
		return False

	# No Roof!
	if state[E]==4 and move[1]==1:
		return False

	# Don't go down in an empty building
	if move[1]==-1 and E>2:
		empty=True
		for x in range(1,E):
			if state[x]!=0:
				empty=False
		if empty:
			return False

	for m in m_list:
		my_g=m>>5

		# am I on the old floor?
		floor = state[E]
		if m & (state[floor]-move[0]):
			# another generator is with me and my generator is not
			if (g_mask-my_g) & (state[floor]-move[0]) and not my_g & (state[floor]-move[0]):
				return False

		# am I on the new floor?
		floor = state[E]+move[1]
		if m & (state[floor]+move[0]):
			# another generator is with me and my generator is not
			if (g_mask-my_g) & (state[floor]+move[0]) and not my_g & (state[floor]+move[0]):
				return False
	return True

def solve(state,depth):
	global recursions

	recursions += 1
	my_hash=hash(state)

	if my_hash in solves:
		return 1 + solves[my_hash][0]

	moves=max_moves
	# pre-define this solve as max_moves so children don't try to resolve it
	solves[my_hash]=[ max_moves, depth, None, None ]

	new_states=moves_from(state)
	if not new_states:
		return max_moves

	index=0
	winner=0
	for candidate in new_states:
		# if this candidate is not identical to a previous, solve it
#		if not candidate[1]:
		tmp=solve(candidate[0],depth+1)
		if tmp < moves:
			moves=tmp
			winner=index
		index += 1
#		moves=min(solve(candidate),moves)

	solves[my_hash]=[ moves, depth, new_states[winner][0], hash(new_states[winner][0]) ]

	return 1+moves

# Pre-seed our end state
solves[hash(end)]=[0,999,end,None]

recursions=0
print "Starting:", state
print "%d moves needed to solve" % ( solve(state,0) - 1 )
print "%d recursuions required" % recursions

step=hash(state)
while solves[step][3]:
	print "Step",solves[step][0],"(depth",solves[step][1],"):",solves[step][2]
	step=solves[step][3]

sys.exit(0)
