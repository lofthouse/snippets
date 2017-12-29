#!/usr/bin/env python
import sys
import os
from collections import defaultdict

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <input file> <bursts>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    bursts = int(sys.argv[2])

    if not (bursts > 0):
        print "%s is not a valid burst count" % sys.argv[2]
        sys.exit(1)

    return (input,bursts)

# Begin actual code

def main():
    # 0 = clean (default)
    # 1 = weakened
    # 2 = infected
    # 3 = flagged
    nodes = defaultdict(int)

    input,bursts = getArgs()

    grid_max = ( len(input[0]) - 1 ) / 2
    r = grid_max
    c = -grid_max

    for line in input:
        for char in line:
            if char == '#':
                nodes[ (r,c) ] = 2
            c = c + 1
        r = r - 1
        c = -grid_max

    # direction 0 = forward = moves[0]
    # ++direction === turn right
    # not using:
    # moves = [ (1,0), (0,1), (-1,0), (0,-1) ]
    # with a separate 0 or 1 index in lines 85/86
    # saves an extra ~0.4 second
    rmoves = [ 1, 0, -1, 0 ]
    cmoves = [ 0, 1, 0, -1 ]
    direction = 0
    position = [0,0]
    infections = 0

    # xrange saves ~1 second over range
    for i in xrange( bursts ):
        # not using tuple(position) saves about 1 second
        here = ( position[0], position[1] )
        node = nodes[ here ]

        # weakened => becomes infected
        if node == 1:
            infections = infections + 1

        # Thanks for ordering states linearly with movements in CW order!!!
        direction = ( direction + node - 1 ) % 4

        # work up through the states!
        nodes[ here ] = ( node + 1 ) % 4

        # not using:
        # position = [sum(x) for x in zip(position,moves[direction]) ]
        # saves nearly 9 seconds!
        position[0] = position[0] + rmoves[direction]
        position[1] = position[1] + cmoves[direction]

    print "I have caused %d node infections" % infections

if __name__=='__main__':
    main()
