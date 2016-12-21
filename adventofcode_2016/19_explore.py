#!/usr/bin/env python

import sys
if len(sys.argv) == 2 and str.isdigit(sys.argv[1]):
	elves=int(sys.argv[1])
else:
	print "Need to know how many elves are playing!"
	sys.exit(0)

table=[x for x in range(elves)]
n=elves

# A brute force tool to display the sequence from which we can deduce a more
# efficient way to calculate a given a(n)

while ( n > 1 ):
	table=table[1:n/2]+table[n/2+1:]+table[:1]
#	print table
	n -= 1

print table[0]+1

sys.exit(0)
