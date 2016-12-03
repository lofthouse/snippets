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
		column = [ sorted(list(a)) for a in zip(*rows) ]
		del rows[:]

		for n in range(3):
			if column[n][2] < (column[n][1] + column[n][0]):
				count += 1

print "There are",count,"possible triangles"

sys.exit(0)
