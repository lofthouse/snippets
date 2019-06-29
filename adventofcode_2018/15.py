#! /usr/bin/env python3
import os
import sys
from pprint import pprint
import heapq

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
    type = ''
    location = ''
    coverage = set()
    in_range = set()
    reachable = dict()
    to_reach_from = []

    def __init__(self,t,loc):
        self.type=t
        self.location=loc

    def attack( self ):
        return

    def findReachable( self ):
        while self.to_reach_from and self.coverage:
            to_here,origin = heapq.heappop( self.to_reach_from )

            self.coverage.discard( origin )
            # once we've touched every in-range location, no point in proceeding
            if self.coverage:
                for next in adjacents( origin ):
                    # use opens?
                    if next in walls or next in warriors:
                        pass
                    else:
                        if next not in self.reachable or len( self.reachable[ next ] ) > (to_here + 1):
                            self.reachable[ next ] = self.reachable[ origin ].copy()
                            self.reachable[ next ].append( next )
                            heapq.heappush(self.to_reach_from,(to_here+1,next))

    def move( self ):
        self.reachable = dict()
        # reachable will be a dict of move lists:  len(reachable(location)) = moves to reach
        self.coverage = self.in_range.copy()
        self.reachable[ self.location ] = []
        self.to_reach_from = []
        heapq.heappush(self.to_reach_from,(0,self.location))
        self.findReachable()

        print( "These are the places I can reach:" )
        pprint( self.reachable )

        return

    def takeTurn( self ):
        targets = set()
        self.in_range = set()

        for warrior in warriors:
            if warriors[ warrior ].type != self.type:
                targets.add( warrior )

        if not targets:
            return False
            # War is over!!!

        print( self.type," here at ",self.location )
        print( "I can attack:" )
        pprint( targets )

        for target in targets:
            for loc in adjacents( target ):
                if loc not in warriors and loc not in walls:
                    self.in_range.add( loc )

        print( "These are the places I can attack from:" )
        pprint( self.in_range )

        if not self.in_range:
            return True
            # Nothing for me to do

        if self.location in self.in_range:
            self.attack()
        else:
            self.move()

        return True



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

def attack():
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
                warriors[ (j,i) ] = warrior(element,(j,i))

    x = i + 1
    y = j + 1

    printgrid()
    round = 0
    complete = True

    for j,i in warriors:
        if not warriors[ (j,i) ].takeTurn():
            complete = False
            break

    if complete:
        round += 1

    print( round," complete rounds were fought" )

if __name__ == "__main__":
    main()
