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

history={(0,0):1}
position=santa_position=robot_position=[0,0]
count=0

with open(sys.argv[1]) as file:
	while True:
		c = file.read(1)
		if not c or c=='\n':
			break
		count += 1
		step=vectors[c]

		if count%2 == 1:
			position=santa_position=tuple(map(add,santa_position,step))
		else:
			position=robot_position=tuple(map(add,robot_position,step))
#		print "Santa is now at",position

		if not position in history:
			history[position] = 1
		else:
			history[position] += 1

print "Santa ended up visiting", len(history),"houses"
print "Santa ended up delivering", sum(history.values()), "presents"
sys.exit(0)
