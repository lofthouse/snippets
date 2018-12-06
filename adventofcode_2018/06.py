#! /usr/bin/env python3
import os
import sys
from pprint import pprint

max = 10
grid = [ [ [-1,0] for i in range(max) ] for j in range(max) ]
infinite = set()

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def mark( x,y,i,d ):
    if x <= 0 or y <= 0 or x >= max or y >= max:
        infinite.add( i )
        return True
    print( f"Marking {x},{y} for {i} at {d}" )
    # tie case:  it goes to nobody
    if grid[x][y][1] == d:
        grid[x][y][0] = -1
        return False
    # already claimed, move along
    elif grid[x][y][0] > 0 and grid[x][y][1] < d:
        return False
    else:
        grid[x][y] = [i,d]
        return True

def main():
    lines = readfile()

    locations = []

    for i,coord in enumerate(lines):
        x,y = coord.split(',')
        x = int(x)
        y = int(y)
        locations.append( (x,y) )
        grid[x][y] = [i,0]
    
    pprint( grid )
    pprint( locations )

    marked = True
    distance = 0
    while marked and distance < 2*max:
        marked = False
        distance += 1
        for i,home in enumerate(locations):
            for x in range(home[0]-distance,home[0]+distance):
                marked = mark(x,y+distance,i,distance) or marked
            for y in range(home[1]-distance,home[1]+distance):
                marked = mark(x-distance,y,i,distance) or marked
            for x in range(home[0]-distance+1,home[0]+distance+1):
                marked = mark(x,y-distance,i,distance) or marked
            for y in range(home[1]-distance+1,home[1]+distance+1):
                marked = mark(x+distance,y,i,distance) or marked
    
    pprint( grid )

    scores = [ 0 for i in range( len( locations ) )]
    for x in range(10):
        for y in range(10):
            if grid[x][y][0] > 0:
                scores[ grid[x][y][0] ] += 1

    pprint( scores )

if __name__ == "__main__":
    main()
