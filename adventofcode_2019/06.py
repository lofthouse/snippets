#! /usr/bin/env python3
import os
import sys
from anytree import Node, RenderTree, Walker

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


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

#    print( RenderTree( root ) )

    orbits = 0

    for n in root.descendants:
        orbits += n.depth

    print( "There are", orbits, "orbits" )

    w = Walker()

    result = w.walk( nodes[ "YOU" ].parent, nodes[ "SAN" ].parent )

    print( "It takes", len( result[0] ) + len( result[2] ), "steps to get from YOU to SAN" )



if __name__ == "__main__":
    main()
