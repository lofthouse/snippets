#!/usr/bin/env python

import sys

if  len(sys.argv) != 3 :
	print "Invalid arguments"
	sys.exit(1)

input = sys.argv[1]
iterations = int(sys.argv[2])

for iteration in range(iterations):
	last_c=''
	output=''
	count=1
	last_c=input[0]
	for i in range(len(input)-1):
		if last_c == input[i+1]:
			count += 1
			continue
		else:
			output += str(count)+last_c
			count = 1
			last_c = input[i+1]
	output += str(count)+last_c
	input=output

print len(output)

sys.exit(0)
