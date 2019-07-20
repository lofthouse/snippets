#! /usr/bin/env python3
import os
import sys
from pprint import pprint
import heapq

# To facilitate reading order, all coordinates are are flipped when storing
# x,y -> foo[ (y,x) ]

moves = [ (-1,0),(0,-1),(0,1),(1,0) ]
#opens = set()
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
    uncoverage = set()
    in_range = set()
    reachable = dict()
    to_reach_from = []

    def __init__(self,t,loc):
        self.type=t
        self.location=loc

    def attack( self ):
        return

    def findReachable( self ):
        while self.to_reach_from and self.uncoverage:
            to_here,origin = heapq.heappop( self.to_reach_from )
            # to_here are the moves required to reach origin from our current location
            # origin is the point of origination for this round of path exploration

            self.uncoverage.discard( origin )
            # we've reached this origin, so remove it from our un-covered
            if self.uncoverage:
                # only if there are un-covered destinations remaining is there a point in looking for more paths
                for next in adjacents( origin ):
                    if next in walls or next in warriors:
                        # this path is blocked.  move along.
                        pass
                    else:
                        # there is a reachable path from this origin.  Add it to our exploration heapqueue ONLY if
                        # it hasn't been reached yet or the existing path to reach is longer than this path or if
                        # the existing path to reach it is longer than this path or
                        # the existing path to reach it is the same length but comes later in reading order
                        if next not in self.reachable or \
                            len( self.reachable[ next ] ) > (to_here + 1) or \
                            ( len( self.reachable[ next ] ) == (to_here + 1) and self.reachable[ next ][0] > self.reachable[ origin ][0] ):
                            self.reachable[ next ] = self.reachable[ origin ].copy()
                            self.reachable[ next ].append( next )
                            heapq.heappush(self.to_reach_from,(to_here+1,next))


    def move( self ):
        self.reachable = dict()
        # reachable will be a dict of move lists:  len(reachable(location)) = moves to reach location from our current location
        self.uncoverage = self.in_range.copy()
        # uncoverage is the set of in_range locations that we have NOT reached by one of our move lists
        self.reachable[ self.location ] = []
        # no moves required to reach where we are, natch
        self.to_reach_from = []
        # to_reach_from is a heapq used to track the (moves_needed_to_reach,coordinates)
        # it is the working list of points from which paths should be explored

        heapq.heappush(self.to_reach_from,(0,self.location))
        self.findReachable()

#        print( "These are the places I can reach:" )
#        pprint( self.reachable )

        destinations = set(self.reachable.keys()).intersection(self.in_range)
#        print( "These are the places I want to reach:" )
#        pprint( destinations )

#        print( "This is the best place to reach:" )
#        pprint( minpath(destinations,self.reachable) )

        step = self.reachable[ minpath(destinations,self.reachable) ][0]
#        print( "My move is to:" )
#        pprint( step )
        warriors[ step ] = warriors.pop( self.location )
        self.location = step

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

#        print()
#        print( self.type," here at ",self.location )
#        print( "I can attack:" )
#        pprint( targets )

        for target in targets:
            for loc in adjacents( target ):
                if loc == self.location or ( loc not in warriors and loc not in walls ):
                    self.in_range.add( loc )

#        print( "These are the places I can attack from:" )
#        pprint( self.in_range )

        if not self.in_range:
            return True
            # Nothing for me to do

        if self.location in self.in_range:
#            print( "I choose to attack" )
            self.attack()
        else:
#            print( "I choose to move" )
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
#    print( "Victim at ",loc," is under attack!" )
    return

def minpath( keys,paths ):
    key = (99999,99999)
    m = 9999999
    for k in keys:
#        print( "Comparing ",k," and ",key )
        if len( paths[k] ) == m:
            key = min( key, k )
        elif len( paths[k] ) < m:
            key = k
            m = len( paths[k] )
#        print( key," wins!" )

    return key

def printgrid():
    for j in range(y):
        for i in range(x):
            if (j,i) in walls:
                print('#',end='')
#            if (j,i) in opens:
            elif (j,i) in warriors:
                print(warriors[ (j,i) ].type,end='')
            else:
                print('.',end='')

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
                pass
#                opens.add( (j,i) )
            elif element == "#":
                walls.add( (j,i) )
            else:
                warriors[ (j,i) ] = warrior(element,(j,i))

    x = i + 1
    y = j + 1

    round = 0
    printgrid()
    print( round," complete rounds fought so far" )
    input()

    complete = False

    while not complete:
        # turns are taking in STARTING order only, so we have to work off a copy of that order
        turn_order = sorted( list( warriors ))
#        pprint( turn_order )

#        print( "Here are our warriors:" )
#        pprint( warriors )
#        pprint( turn_order )

        for j,i in turn_order:
#            print( "Time for (",j,",",i,") to take a turn" )

            if not warriors[ (j,i) ].takeTurn():
                complete = True
                break

        if not complete:
            round += 1

        printgrid()
        print( round," complete rounds fought so far" )
        input()

    print( round," complete rounds were fought" )

if __name__ == "__main__":
    main()
