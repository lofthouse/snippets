#!/usr/bin/env python

import sys
from heapq import heapify,heappush,heappop
from hashlib import md5

if len(sys.argv) == 2:
	passcode=sys.argv[1]
else:
	print "Need to know the passcode!"
	sys.exit(0)

def isLockedOrWall(x,y,passcode,movement):
	opencodes='bcdef'
	index='UDLR'.index(movement)

	if x<0 or y<0 or x>3 or y>3:
		return True

	return not md5(passcode).hexdigest()[index] in opencodes

def tryPoint(moves,x,y,path,passcode,movement):
	global visited,todo,end,paths,found_shortest

	if not isLockedOrWall(x,y,passcode,movement):
		if (x,y) == end:
			if not found_shortest:
				found_shortest=True
				print "The shortest path was %s moves: %s" % (moves,path)
			else:
				paths.add(moves)
		else:
			heappush(todo,(moves,(x,y),path,passcode+movement))
todo=[]
heapify(todo)
paths=set()
found_shortest=False
start=(0,0)
end=(3,3)
path=''
heappush(todo,(0,start,path,passcode))

while todo:
	moves,(x,y),path,passcode=heappop(todo)
	tryPoint(moves+1,x,y-1,path+'U',passcode,'U')
	tryPoint(moves+1,x,y+1,path+'D',passcode,'D')
	tryPoint(moves+1,x-1,y,path+'L',passcode,'L')
	tryPoint(moves+1,x+1,y,path+'R',passcode,'R')

print "The longest path was: %s moves" % max(paths)
sys.exit(0)
