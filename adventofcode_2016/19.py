#!/usr/bin/env python

import sys
if len(sys.argv) == 2 and str.isdigit(sys.argv[1]):
	elves=int(sys.argv[1])
else:
	print "Need to know how many elves are playing!"
	sys.exit(0)

count=4
mid=3
high=9

# A Beautiful Sequence!  Beginning at 4 elves = 1, count by 1 to 3 then by 2 to 9.
# Repeat for increasing powers of 3

while ( count <= elves ):
	step=0
	while ( step < mid and count <= elves ):
		step += 1
		count += 1
	while ( step < high and count <= elves ):
		step += 2
		count += 1
	mid *= 3
	high *= 3

print step

sys.exit(0)
