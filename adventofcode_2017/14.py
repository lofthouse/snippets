#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 2 :
        print "Missing argument"
        print "%s <input>" % sys.argv[0]
        sys.exit(1)

    return sys.argv[1]

# Begin actual code


def knotHash( input ):
    lengths = map(ord,input) + [17, 31, 73, 47, 23]
    ring = range(256)
    position = 0
    skip = 0

    for i in range(64):
        ring,position,skip = hashRound(ring,position,skip,lengths)

    dense_ring = densify(ring)

    return "".join(map(lambda x: format(x,'08b'),dense_ring))

def densify(ring):
    result = []
    for group in range(16):
        result.append( reduce(lambda x, y: x^y, ring[group*16:group*16+16]) )

    return result

def hashRound(ring,position,skip,lengths):
    n = len(ring)

    debug( "Processing from %d with skip %d" % (position,skip) )

    for length in lengths:
        start = position
        stop = position + length
        tmp = list(ring)

        for i in range(length):
            tmp[(stop - i - 1) % n] = ring[(start + i) % n]

        ring = list(tmp)
        position = (position + length + skip) % n
        skip = skip + 1

    return (ring,position,skip)

def expandRegion( disk, row, column ):
    # I originally did row and column ranges and then excluded diagonals, but it was messy
    # This is ugly but cleaner?
    neighbors = [ (row-1,column),(row+1,column),(row,column-1),(row,column+1) ]

    for R,C in neighbors:
        if R >= 0 and R < 128 and C >= 0 and C < 128:
            if disk[R][C] == '1':
                disk[R][C] = ' '
                expandRegion( disk, R, C )
            else:
                disk[R][C] = ' '

def main():
    input = getArgs()
    count = 0
    disk = []

    for i in range(128):
        hash = knotHash( input + '-' + str(i) )
        debug( hash )
        count = count + hash.count('1')
        # disk rows will need to be lists later for marking regions
        disk.append( list(hash) )

    print "There are %d used squares" % (count)

    # WARNING: disk is now in row,column order
    region_count = 0


    # strategy:  walk entire disk.  When we find a 1, mark it resolved ( ' ' )
    # then recursively mark all adjacent squares as resolved and increase
    # region count by 1
    for r in range(128):
        for c in range(128):
            # Empty or already resolved cells:  do nothing
            if disk[r][c] == '0' or disk[r][c] == ' ':
                disk[r][c] = ' '
            # Used cells must be in a new region
            else:
                region_count = region_count + 1
                disk[r][c] = ' '
                expandRegion( disk, r, c )

    print "There were %d regions found" % region_count


if __name__=='__main__':
    main()
