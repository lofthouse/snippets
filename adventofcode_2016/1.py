#!/usr/bin/env python

import sys
import os.path
from operator import add

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

paper_order = 0
ribbon_order = 0

vectors=[(0,1),(1,0),(0,-1),(-1,0)]
compass=0
position=[0,0]

visited=[[0,0]]
first=True

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

directions=content[0].split(', ')

for direction in directions:
	turn=direction[:1]
	distance=int(direction[1:])

	if (turn=='R'):
		compass = ( compass + 1 ) % 4
	elif (turn=='L'):
		compass = ( compass - 1 ) % 4
	else:
		print "That's not a direction!"
		sys.exit(1)

	# The original solution used walk=[n*distance for n in vectors[compass]] and mapped that with add
	# This is brute-forcey, but gets interim positions
	# I probably should do a line test.  Yes, I should.
	for _ in range(distance):
		position = map(add, position, vectors[compass])

#		print "I'm at", position, "having followed", direction
#		print "I've visited", visited

		if position in visited and first:
			print "I've been here before:", position, "which is", sum(map(abs,position)),"blocks away"
			first = False
		elif first:
			visited.append(position)

print "Easter Bunny HQ is",sum(map(abs,position)),"blocks away"

sys.exit(0)
