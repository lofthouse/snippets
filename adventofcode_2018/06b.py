#! /usr/bin/env python3
import os
import sys

# size of square grid, and the list of points that spill to infinity
maximum = 400
infinite = set()

grid = [ [ -1 for i in range(maximum) ] for j in range(maximum) ]
locations = []

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

# tags the grid at x,y as safe (1) or not (0)
def safe(x,y):
    d = 0
    for i in range( len(locations) ):
        d += abs( x-locations[i][0] ) + abs( y-locations[i][1] )
    return( d < 10000 )

def main():
    lines = readfile()

    # store all the points in locations
    for i,coord in enumerate(lines):
        x,y = [ int(temp) for temp in coord.split(',') ]
        locations.append( (x,y) )
        grid[x][y] = i

    tot = 0
    # walk the grid and sum the safe values
    for x in range(maximum):
        for y in range(maximum):
            tot += safe(x,y)
    print( tot )

if __name__ == "__main__":
    main()
