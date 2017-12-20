#!/usr/bin/env python

import sys
import os.path
from math import sqrt

if len(sys.argv) != 2 :
    print "Invalid argument"
    print "%s <origin square for data>" % sys.argv[0]
    sys.exit(1)

try:
    data_square = int(sys.argv[1])
except:
    print "%s is not a valid integer" % sys.argv[1]
    sys.exit(1)

layer = 0
x = 0
y = 0
cursor = 1

grid = {}
grid[x,y] = 1
part2_complete = False

while cursor != data_square:
    # increment the cursor.  There are 5 possible "correct" movements
    # the movement must be determined first BEFORE we increment the cursor!

    # We have finished the circuit of a layer:  layer up!
    if x == layer and y == -layer:
        layer = layer + 1
        x = x + 1
    # Right side:  move up
    elif x == layer and y != layer:
        y = y + 1
    # Top side: move left
    elif y == layer and x != -layer:
        x = x - 1
    # Left side: move down
    elif x == -layer and y != -layer:
        y = y - 1
    # Bottom side: move right
    elif y == -layer and x != layer:
        x = x + 1

    cursor = cursor + 1
    cell_value = 0

    # add up all neighboring cells (if present)
    for xi in range(-1,2):
        for yi in range(-1,2):
            if (x+xi,y+yi) in grid:
                cell_value = cell_value + grid[x+xi,y+yi]

    grid[x,y] = cell_value

    if not part2_complete and cell_value > data_square:
        print "Part 2:  attempted to write %d at cell %d, which is greater than %d" % (cell_value,cursor,data_square)
        part2_complete = True

print "%d is at %d,%d for a Manhattan Distance of %d" % (data_square,x,y,abs(x)+abs(y))
