#!/usr/bin/env python

import sys
import os.path
from itertools import permutations

if len(sys.argv) != 2 :
    print "Invalid argument"
    print "%s <file containing spreadsheet>" % sys.argv[0]
    sys.exit(1)

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as input_file:
        input = input_file.read().splitlines()
else:
    print "%s is not a file" % sys.argv[1]
    sys.exit(1)

checksum_1 = 0
checksum_2 = 0

for row in input:
    row_min = 999999
    row_max = 0
    found = False

    for column in row.split():
        row_min = min(row_min,int(column))
        row_max = max(row_max,int(column))

    checksum_1 = checksum_1 + row_max - row_min

    for pair in permutations( (int(x) for x in row.split()),2):
        if not found and ( pair[1] / pair[0] ) * pair[0] == pair[1]:
            found = True
            checksum_2 = checksum_2 + ( pair[1] / pair[0] )


print "The Part 1 Checksum is %d" % checksum_1
print "The Part 2 Checksum is %d" % checksum_2
