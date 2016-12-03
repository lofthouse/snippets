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
rows=[]

for line in content:
	rows.append(map(int,line.split()))
	if len(rows) == 3:
		for column in map(None,*rows):
			if 2*max(column) < sum(column):
				count += 1
		del rows[:]

print "There are",count,"possible triangles"

sys.exit(0)
