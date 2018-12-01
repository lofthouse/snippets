#! /usr/bin/env python3

import os
import sys
from itertools import combinations
from operator import mul

def readinput():
    if len(sys.argv) != 2:
        print( "Missing input filename!" )
        sys.exit(1)
    if not os.path.isfile( sys.argv[1] ):
        print( f"{sys.argv[1]} is not a valid file!" )
        sys.exit(1)

    with open( sys.argv[1] ) as input_file:
        lines = input_file.read().splitlines()

    return lines

def vol(x):
    v = 1
    for y in x:
        v *= y
    return v

def main():
    lines = readinput()

    area = 0
    length = 0

    for line in lines:
        dims = sorted([ int(x) for x in line.split('x') ])
        areas = sorted( [ x*y for x,y in combinations( dims,2 ) ] )

        area += 2*sum( areas ) + areas[0]
        length += 2*sum( dims[:2] ) + vol(dims)

    print( f"The elves should order {area} square feet of wrapping paper" )
    print( f"The elves should order {length} feet of ribbon" )

if __name__ == "__main__":
    main()
