#!/usr/bin/env python

import sys
import os.path
from operator import add

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

count=0
sides=[[],[],[]]
row=0

for line in content:
	sides[row%3]=map(int,line.split())

	if row%3 == 2:
		rotated = [ list(a) for a in zip(*sides[::-1]) ]

		for testrow in range(3):
			rotated[testrow].sort()
			if rotated[testrow][2] < (rotated[testrow][1] + rotated[testrow][0]):
				count += 1
	row += 1

print "There are",count,"possible triangles"

sys.exit(0)
