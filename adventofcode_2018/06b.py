#! /usr/bin/env python3
import os
import sys
from pprint import pprint

maximum = 400
grid = [ [ -1 for i in range(maximum) ] for j in range(maximum) ]
locations = []
infinite = set()

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def closest(x,y):
    distance = 2*maximum
    winner = -1
    tie = False
    d = 0
    for i in range( len(locations) ):
        d += abs( x-locations[i][0] ) + abs( y-locations[i][1] )
    if d < 10000:
        return( 1 )
    else:
        return( 0 )    

def main():
    lines = readfile()

    for i,coord in enumerate(lines):
        x,y = coord.split(',')
        x = int(x)
        y = int(y)
        locations.append( (x,y) )
        grid[x][y] = i

    for x in range(maximum):
        for y in range(maximum):
            grid[x][y] = closest(x,y)
            if x == 0 or y == 0 or x == (maximum-1)  or y == (maximum-1):
                infinite.add( grid[x][y] )

    scores = [ 0 for i in range( len( locations ) ) ]
    tot = 0
    for x in range(maximum):
        for y in range(maximum):
            tot += grid[x][y]

    print( tot )

if __name__ == "__main__":
    main()
