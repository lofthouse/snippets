#! /usr/bin/env python3
import os
import sys
from pprint import pprint

# To facilitate reading order, all coordinates are are flipped when storing
# x,y -> foo[ (y,x) ]

moves = [ (-1,0),(0,-1),(0,1),(1,0) ]
opens = set()
walls = set()
warriors = dict()
x = 0
y = 0
hp_max = 300

class warrior:
    ap = 3
    hp = hp_max

    def __init__(self,t):
        self.type=t

    def takeTurn(self,j,i):
        targets = set()

        for warrior in warriors:
            if warriors[ warrior ].type != self.type:
                targets.add( warrior )

        if not targets:
            return False
            # War is over!!!

        print( self.type," here at (",i,",",j,")" )
        print( "I can attack:" )
        pprint( targets )


        return True



#        make superlist of in-range locations
#
#        if null set:
#            end turn
#        elif (j,i) in set:
#            attack the weakest link
#        else:
#            move!!!!!!



#        vhp = hp_max + 1
#
#        for loc in adjacents( (j,i) ):
#            # moves is in reading order, so so is this list
#            if loc in warriors:
#                if warriors[ loc ].hp < vhp:
#                    victim = loc
#                    vhp = warriors[ loc ].hp
#        if vhp <= hp_max:
#            attack( victim )



def adjacents( loc ):
    return [ tuple(a+b for a,b in zip( loc, move )) for move in moves ]

def attack( loc ):
    print( "Victim at ",loc," is under attack!" )

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
    round = 0
    complete = True

    for j,i in warriors:
        if not warriors[ (j,i) ].takeTurn(j,i):
            complete = False
            break

    if complete:
        round += 1

    print( round," complete rounds were fought" )

if __name__ == "__main__":
    main()
