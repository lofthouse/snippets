#!/usr/bin/env python

import sys
import os.path
from itertools import permutations

if len(sys.argv) != 3 :
    print "Invalid argument"
    print "%s <file containing jumps> <part>" % sys.argv[0]
    sys.exit(1)

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as input_file:
        input = input_file.read().splitlines()
else:
    print "%s is not a file" % sys.argv[1]
    sys.exit(1)

part = int(sys.argv[2])

if not (part == 1 or part == 2):
    print "%s is not a valid part" % sys.argv[2]
    sys.exit(1)

line = 0
lines = {}

for jump in input:
    lines[line] = int(jump)
    line = line + 1

step = 0
line = 0

while line in lines:
    jump = lines[line]

    step = step + 1
    if part == 2 and jump >= 3:
        lines[line] = jump - 1
    else:
        lines[line] = jump + 1
    line = jump + line

#    print lines

print "It took %d steps to escape" % step
