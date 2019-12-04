#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

moves = {'R':(1,0), 'L':(-1,0), 'U':(0,1), 'D':(0,-1)}

def steps( instructions ):
    here = (0,0)
    steps = 0
    points = dict()

    for instruction in instructions.split(","):
        d,m = instruction[0],int( instruction[1:] )

        for step in range(m):
            steps += 1
            here = ( here[0] + moves[d][0], here[1] + moves[d][1] )

            if here not in points:
                points[ here ] = steps

    return points

def main():
    lines = readfile()

    a = steps( lines[0] )
    b = steps( lines[1] )

    intersections = set(a).intersection(set(b))

    closest = min(intersections, key = lambda pair: abs(pair[0]) + abs(pair[1]) )

    print( "The part 1 closest point is", closest, "at a distance of", sum([ abs(k) for k in closest ]) )

    closest = min(intersections, key = lambda pair: a[pair] + b[pair] )

    print( "The part 2 closest point is", closest, "at", a[closest] + b[closest], "total steps" )


if __name__ == "__main__":
    main()
