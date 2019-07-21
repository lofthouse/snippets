#! /usr/bin/env python3
import os
import sys
from pprint import pprint
import heapq

# To facilitate reading order, all coordinates are are flipped when storing
# x,y -> foo[ (y,x) ]

killed_this_round = set()
moves = [ (-1,0),(0,-1),(0,1),(1,0) ]
#opens = set()
walls = set()
warriors = dict()
x = 0
y = 0
hp_max = 200

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
        target = (99999,99999)
        target_hp = hp_max + 1

        # adjacents gives reading order, so no further tie breaking is needed!
        for loc in adjacents( self.location ):
#            print( "Testing attackability of ",loc )
            if loc in warriors and warriors[ loc ].type != self.type:
#                print( "I could attack this...",end='' )
                if warriors[ loc ].hp < target_hp:
#                    print( "and I will" )
                    target = loc
                    target_hp = warriors[ loc ].hp
#                else:
#                    print( "but I have better options" )

#        print( "Attacking ",target )

        warriors[ target ].hp -= self.ap
        if warriors[ target ].hp <= 0:
#            print( target, "is dead, killed by", self.location )
            killed_this_round.add( target )
            del warriors[ target ]

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
#        pprint( self.reachable.keys() )

        destinations = set(self.reachable.keys()).intersection(self.in_range)

#        print( "These are the places I want to reach:" )
#        pprint( destinations )

#        print( "This is the best place to reach:" )
#        pprint( minpath(destinations,self.reachable) )

        if destinations:
            step = self.reachable[ minpath(destinations,self.reachable) ][0]
#            print( "My move is to:" )
#            pprint( step )
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

        if not self.location in self.in_range:
#            print( "I must move" )
            self.move()

        if self.location in self.in_range:
#            print( "I choose to attack" )
            self.attack()

        return True

def adjacents( loc ):
    return [ tuple(a+b for a,b in zip( loc, move )) for move in moves ]

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

def outcome( r ):
    hp_tot = 0
    for warrior in warriors:
        hp_tot += warriors[ warrior ].hp

    return r * hp_tot

def printgrid(r):
    f=open( '{:02d}'.format(r)+'_me.txt', 'w' )
    for j in range(y):
        for i in range(x):
            if (j,i) in walls:
#                print('#',end='')
                f.write('#')
#            if (j,i) in opens:
            elif (j,i) in warriors:
#                print(warriors[ (j,i) ].type,end='')
                f.write(warriors[ (j,i) ].type)
            else:
#                print('.',end='')
                f.write('.')

#        print('  ', end='')
        f.write(' ')

        f.write(', '.join( [ warriors[ (j,i) ].type + '(' + str(warriors[ (j,i) ].hp) + ')' for i in range(x) if (j,i) in warriors ] ) )
#        for i in range(x):
#            if (j,i) in warriors:
#                print(warriors[ (j,i) ].type,'(',warriors[ (j,i) ].hp,'), ',end='')
#                f.write(warriors[ (j,i) ].type + '(' + str(warriors[ (j,i) ].hp) + '), ')

#        print('')
        f.write('\n')
    f.close()


def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    global x
    global y
    global killed_this_round
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
    printgrid(round)
#    print( round," complete rounds fought so far" )
#    input()

    complete = False

    while not complete:
        # turns are taking in STARTING order only, so we have to work off a copy of that order
        turn_order = sorted( list( warriors ))
        killed_this_round = set()
#        pprint( turn_order )

#        print( "Here are our warriors:" )
#        pprint( warriors )
#        pprint( turn_order )

        for j,i in turn_order:
#            print( "Time for (",j,",",i,") to take a turn" )
            # (j,i) may have just been killed, so check first before trying to takeTurn!
            if (j,i) not in killed_this_round and not warriors[ (j,i) ].takeTurn():
                complete = True
                break

        if not complete:
            round += 1

        printgrid(round)

#        print( round," complete rounds fought so far" )
#        input()

    printgrid(round)
    print( round," complete rounds were fought" )
    print( "The outcome is ", outcome(round) )

if __name__ == "__main__":
    main()
