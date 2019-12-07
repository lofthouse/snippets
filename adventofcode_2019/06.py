#! /usr/bin/env python3
import argparse
from anytree import Node, RenderTree, Walker

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 06')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def main():
    lines = readfile()
    nodes = {}

    for line in lines:
        p,c = line.split(")")
        if p not in nodes:
            nodes[ p ] = Node( p )

        if c in nodes:
            nodes[ c ].parent = nodes[ p ]
        else:
            nodes[ c ] = Node( c, parent=nodes[p] )

    root = nodes[ c ].root

    if args.verbose:
        print( RenderTree( root ) )

    # Part 1
    orbits = 0
    for n in root.descendants:
        orbits += n.depth
    print( "There are", orbits, "orbits" )

    # Part 2
    w = Walker()
    result = w.walk( nodes[ "YOU" ].parent, nodes[ "SAN" ].parent )
    print( "It takes", len( result[0] ) + len( result[2] ), "steps to get from YOU to SAN" )

if __name__ == "__main__":
    main()
