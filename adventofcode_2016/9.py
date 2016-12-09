#!/usr/bin/env python

import sys
import os.path
import re

instruction=re.compile('\([0-9]+x[0-9]+\)')
output=''

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

for line in content:
	output=''
#	print
#	print "New Line:",line
	while line:
#		print "In:",line
#		print "Out:",output
		next_ins=instruction.search(line)
		if next_ins:
			ins=next_ins.group(0)
			start,end = next_ins.span()
#			print "Found instruction",ins
			output += line[0:start]
			line = line[end:]
			n,c=map(int,ins.strip('()').split('x'))
			output += line[0:n]*c
			line = line[n:]
		else:
			output += line
#			print "Copied rest of line"
			line=''

#	print "The output is", output, "and is", len(output), "characters long"
	print "The output is", len(output), "characters long"

sys.exit(0)
