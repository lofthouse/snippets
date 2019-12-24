#! /usr/bin/env python3
import argparse
from collections import defaultdict
from queue import PriorityQueue
from math import atan2, pi

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 10')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
parser.add_argument("n", type=int, help="the nth asteroid to vaporize")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        lines = input_file.read().splitlines()

    asteroids = set()
    global factors

    for y,line in enumerate( lines ):
        for x,state in enumerate( line ):
            if state == "#":
                asteroids.add( (x,y) )

    return asteroids

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
                # just blindly store heading of all other vectors
                # duplicates (e.g. invisible) disappear into the same basis
                visible.add( heading( home, other ) )

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

    i = 0
    while True:
        # we'll be deleting empty headings, so iterate on the current list for this round
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
