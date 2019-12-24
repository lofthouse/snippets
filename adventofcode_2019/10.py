#! /usr/bin/env python3
import argparse
from collections import defaultdict
from queue import PriorityQueue
from math import atan2, pi
from pprint import pprint

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 10')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
parser.add_argument("n", type=int, help="the nth asteroid to vaporize")
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

# return a value that increases from a minimum at pi/2 to a max at pi/2 - infinitesimal
# remember that the y axis is flipped in elf-land! (positive DOWN)
def heading( origin, dest ):
    return (pi/2 + atan2( dest[1]-origin[1],dest[0]-origin[0] )) % (2*pi)

def part_1( asteroids ):
    vis_counts = defaultdict( list )

    for home in asteroids:
        visible = set()

        for other in asteroids:
            if other != home:
                # just blindly store basis of all other vectors
                # duplicates (e.g. invisible) disappear into the same basis
                visible.add( basis( home, other ) )

        vis_counts[ len( visible ) ].append( home )

    best_count = max( vis_counts )

    print( "The best observatory is at", vis_counts[ best_count ][0], "where I can see", best_count )
    return vis_counts[ best_count ][0]

# for part 2, we'll re-do the math for the winner, but this time
# we'll store each point in a list in a priority queue ordered by the angle
# in radians clockwise from pi/2
# extraction then is just pop-ing one-at-a-time off each list going round
# the priority queue
def part_2( asteroids, winner ):
    starchart = defaultdict( PriorityQueue )

    for other in asteroids:
        if other != winner:
            starchart[ heading( winner, other ) ].put( ( sum( abs(b-a) for a,b in zip( winner, other ) ), other ) )

    if args.verbose:
        for r in sorted( starchart.keys() ):
            print( r,": ", starchart[ r ].queue )

    i = 0
    while True:
        for r in sorted( starchart.keys() ):
            last = starchart[ r ].get()[1]
            if starchart[ r ].empty():
                del starchart[ r ]
            i += 1
            if not i < args.n:
                print( "The", args.n, "asteroid to be obliterated was at", last, ". Submit", 100*last[0]+last[1] )
                return

def main():
    asteroids = readfile()

    winner = part_1( asteroids )
    part_2( asteroids, winner )

if __name__ == "__main__":
    main()
