#!/usr/bin/env python

import sys
import os.path

if len(sys.argv) != 2 :
    print "Invalid argument"
    print "%s <number> <file containing number>" % sys.argv[0]
    sys.exit(1)

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as input_file:
        input = input_file.read().splitlines()[0]
else:
    input = sys.argv[1]

part = 1

for offset in (1, len(input)/2):
    sum = 0

    for pair in zip(input,input[-offset:] + input[:-offset]):
        if pair[0] == pair[1]:
            sum += int(pair[0])

    print "Part %d: %d" % (part,sum)

    part += 1
