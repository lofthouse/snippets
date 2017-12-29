#!/usr/bin/env python
import sys
import os

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
    infected_nodes = set()

    input,bursts = getArgs()

    grid_max = ( len(input[0]) - 1 ) / 2
    r = grid_max
    c = -grid_max

    for line in input:
        for char in line:
            if char == '#':
                infected_nodes.add( (r,c) )
            c = c + 1
        r = r - 1
        c = -grid_max

    # direction 0 = forward = moves[0]
    # ++direction === turn right
    moves = [ (1,0), (0,1), (-1,0), (0,-1) ]
    direction = 0
    position = [0,0]
    infections = 0

    for i in range( bursts ):
        if tuple(position) in infected_nodes:
            infected_nodes.remove( tuple(position) )
            direction = ( direction + 1 ) % 4
        else:
            infected_nodes.add( tuple(position) )
            infections = infections + 1
            direction = ( direction - 1 ) % 4

        position = [sum(x) for x in zip(position,moves[direction]) ]
#        print "After %d bursts:" % (i + 1)
#        print infected_nodes
#        print position
#        print

    print "I have caused %d node infections" % infections

if __name__=='__main__':
    main()
