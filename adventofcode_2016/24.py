#!/usr/bin/env python

import sys
import os.path
from time import sleep
from heapq import heapify,heappop,heappush
from itertools import combinations,permutations

if len(sys.argv) < 2:
	print "Usage:  24.py <map file> [graph]"
	sys.exit(1)

graph = True if len(sys.argv) == 3 else False
rows=0

# Read the input file and generate the walls set and checkpoints dictionary
def loadMap():
	global rows

	with open(sys.argv[1]) as input_file:
		content = input_file.read().splitlines()

	walls=set()
	checkpoints={}

	for y in range( len(content) ):
		for x in range( len(content[y]) ):
			if content[y][x]=='#':
				walls.add((x,y))
			if content[y][x].isdigit():
				checkpoints[ int(content[y][x]) ]=(x,y)

	# set the global rows so we can move the cursor off the grid later
	rows=len(content)
	return ( walls, checkpoints )

# manhatten cost
def costEstimate( orig, dest ):
	return sum( [ abs(a-b) for (a,b) in zip(orig,dest) ] )

# Generate a dict of all the shortest paths between checkpoints in the maze
def findDistances( walls, checkpoints ):
	# all the possible checkpoint pairs
	pairs = combinations( range( max(checkpoints)+1 ), 2 )
	result={}

	for pair in pairs:
		distance = shortestPath( pair, walls, checkpoints)
		result[ pair ] = distance
		# go ahead and store the reverse pair, too:  it makes the final step simpler
		result[ pair[::-1] ] = distance

	return result

# Generate a list of valid coordinates from the provided location
def movesFrom( location, walls, visited ):
	result=[]
	# just an elegant way of adding the 4 possible movements to our location and creating the 4 results
	for candidate in [ tuple( map( sum, zip( location, d ))) for d in [(-1,0),(1,0),(0,-1),(0,1)] ]:
		if candidate not in walls and candidate not in visited: # <- key optimization #1
			result.append( candidate )
	return result

# Useless Eye Candy
def printProgress( pair, walls, checkpoints, visited ):
	sys.stdout.write("\033[43m")
	for x,y in visited:
		sys.stdout.write("\033[%d;%dH " % (y+1,x+1)) # <- ANSI is row, column: x,y are swapped

	sys.stdout.write("\033[37;1m")
	sys.stdout.write("\033[42;1m")
	for point in pair:
		x,y=checkpoints[ point ]
		sys.stdout.write("\033[%d;%dHX" % (y+1,x+1)) # <- ANSI is row, column: x,y are swapped

	resetCursor()

# More useless Eye Candy
def printWalls( walls ):
	os.system('clear')
	sys.stdout.write("\033[47m")
	for x,y in sorted(walls):
		sys.stdout.write("\033[%d;%dH " % (y+1,x+1))
	resetCursor()

# Move the cursor off the freshly drawn map and reset everything
def resetCursor():
	global rows

	sys.stdout.write("\033[%d;0H" % (rows+1) )
	sys.stdout.write("\033[0m")
	sys.stdout.flush()

# Use A* to find the shortest path between a checkpoint pair
def shortestPath( pair, walls, checkpoints ):
	global graph
	orig,dest = [ checkpoints[a] for a in pair ]

	todo=[]
	heapify(todo)
	visited=set()

	# Seed the heap with 0 accumulated cost from origin
	heappush( todo, (0,0,orig) )

	if graph:
		printWalls( walls )

	while todo:
		# The estimated cost is only needed to order the heap:  throw it away when we pop
		_,cost,location=heappop( todo )
		if location in visited: # <- key optimization #2:  This location may have already been explored between when this job was pushed and when we popped it!
			continue
		visited.add( location )

		if graph and len(visited) % 40 == 0:
			printProgress( pair, walls, checkpoints, visited) # <- Don't you wish you were writing this OO now?
			sleep(0.02)

		if location == dest:
			return cost # <- We're here:  just return the total cost

		for new_location in movesFrom( location, walls , visited ):  # V it will have taken one more move from the new_location when we try it
			heappush( todo, (cost+costEstimate( new_location, dest ), cost+1, new_location ) ) # <- estimate the total cost for each new location and push it on the queue

def main():
	# Compute distances for the map
	walls,checkpoints=loadMap()
	distances=findDistances( walls, checkpoints )

	# Then all we have to do is find the minimum for the possible permutations of checkpoints
	for end in ((),'without returning home'),((0,),'if we return back to point 0'):
		path_lengths={}
		for path in permutations( range( 1, max(checkpoints)+1 ), max(checkpoints) ):
			path = (0,) + path + end[0] # <- start and end at point 0
			length = 0
			for i in range( len(path) - 1 ): # we'll add the distance for point a to point a+1, so don't run off the end!
				length += distances[ (path[i],path[i+1]) ] # <- Add up all the path lengths in order for this permutation
			path_lengths[path] = length

		# Now just pull the shortest path
		winner = min(path_lengths, key=path_lengths.get) # <- We need the minimum value, not the minimum key
		print "The shortest path",winner,"is",path_lengths[ winner ],end[1]

if __name__=='__main__':
	main()
