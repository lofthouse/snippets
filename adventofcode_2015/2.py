#!/usr/bin/env python

import sys
import os.path
import itertools

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

paper_order = 0
ribbon_order = 0

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

for line in content:
	dims=line.split('x')
	dimensions=tuple(sorted(map(int, dims)))
	sides=itertools.combinations(dimensions,2)
	areas=tuple(x*y for x,y in sides)
	l,w,d=dimensions

	paper_order += min(areas) + 2*sum(areas)
	ribbon_order += 2*l+2*w+l*w*d

print "The elves should order", paper_order, "square feet of paper"
print "The elves should order", ribbon_order, "feet of ribbon"

sys.exit(0)
