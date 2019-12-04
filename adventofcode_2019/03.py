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

def segments( instructions ):
    here = (0,0)
    lines = set()

    for step in instructions.split(","):
        m,d = step[0],int( step[1:] )
        there = ( here[0] + d*moves[m][0], here[1] + d*moves[m][1] )

        # Always in in closest,farthest point pair format
        lines.add( (min(here,there),max(here,there)) )
        here=there

    return lines

def intersection( a, b ):
    # Both Vertical
    if a[0][0] == a[1][0] and b[0][0] == b[1][0]:
        # Colinear
        if a[0][0] == b[0][0]:
            # Overlapping
            if a[0][1] > b[0][1] and a[0][1] < b[1][1] or\
               a[1][1] > b[0][1] and a[1][1] < b[1][1]:
                # y value is 2nd in sorted set of 4 y values
#                print( "I believe that",a,"and",b,"are vertical colinear and overlapping" )
                return ( a[0][0], sorted( [ j for i,j in a+b ] )[1] )
            else:
                return False
        else:
            return False

    # Both Horizontal
    if a[0][1] == a[1][1] and b[0][1] == b[1][1]:
        # Colinear
        if a[0][1] == b[0][1]:
            # Overlapping
            if a[0][0] > b[0][0] and a[0][0] < b[1][0] or\
               a[1][0] > b[0][0] and a[1][0] < b[1][0]:
                # y value is 2nd in sorted set of 4 x values
#                print( "I believe that",a,"and",b,"are horizontal colinear and overlapping" )
                return ( sorted( [ i for i,j in a+b ] )[1], a[0][1] )
            else:
                return False
        else:
            return False

    # Perpendicular
    # Crossing
    if a[0][0] < b[0][0] and a[1][0] > b[0][0] and a[0][1] > b[0][1] and a[0][1] < b[1][1] or\
       b[0][0] < a[0][0] and b[1][0] > a[0][0] and b[0][1] > a[0][1] and b[0][1] < a[1][1]:
        # intersection is double value in each sorted list of x/y coordinates
#        print( "I believe that",a,"and",b,"are perpendicular and crossing" )
        return ( sorted( [i for i,j in a+b ] )[1], sorted( [j for i,j in a+b ] )[1] )
    else:
        return False

def main():
    lines = readfile()

    a = segments( lines[0] )
    b = segments( lines[1] )

    intersections = set()

    for seg_a in a:
        for seg_b in b:
            intersections.add( intersection( seg_a, seg_b ) )

    intersections.discard( False )
#    print( "Intersections:", intersections )

    closest = min(intersections, key = lambda pair: abs(pair[0]) + abs(pair[1]) )

    print( "The closest point is", closest, "at a distance of", sum([ abs(k) for k in closest ]) )



if __name__ == "__main__":
    main()
