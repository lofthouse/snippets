#!/usr/bin/env python

import sys
import os.path

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

literals=0
values=0
encoded=0

for line in content:

	literals += len(line)
	values += len(line.decode('string_escape'))-2
	encoded += len(line.encode('string_escape').replace('"','\\\"'))+2
#	print "The string is %s and has length %d" % (line,len(line))
#	print "The string means %s which has length %d" % (line.decode('string_escape'),len(line.decode('string_escape'))-2)
#	print "String %s encodes to %s with length %d" % (line, line.encode('string_escape').replace('"','\\\"'), len(line.encode('string_escape').replace('"','\\\"'))+2)

print "%d characters in-file reduced to %d in memory, for a savings of %d" % (literals, values, literals-values)
print "%d characters in-file increased to %d in memory, for a cost of %d" % (literals, encoded, encoded-literals)

sys.exit(0)
