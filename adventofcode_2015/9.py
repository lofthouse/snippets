#!/usr/bin/env python

import sys
import os.path

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

def addCost(a,b,c):
	if not a in stations:
		stations[a]={}
	stations[a][b]=int(c)

def fare(origin,prior_visited):
	visited=list(prior_visited)
	visited.append(origin)

	# original version used a dict to track the destination with each fare.  Not needed.
	minimum_fares=[ stations[origin][destination] + fare(destination,visited) for destination in stations[origin] if destination not in visited ]

	return min(minimum_fares or [0])

stations={}

for line in content:
	buffer=line.split()
	addCost(buffer[0],buffer[2],buffer[4])
	addCost(buffer[2],buffer[0],buffer[4])

stations['home']={station:0 for station in stations}

print fare('home',[])

sys.exit(0)
