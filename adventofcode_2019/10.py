#! /usr/bin/env python3
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day N')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
#parser.add_argument("x", type=int, help="the number x")
args = parser.parse_args()

# global factors lookup table used to find integer basis for all vectors
# every integer in the range 1-largest_dimension will have a factor list like
# 24: [ 1,2,3,4,6,8,12 ]
factors = {}

def readfile():
    with args.input_file as input_file:
        lines = input_file.read().splitlines()

    asteroids = set()
    global factors

    for y,line in enumerate( lines ):
        for x,state in enumerate( line ):
            if state == "#":
                asteroids.add( (x,y) )

    # build the factor table for each integer
    # 1 and (self) are trivial cases and added manually to cut comp time by 1/2!
    for i in range( 1, max(x,y) + 1 ):
        factors[i] = [ 1 ]
        for f in range( 2, i // 2 + 1 ):
            if i % f == 0:
                factors[i].append( f )
        factors[i].append( i )

    return asteroids

# return the integer basis for the vector from origin to destination
# it's the (destination-origin)/mcd where mcd is the maximum common factor
# shared by the absolute value of both coordinates of origin and destination
def basis( origin, destination ):
    global factors

    basis = [ b-a for a,b in zip( origin, destination ) ]

    # if a coordinate is 0, then scale the other axis by its mcd instead
    if all( i != 0 for i in basis ):
        if args.verbose:
            print( "Finding basis for", basis )

        mcd = max( set( factors[ abs( basis[0] ) ]).intersection( set( factors[ abs( basis[1] ) ] ) ) )
    else:
        mcd = max( factors[ max( ( abs(j) for j in basis ) ) ] )

    # integer division!  no FP ops required, since everything is integer by definition!
    # FWIW, it makes no time difference in python
    return tuple( i // mcd for i in basis )

def part_1( asteroids ):
    vis_counts = defaultdict( list )

    for home in asteroids:
        visible = set()

        for other in asteroids:
            if other != home:
                if args.verbose:
                    print( "Adding basis for", other, "from", home )

                visible.add( basis( home, other ) )

                if args.verbose:
                    print( visible )

        if args.verbose:
            print( "I can see", len( visible ), "asteroids from", home )

        vis_counts[ len( visible ) ].append( home )

        if args.verbose:
            print( vis_counts )

    best_count = max( vis_counts )

    print( "The best observatory is at", vis_counts[ best_count ], "where I can see", best_count )


def main():
    asteroids = readfile()

    part_1( asteroids )


if __name__ == "__main__":
    main()
