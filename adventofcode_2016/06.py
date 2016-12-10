#!/usr/bin/env python

import sys
import os.path
import collections

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

columns=[collections.Counter() for i in range(8)]

for line in content:
	for i,l in enumerate(line):
		columns[i][l] += 1

password = [ i.most_common()[-1][0] for i in columns ]

print "The password is",''.join(password)

sys.exit(0)
