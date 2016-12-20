#!/usr/bin/env python

import sys
from heapq import heapify,heappop,heappush
from itertools import combinations

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

g_list=(Ag,Bg,Cg,Dg,Eg,Fg,Gg)
m_list=(Am,Bm,Cm,Dm,Em,Fm,Gm)
gm_list=(Ag|Am,Bg|Bm,Cg|Cm,Dg|Dm,Eg|Em,Fg|Fm,Gg|Gm)

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

def pack(state):
	# reduce a specific state to a fully-equivalent representation
	# representation is tuple( elevator floor,
	# GMs on 1, GMs on 2, GMs on 3, GMs on 4,
	# 1-2 splits, 1-3 splits, 1-4 splits, 2-3 splits, 2-4 splits, 3-4 splits (g high),
	# interestingly, the order of g-m doesn't matter:  not including the second order cuts time nearly in half!
	# this means that this function is most of the processing time in this solution
	# a smarter state structure might have enabled sub-second solutions.  Oh well.

	# Using a tuple throughout saves a small amount of time vs. building a list then converting back to a tuple
	tmp=(state[0],)
	for floor in (1,2,3,4):
		count=0
		for pair in gm_list:
			if state[floor] & pair:
				count += 1
		tmp+=(count,)

	for x in combinations((1,2,3,4),2):
		count=0
		for m in m_list:
			for g in g_list:
				if state[x[0]] & m and state[x[1]] & g:
					count += 1
		tmp+=(count,)

	return tmp

def moves_from(state):
	global E
	global visited

	# what is elegible to move (on the floor with the elevator)?
	gs=[ state[state[E]] & x for x in g_list ] # all generators on the floor
	gs=[ x for x in gs if x ] # strip empty entries (actually faster than putting if condition in above)
	ms=[ state[state[E]] & x for x in m_list ] # all microchips on the floor
	ms=[ x for x in ms if x ] # strip empty entries (actually faster than putting if condition in above)
	gms=[ state[state[E]] & x for x in gm_list ] # all generator-microchip pairs on the floor
	gms=[ x for x in gms if x in gm_list ] # strip invalid entries (actually faster than putting if condition in above)

	moves=[]
	moves += [ x[0] for x in combinations(gs,1) ]  # 1 generator
	moves += [ x|y for x,y in combinations(gs,2) ] # 2 generators
	moves += [ x[0] for x in combinations(ms,1) ]  # 1 microchip
	moves += [ x|y for x,y in combinations(ms,2) ] # 2 microchips
	# create tuples with the direction of the movement

	moves = [ (x,1) for x in moves ] + [ (x,-1) for x in moves ]
	valid_moves=[ x for x in moves if valid_move(x,state) ]

	states=[]
	for move in valid_moves:
		states.append( state_from(move,state) )

	# all gm pairs are equivalent:  only include one!
	if gms:
		if valid_move( (gms[0],1), state):
			states.append( state_from( (gms[0],1),state) )
		if valid_move( (gms[0],-1), state):
			states.append( state_from( (gms[0],-1),state) )

	return states

def state_from(move,state):
	global E

	new_state=list(state)
	new_state[E] = state[E] + move[1]
	new_state[state[E]] -= move[0]
	new_state[state[E]+move[1]] += move[0]

	return new_state

def valid_move(move,state):
	global g_mask,m_mask

	# No Basement!
	if state[E]==1 and move[1]==-1:
		return False

	# No Roof!
	if state[E]==4 and move[1]==1:
		return False

	for m in m_list:
		my_g=m<<7

		# if I am on the old floor...
		floor = state[E]
		if m & (state[floor]-move[0]):
			# and another generator is with me and my generator is not
			if (g_mask-my_g) & (state[floor]-move[0]) and not my_g & (state[floor]-move[0]):
				return False

		# if I am on the new floor...
		floor = state[E]+move[1]
		if m & (state[floor]+move[0]):
			# and another generator is with me and my generator is not
			if (g_mask-my_g) & (state[floor]+move[0]) and not my_g & (state[floor]+move[0]):
				return False
	return True

def solve(state,end):
	global nodes_expanded
	global nodes_skipped
	global to_visit
	global visited
	moves = 0
	end = pack( end )

	# BFS across states in the to_visit priority queue (number of moves to get to state is priority)
	while to_visit:
		moves,neighbor=heappop( to_visit )

		new_states=moves_from( neighbor )

		# iterate across all the possible states reachable from this neighbor
		for next in new_states:
			# if the state is not equivalent to another
			tmp=pack( next ) # not recalculating pack() saves ~ 0.5s in part 1!
			if tmp == end:
				return moves + 1
			if not tmp in visited:
				visited.add( tmp )
				heappush( to_visit, ( moves+1,next ) )
				nodes_expanded += 1
			else:
				nodes_skipped += 1

to_visit=[(0,state)]
heapify( to_visit )
visited=set([])

print "Starting:", state
print "%d moves needed to solve" % solve(state,end)
print "%d nodes expanded" % nodes_expanded
print "%d nodes skipped" % nodes_skipped

sys.exit(0)
