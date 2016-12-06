#!/usr/bin/env python

import sys
import os.path
import collections

count = 0
grid = [ [ 0 for i in range(1000) ] for j in range(1000) ]

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

for line in content:
	if not line :
		continue
	parse=line.split()
	if parse[0] == 'turn' :
		operation = parse[1]
		parse = parse[2:]
	else :
		operation = parse[0]
		parse = parse[1:]
	x0,y0 = map(int,parse[0].split(','))
	x1,y1 = map(int,parse[2].split(','))

	for x in range(x0,x1+1) :
		for y in range(y0,y1+1) :
			if operation == 'on' :
				grid[x][y] = 1
			if operation == 'off' :
				grid[x][y] = 0
			if operation == 'toggle' :
				grid[x][y] = 1 - grid[x][y]

print "There are",sum(sum(i) for i in grid),"lights lit"

sys.exit(0)
