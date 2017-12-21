#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 4 :
        print "Invalid argument"
        print "%s <input file> <length> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    try:
        length = int(sys.argv[2])
    except:
        print "%s is not a valid integer" % sys.argv[2]
        sys.exit(1)

    part = int(sys.argv[3])

    if not (part == 1 or part == 2):
        print "%s is not a valid part" % sys.argv[3]
        sys.exit(1)

    return (map(int,input[0].split(',')), range(length), part)

# Begin actual code

def main():
    lengths,ring,part = getArgs()

    position = 0
    skip = 0
    n = len(ring)

    debug( ring )

    for length in lengths:
        debug( "Processing length %d" % length )

        start = position
        stop = position + length
        tmp = list(ring)

        for i in range(length):
            tmp[(stop - i - 1) % n] = ring[(start + i) % n]

        ring = list(tmp)
        position = (position + length + skip) % n
        skip = skip + 1

        debug( ring )

    print "The answer is %d " % (ring[0] * ring[1])


if __name__=='__main__':
    main()
