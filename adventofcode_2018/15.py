#! /usr/bin/env python3
import os
import sys
from pprint import pprint

# To facilitate reading order, all coordinates are are flipped when storing
# x,y -> foo[ (y,x) ]

opens = set()
walls = set()
warriors = dict()
x = 0
y = 0

class warrior:
    ap = 3
    hp = 300

    def __init__(self,t):
        self.type=t

def printgrid():
    for j in range(y):
        for i in range(x):
            if (i,j) in walls:
                print('#',end='')
            if (i,j) in opens:
                print('.',end='')
            if (i,j) in warriors:
                print(warriors[ (i,j) ].type,end='')

        print('  ', end='')

        for i in range(x):
            if (i,j) in warriors:
                print(warriors[ (i,j) ].type,'(',warriors[ (i,j) ].hp,'), ',end='')

        print('')


def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    global x
    global y
    lines = readfile()
    for j,line in enumerate(lines):
        for i,element in enumerate(line):
            if element == ".":
                opens.add( (i,j) )
            elif element == "#":
                walls.add( (i,j) )
            else:
                warriors[ (i,j) ] = warrior(element)

    x = i + 1
    y = j + 1

    printgrid()

    pprint( warriors )
    pprint( sorted(warriors) )
    pprint( warriors )


if __name__ == "__main__":
    main()
