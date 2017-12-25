#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <steps> <part>" % sys.argv[0]
        sys.exit(1)

    return ( int(sys.argv[1]), int(sys.argv[2]) )

# Begin actual code

def insert(i,position,buffer):
    if position == 0:
        return buffer[0:1] + [i] + buffer[1:]
    if position == (i-1):
        return buffer + [i]
    return buffer[0:position+1] + [i] + buffer[position+1:]

def main():
    step,part = getArgs()

    buffer = [ 0 ]
    position = 0

    if part == 1:
        stop = 2017 + 1

        for i in xrange(1,stop):
            position = ( position + step ) % i
            buffer = insert(i,position,buffer)
            debug( i, "(", position, "): ", buffer )
            position = position + 1

        debug( buffer )
        print "After inserting %d, the next value is %d" % (i, buffer[(position + 1) % i])
    else:
        stop = 50000000 + 1
        zero = 0

        for i in xrange(1,stop):
            if i % 1000 == 0:
                print "\r%d" % i,

            position = ( position + step ) % i
            if position == zero:
                print "%d has slipped in after 0" % i

            position = position + 1

if __name__=='__main__':
    main()
