#! /usr/bin/env python3
import os
import sys

def abort( msg ):
    print( msg )
    exit( -1 )

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        lines = in_file.read().splitlines()

    clay = set()
    x_range = set()
    y_range = set()
    x_min = x_max = 500
    # These are intentionally backwards: we're ONLY allowed to use the valid clay range!
    y_min = 9999
    y_max = 0

    for line in lines:
        A,B = line.split(", ")
        a_i = int( A.split("=")[1] )
        b_min,b_max = [ int(j) for j in B.split("=")[1].split("..") ]

        if line.startswith("x"):
            x_min = min( x_min, a_i )
            x_max = max( x_max, a_i )
            y_min = min( y_min, b_min )
            y_max = max( y_max, b_max )
            for j in range( b_min, b_max+1 ):
                clay.add( (a_i,j) )
        else:
            x_min = min( x_min, b_min )
            x_max = max( x_max, b_max )
            y_min = min( y_min, a_i )
            y_max = max( y_max, a_i )
            for i in range( b_min, b_max+1 ):
                clay.add( (i,a_i) )

    # water can flow around the sides of the extent walls:  add 1 to each side of the "world"
    for i in range( x_min-1, x_max+2 ):
        x_range.add(i)
    for j in range( y_min, y_max+1 ):
        y_range.add(j)

    return ( clay, x_range, y_range )

def takescan( clay, static, flowing, x_range, y_range ):
    for y in y_range:
        for x in x_range:
            if (x,y) in clay:
                print( '#', end='' )
            elif (x,y) in static:
                print( '~', end='' )
            elif (x,y) in flowing:
                print( '|', end='' )
            else:
                print( '.', end='' )
        print()

    input()

def neighbors( point ):
    # remember y is positive DOWN
    neighbor_list = [ (-1,0),(0,1),(1,0),(0,-1) ]
    return [ tuple(a+b for a,b in zip( point, neighbor )) for neighbor in neighbor_list ]

def flow( origin, clay, static, flowing, falls, x_range, y_range ):
    left,below,right,above = neighbors( origin )

#    print( "Neighbors of",origin,":",neighbors( origin ) )
#    print( "Static:", sorted(static) )
#    print( "Flowing:", sorted(flowing) )

    # The water either goes down...
    if below not in clay and below not in static:
        # (but only counts as "flowing" if in_range
        if origin[1] in y_range:
            flowing.add( origin )
        # (but only to the bottom of our world)
        if below[1] in y_range or below[1] < min( y_range ):
            falls.append( below )
    # or the water goes to the side
    else:
        # we have to flow left and right to determine if we go static or stay flowing
        l_flow = r_flow = True

        l = left
        b = below
        while l not in clay and ( b in clay or b in static ) and l[0] in x_range:
            l,b,r,a = neighbors( l )
        l_extent = l[0]+1

        # if we spill left, add a new flow if it's in range
        if b not in clay and b not in static:
            falls.append( b )
        # if we hit clay, flag it
        elif l in clay:
            l_flow = False
        else:
            abort( "Logic Error in left flow" )

        r = right
        b = below
        while r not in clay and ( b in clay or b in static ) and r[0] in x_range:
            l,b,r,a = neighbors( r )
        r_extent = r[0]-1

        # if we spill right, add a new flow if it's in range
        if b not in clay and b not in static:
            falls.append( b )
        # if we hit clay, flag it
        elif r in clay:
            r_flow = False
        else:
            abort( "Logic Error in right flow" )

        j = origin[1]
        for i in range( l_extent, r_extent+1 ):
            # if we're flowing, mark this level and we're done
            if l_flow or r_flow:
                flowing.add( (i,j) )
            # if NOT, mark this as static (and not flowing!)...
            else:
                static.add( (i,j) )
                flowing.discard( (i,j) )

        # ...and ADD our source back to falls resolution list now that we're marked static!!!
        if not (l_flow or r_flow):
            # (but only to the top of the world)
            if above[1] in y_range:
                falls.append( above )

def main():
    clay, x_range, y_range = readfile()
    static = set()
    flowing = set()
    # our buffer of water sources that need to be resolved
    falls = [ (500,0) ]

#    print( clay )
#    print( sorted(x_range) )
#    print( sorted(y_range) )

    while falls:
#        takescan( clay, static, flowing, x_range, y_range )
        flow( falls.pop(), clay, static, flowing, falls, x_range, y_range )

    takescan( clay, static, flowing, x_range, y_range )

    print( "The number of reachable tiles is", len(static)+len(flowing) )
    print( "The number of static tiles is", len(static) )
    print( "The number of flowing tiles is", len(flowing) )


if __name__ == "__main__":
    main()
