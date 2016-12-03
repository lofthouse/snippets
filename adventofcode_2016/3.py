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

for line in content:
	sides=map(int,line.split())
	sides.sort()
	if sides[2] < (sides[1] + sides[0]):
		count += 1

print "There are",count,"possible triangles"

sys.exit(0)
