#!/usr/bin/env python

import sys
import os.path

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

content=[line.split() for line in content]

print "%d instructions loaded" % len(content)

def readarg(arg):
#	print "readarg here looking at",arg
	if arg[0]=='-':
		if arg[1:].isdigit():
			return -int(arg[1:])
	elif arg.isdigit():
		return int(arg)
	else:
		return registers[arg]


def execute():
	global line,content,counter,registers

	counter  += 1
	cmd=content[line][0]

	if cmd=='cpy':
		test=readarg(content[line][1])
		if content[line][2] in registers:
			registers[content[line][2]]=test

	if cmd=='inc':
		registers[content[line][1]] += 1

	if cmd=='dec':
		registers[content[line][1]] -= 1

	if cmd=='jnz':
		test=readarg(content[line][1])
		if test:
			line=line+readarg(content[line][2])
			return

	if cmd=='tgl':
		target=line+readarg(content[line][1])
		if target < len(content):
#			print "Evaluating command at",target,":",content[target]
			tcmd=content[target][0]

			if tcmd=='inc':
				content[target][0]='dec'
			elif tcmd=='dec' or tcmd=='tgl':
				print "Found dec or tgl"
				content[target][0]='inc'
			elif tcmd=='cpy':
				content[target][0]='jnz'
			elif tcmd=='jnz':
				content[target][0]='cpy'
#		else:
#			print "Out-of-range:  skipping"

	line += 1
	return

line=0
counter=1
registers={'a':12,'b':0,'c':0,'d':0}

while line < len(content):
#	print counter,"executing",content[line],"at line",line
#	print "Registers:",registers
#	for inst in content:
#		print inst
#	print
	execute()

print counter,line,'N/A',registers
