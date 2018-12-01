#! /usr/bin/env python3
import os
import sys
import numpy as np


def readfile():
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print( f"Usage:  {sys.argv[0]} <input file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as input_file:
        lines = input_file.read().splitlines()

    return lines

def main():
    paths = readfile()

    for path in paths:
        if len(paths) > 1:
            print( f"\n{path}" )

        position = [ np.array( (0,0) ), np.array( (0,0) ), np.array( (0,0) ) ]

        moves= {'^': np.array( ( 0, 1) ),
                'v': np.array( ( 0,-1) ),
                '<': np.array( (-1, 0) ),
                '>': np.array( ( 1, 0) )}

        houses = [ 0, set( [(0,0),] ), set( [(0,0),] ) ]

        turn = 1

        for step in path:
            position[0] += moves[step]
            position[turn] += moves[step]
            houses[1].add( tuple(position[0]) )
            houses[2].add( tuple(position[turn]) )
            turn = 3-turn

        for part in [1,2]:
            print( f"We visited {len(houses[part])} houses for part {part}" )

if __name__ == "__main__":
    main()
