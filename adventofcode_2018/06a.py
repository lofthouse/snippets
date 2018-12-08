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

# returns the value to be stored in the grid at x,y:  the closest point
# ID or -1 in the event of a tie
def closest(x,y):
    min_distance = 2*maximum
    winner = -1
    tie = False
    for i in range( len(locations) ):
        d = abs( x-locations[i][0] ) + abs( y-locations[i][1] )
        if d == min_distance:
            tie = True
        if d < min_distance:
            tie = False
            min_distance = d
            winner = i

    if tie:
        return( -1 )
    else:
        return( winner )    

def main():
    lines = readfile()

    # store all the points in locations
    for i,coord in enumerate(lines):
        x,y = [ int(temp) for temp in coord.split(',') ]
        locations.append( (x,y) )
        grid[x][y] = i

    scores = [ 0 for i in range( len( locations ) ) ]

    # walk the grid and record closests, keeping score.  Anything on an edge is infinite
    for x in range(maximum):
        for y in range(maximum):
            winner = closest(x,y)
            grid[x][y] = winner
            if winner > 0:
                scores[ winner ] += 1
            if x == 0 or y == 0 or x == (maximum-1)  or y == (maximum-1):
                infinite.add( winner )

    candidates = set()
    for i in range( len(locations) ):
        if i not in infinite:
            candidates.add( scores[i] )
    print( max(candidates) )

if __name__ == "__main__":
    main()
