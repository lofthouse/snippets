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

def decoded_length(line):
	next_ins=instruction.search(line)
	if next_ins:
		ins=next_ins.group(0)
		start,end = next_ins.span()
		n,c=map(int,ins.strip('()').split('x'))
		return len(line[0:start]) + c*decoded_length(line[end:end+n]) + decoded_length(line[end+n:])
	else:
		return len(line)

for line in content:
	print "The output is", decoded_length(line), "characters long"

sys.exit(0)
