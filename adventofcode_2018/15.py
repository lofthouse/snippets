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
            if (j,i) in walls:
                print('#',end='')
            if (j,i) in opens:
                print('.',end='')
            if (j,i) in warriors:
                print(warriors[ (j,i) ].type,end='')

        print('  ', end='')

        for i in range(x):
            if (j,i) in warriors:
                print(warriors[ (j,i) ].type,'(',warriors[ (j,i) ].hp,'), ',end='')

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
                opens.add( (j,i) )
            elif element == "#":
                walls.add( (j,i) )
            else:
                warriors[ (j,i) ] = warrior(element)

    x = i + 1
    y = j + 1

    printgrid()

    pprint( warriors )
    pprint( sorted(warriors) )
    pprint( warriors )


if __name__ == "__main__":
    main()
