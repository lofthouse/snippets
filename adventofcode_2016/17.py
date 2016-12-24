#!/usr/bin/env python

import sys
from heapq import heapify,heappush,heappop
from hashlib import md5

if len(sys.argv) == 2:
	passcode=sys.argv[1]
else:
	print "Need to know the passcode!"
	sys.exit(0)

def isLockedOrWall(coord,passcode,movement):
	opencodes='bcdef'
	index='UDLR'.index(movement)

	if coord[0]<0 or coord[1]<0 or coord[0]>3 or coord[1]>3:
		return True

	return not md5(passcode).hexdigest()[index] in opencodes

def tryPoint(moves,coord,path,passcode,movement):
	global visited,todo,end,paths,found_shortest

	if not isLockedOrWall(coord,passcode,movement):
		if coord == end:
			if not found_shortest:
				found_shortest=True
				print "The shortest path was %s moves: %s" % (moves,path)
			else:
				paths.add(moves)
		else:
			heappush(todo,(moves,coord,path,passcode+movement))
todo=[]
heapify(todo)
paths=set()
found_shortest=False
end=[3,3]
vectors={'U':[0,-1],'D':[0,1],'L':[-1,0],'R':[1,0]}

heappush(todo,(0,[0,0],'',passcode))
while todo:
	moves,coord,path,passcode=heappop(todo)
	for vector in 'UDLR':
		tryPoint(moves+1,map(sum,zip(coord,vectors[vector])),path+vector,passcode,vector)

print "The longest path was: %s moves" % max(paths)
sys.exit(0)
