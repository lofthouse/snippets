#!/usr/bin/env python

import sys
import os.path
from operator import add

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

vectors={'^':(0,1),
	'>':(1,0),
	'v':(0,-1),
	'<':(-1,0)}

history=[(0,0)]
position=[0,0]

with open(sys.argv[1]) as file:
	while True:
		c = file.read(1)
		if not c or c=='\n':
			break
		step=vectors[c]
		position=tuple(map(add,position,step))

#		print "Santa is now at",position

		if not position in history:
			history.append(position)
#		else:
#			print "     Santa's been here before!"

print "Santa ended up visiting", len(history),"houses"
sys.exit(0)
