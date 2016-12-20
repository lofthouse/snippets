#!/usr/bin/env python

import sys
import hashlib
from heapq import heapify,heappop,heappush
from itertools import combinations
import json

Am=1<<1
Bm=1<<2
Cm=1<<3
Dm=1<<4
Em=1<<5
Fm=1<<6
Gm=1<<7

Ag=1<<8
Bg=1<<9
Cg=1<<10
Dg=1<<11
Eg=1<<12
Fg=1<<13
Gg=1<<14

g_mask=Ag|Bg|Cg|Dg|Eg|Fg|Gg
m_mask=Am|Bm|Cm|Dm|Em|Fm|Gm

g_list=[Ag,Bg,Cg,Dg,Eg,Fg,Gg]
m_list=[Am,Bm,Cm,Dm,Em,Fm,Gm]
gm_list=[Ag|Am,Bg|Bm,Cg|Cm,Dg|Dm,Eg|Em,Fg|Fm,Gg|Gm]

nodes_expanded=0
nodes_skipped=0

# States are bitwise OR of present devices arranged as a list (floors 0=>3).  list[0] is elevator location.
if len(sys.argv) == 2 and sys.argv[1] == 'test':
	state=[ 1,
			Am|Bm,
			Ag,
			Bg,
			0 ]
	end=[ 4, 0, 0, 0, Ag|Bg|Am|Bm ]
elif len(sys.argv) == 2 and sys.argv[1] == '1':
	state=[ 1,
			Ag|Bg|Cg|Dg|Eg|Bm|Dm|Em,
			Am|Cm,
			0,
			0 ]
	end=[ 4, 0, 0, 0, Ag|Bg|Cg|Dg|Eg|Am|Bm|Cm|Dm|Em ]
else:
	state=[ 1,
			Ag|Bg|Cg|Dg|Eg|Bm|Dm|Em|Fg|Fm|Gg|Gm,
			Am|Cm,
			0,
			0 ]
	end=[ 4, 0, 0, 0, Ag|Bg|Cg|Dg|Eg|Fg|Gg|Am|Bm|Cm|Dm|Em|Fm|Gm ]

# Elevator (index into state)
E=0

def hash(state):
	# using hexdigest for possible debugging:  binary digest should be safe in this environment
	return hashlib.md5(json.dumps(state, sort_keys=True)).hexdigest()

def pack(state):
	# reduce a specific state to a fully-equivalent representation
	# representation is tuple( elevator floor,
	# GMs on 1, GMs on 2, GMs on 3, GMs on 4,
	# 1-2 splits, 1-3 splits, 1-4 splits, 2-3 splits, 2-4 splits, 3-4 splits (g high),
	# 1-2 splits, 1-3 splits, 1-4 splits, 2-3 splits, 2-4 splits, 3-4 splits (m high),
	tmp=[state[0]]
	for floor in (1,2,3,4):
		count=0
		for pair in gm_list:
			if state[floor] & pair:
				count += 1
		tmp.append(count)

	for x in combinations((1,2,3,4),2):
		count=0
		for m in m_list:
			for g in g_list:
				if state[x[0]] & m and state[x[1]] & g:
					count += 1
		tmp.append(count)

	for x in combinations((1,2,3,4),2):
		count=0
		for g in g_list:
			for m in m_list:
				if state[x[0]] & g and state[x[1]] & m:
					count += 1
		tmp.append(count)

	return tuple(tmp)

#def unpack(state):
#	return [


def moves_from(state):
	global E
	global visited

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

	states=[]
	for move in valid_moves:
		states.append( state_from(move,state) )

	if gm_up_moves:
		states.append( state_from(gm_up_moves[0],state) )
#	if len(gm_up_moves) > 1:
#		for move in gm_up_moves[1:]:
#			visited.add( pack(state_from(move,state)) )

	if gm_dn_moves:
		states.append( state_from(gm_dn_moves[0],state) )
#	if len(gm_dn_moves) > 1:
#		for move in gm_dn_moves[1:]:
#			visited.add( pack(state_from(move,state)) )

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
		my_g=m<<7

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

def solve(state):
	global nodes_expanded
	global nodes_skipped
	global to_visit
	global visited
	moves = 0
	max_moves = 0

#	print to_visit

	while to_visit:
#		print "To Visit:",to_visit
		moves,neighbor=heappop( to_visit )
#		print "Moves:",moves
#		print "Neighbors:",neighbor

		new_states=moves_from( neighbor )
#		print "New States:", new_states

		if end in new_states:
			return moves + 1

		for next in new_states:
			if not pack( next ) in visited:
				visited.add( pack( next ) )
				if not ( moves+1,next ) in to_visit:
					heappush( to_visit, ( moves+1,next ) )
					nodes_expanded += 1
					if moves + 1 > max_moves:
						max_moves += 1
						print "Exploring %d move nodes" % max_moves
			else:
				nodes_skipped += 1

to_visit=[(0,state)]
heapify( to_visit )
visited=set([])

print "Starting:", state
#solve(state)
print "%d moves needed to solve" % solve(state)
print "%d nodes expanded" % nodes_expanded
print "%d nodes skipped" % nodes_skipped

sys.exit(0)
