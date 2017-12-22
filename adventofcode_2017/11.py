#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 2 :
        print "Invalid argument"
        print "%s <input file> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    return input

# Begin actual code

def distance(p):
    if (p[0] * p[1]) >= 0:
        return sum(map(abs,p))
    else:
        return abs( p[0] ) + abs( abs(p[1]) - abs(p[0]) )

def main():
    input = getArgs()

    position = (0,0)
    fd = 0

    vectors={
        'n':(0,1),
        'ne':(1,0),
        'se':(1,-1),
        's':(0,-1),
        'sw':(-1,0),
        'nw':(-1,1)
    }

    for step in input[0].split(','):
        position = map(sum, zip(position, vectors[step]))
        p = distance(position)
        fd = max( fd, p )

    print "Distance is %d, and the furthest we ever got was %d" % (p,fd)

if __name__=='__main__':
    main()
