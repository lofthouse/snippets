#!/usr/bin/env python

import sys
import os.path
from time import sleep
from heapq import heapify,heappop,heappush
from itertools import combinations,permutations

if len(sys.argv) < 2:
	print "Usage:  24.py <map file> [graph]"
	sys.exit(1)

if len(sys.argv) == 3:
	graph = True
else:
	graph = False

def loadMap():
	with open(sys.argv[1]) as input_file:
		content = input_file.read().splitlines()

	x=0
	walls=set()
	checkpoints={}

	for x in range( len(content) ):
		for y in range( len(content[x]) ):
			if content[x][y]=='#':
				walls.add((x,y))
			if content[x][y].isdigit():
				checkpoints[ int(content[x][y]) ]=(x,y)

	return ( len(content), len(content[0]), walls, checkpoints )

def costEstimate( orig, dest ):
	return sum( [ abs(a-b) for (a,b) in zip(orig,dest) ] )

def findDistances(X, Y, walls, checkpoints):
	global graph
	pairs = combinations( range( max(checkpoints)+1 ), 2 )
	result={}

	for pair in pairs:
		distance = shortestPath(X, Y, pair, walls, checkpoints)
		result[ pair ] = distance
		result[ pair[::-1] ] = distance
		if graph:
			print pair,":",distance
			sleep(1)

	return result

def movesFrom( location, walls , visited ):
	result=[]
	for candidate in [ tuple( map( sum, zip( location, d ))) for d in [(-1,0),(1,0),(0,-1),(0,1)] ]:
		if candidate not in walls and candidate not in visited:
			result.append( candidate )
	return result

def printProgress( X, Y, walls, checkpoints, visited ):
	os.system('clear')

	for x in range(X):
		for y in range(Y):
			if (x,y) in walls:
				sys.stdout.write('#')
			elif (x,y) in visited:
				sys.stdout.write('*')
			else:
				sys.stdout.write(' ')
		sys.stdout.write('\n')

def shortestPath( X, Y, pair, walls, checkpoints ):
	global graph
	orig,dest=pair

	todo=[]
	heapify(todo)
	visited=set()
	v_count=0
	p_count=0

	heappush( todo, (0,0,checkpoints[ orig ]) )

	while todo:
		_,cost,location=heappop( todo )
		if location in visited:
			p_count+=1
			continue
		visited.add( location )

		if graph:
			if len(visited) % 50 == 0:
				printProgress(X, Y, walls, checkpoints, visited)
				print "%d nodes processed" % len(visited)
				print "%d jobs pruned" % p_count
				sleep(0.05)

		if location == checkpoints[ dest ]:
			return cost
		for new_location in movesFrom( location, walls , visited ):
			heappush( todo, (cost+costEstimate( new_location, checkpoints[ dest ] ), cost+1, new_location ) )

def main():
	X,Y,walls,checkpoints=loadMap()
	distances=findDistances( X, Y, walls, checkpoints )
	path_lengths={}

	for path in permutations( range( 1, max(checkpoints)+1 ), max(checkpoints) ):
		path = (0,)+path+(0,)
		length = 0
		for i in range( len(path) - 1 ):
			length += distances[ (path[i],path[i+1]) ]
		path_lengths[path] = length
	winner = min(path_lengths, key=path_lengths.get)
	print "The shortest path",winner,"is",path_lengths[ winner ]

if __name__=='__main__':
	main()

