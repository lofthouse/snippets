#!/usr/bin/env python

import sys
import os.path
from itertools import product

if len(sys.argv) < 2:
	print "Usage:  22.py <instruction file>"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

content=[line.split() for line in content]
nodes={}
viable_pairs=set()
X=0
Y=0

for line in content:
	if line[0][0] != '/':
		continue
	tmp=line[0].split('-')
	x=int( tmp[1][1:] )
	y=int( tmp[2][1:] )
	X=max(x,X)
	Y=max(y,Y)
	size,used,avail=[ int(e[:-1]) for e in line[1:4] ]

	nodes[ (x,y) ]=(size, used, avail)

X+=1
Y+=1

for A,B in product( [node for node in nodes], repeat=2 ):
	if nodes[A][1] != 0:
		if A != B:
			if nodes[A][1] <= nodes[B][2]:
				viable_pairs.add( (A,B) )

#print viable_pairs
print "The grid is %d wide by %d tall" % (X,Y)
print "There are %d viable pairs" % len(viable_pairs)


for node in sorted(nodes.iterkeys()):
	if nodes[node][1] == 0:
		print '_',
	elif node==(X-1,0):
		print 'G',
	elif node==(0,0):
		print 'O',
	elif nodes[node][1] > 75:
		print '#',
	else:
		print '.',

	if node[1] == Y-1:
		print

print '''
69 moves to position empty in front of goal node
5 moves to advance goal node 1 step towards origin and reposition empty
31 total steps up required
1 last step to move goal onto empty (at origin)
69 + 5*31 + 1 = 225
'''

sys.exit(0)
