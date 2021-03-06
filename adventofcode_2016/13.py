#!/usr/bin/env python

import sys
from heapq import heapify,heappush,heappop

if len(sys.argv) == 2 and str.isdigit(sys.argv[1]):
	d=int(sys.argv[1])
else:
	print "Need to know the designer's favorite number!"
	sys.exit(0)

def isWall(x,y,d):
	if x<0 or y<0:
		return True
	return bin(x*x + 3*x + 2*x*y + y + y*y + d).count('1') % 2 == 1

def printMap(h,v,d):
	for y in range(v):
		for x in range(h):
			if isWall(x,y,d):
				print '#',
			else:
				print ' ',
		print

def tryPoint(x,y,moves):
	global visited,reachable,todo,end,d

	if moves>50:
		return

	here=(x,y)
	if here in visited:
		return
	visited.add(here)

	if not isWall(x,y,d):
		reachable.add(here)
		heappush(todo,(moves,here))

visited=set()
reachable=set()
todo=[]
heapify(todo)

start=(1,1)

heappush(todo,(0,start))
reachable.add(start)
printMap(40,50,d)

while todo:
	moves,(x,y)=heappop(todo)
	for new_x in x-1,x+1:
		tryPoint(new_x,y,moves+1)
	for new_y in y-1,y+1:
		tryPoint(x,new_y,moves+1)

print "We reached %d points" % len(reachable)
