#!/usr/bin/env python

import sys
import os.path

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

print "%d instructions loaded" % len(content)

def readarg(arg):
	if arg.isdigit():
		return int(arg)
	else:
		return registers[arg]


def execute():
	global line
	global counter

	counter  += 1
	parse=content[line].split()
	cmd=parse[0]

	if cmd=='cpy':
		test=readarg(parse[1])
		registers[parse[2]]=test

	if cmd=='inc':
		registers[parse[1]] += 1

	if cmd=='dec':
		registers[parse[1]] -= 1

	if cmd=='jnz':
		test=readarg(parse[1])
		if test:
			line=line+int(parse[2])
			return

	line += 1
	return

line=0
counter=1
registers={'a':0,'b':0,'c':1,'d':0}

while line < len(content):
#	print counter,line,content[line],registers
	execute()

print counter,line,'N/A',registers
