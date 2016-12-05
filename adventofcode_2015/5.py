#!/usr/bin/env python

import sys
import os.path
import collections

count=0

# Check every pair against the remainder of the line
def hasdoublepair(line):
	for n in range(len(line)-3):
		if line[n:n+2] in line[n+2:] :
			return True
	return False

# Check every letter against the letter 2 ahead
def hasoffsetpair(line):
	for n in range(len(line)-2):
		if line[n] == line[n+2]:
			return True
	return False

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

for line in content:
	if hasdoublepair(line) and hasoffsetpair(line) :
		count += 1

print "There are",count,"nice lines"

sys.exit(0)
