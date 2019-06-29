#! /usr/bin/env python3
import os
import sys
from pprint import pprint

opens = set()
walls = set()
goblins = dict()
elves = dict()

class warrior:
    ap = 3
    hp = 300

def printgrid(x,y):
    for j in range(y):
        for i in range(x):
            if (i,j) in walls:
                print('#',end='')
            if (i,j) in opens:
                print('.',end='')
            if (i,j) in goblins:
                print('G',end='')
            if (i,j) in elves:
                print('E',end='')

        print('  ', end='')

        for i in range(x):
            if (i,j) in goblins:
                print('G(',goblins[ (i,j) ].hp,'), ',end='')
            if (i,j) in elves:
                print('E(',elves[ (i,j) ].hp,'), ',end='')

        print('')


def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    x = y = 0

    lines = readfile()
    for j,line in enumerate(lines):
        for i,element in enumerate(line):
            if element == ".":
                opens.add( (i,j) )
            if element == "#":
                walls.add( (i,j) )
            if element == "G":
                goblins[ (i,j) ] = warrior()
            if element == "E":
                elves[ (i,j) ] = warrior()

    x = i + 1
    y = j + 1

    printgrid(x,y)


if __name__ == "__main__":
    main()
