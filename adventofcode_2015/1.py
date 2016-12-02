#!/usr/bin/env python

import sys

if  len(sys.argv) != 2 :
	print "Invalid argument"
	sys.exit(1)

floor=0
step=0
messaged=False

with open(sys.argv[1]) as file:
	while True:
		c = file.read(1)
		if not c:
			break
		step += 1
		if c == '(':
			floor += 1
		if c == ')':
			floor -= 1
		if floor < 0 and not messaged :
			print "Santa entered the basement on step", step
			messaged = True

print "Santa ended up on floor", floor
sys.exit(0)
