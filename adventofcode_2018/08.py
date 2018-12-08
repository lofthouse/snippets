#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()[0]


def mdsum( data ):
    children = data[0]
    md = data[1]

    offset = 2
    mds = 0
    value = 0
    cvs = []
    for i in range( children ):
        v,l,s = mdsum( data[offset:-md])
        mds += s
        offset += l
        cvs.append(v)

    if children == 0:
        value = sum( data[offset:offset+md] )
    else:
        for m in range(md):
            child = data[offset+m]
            if child-1 < len(cvs):
                value += cvs[child-1]

    return ( value, offset + md, mds + sum( data[offset:offset+md]) )

def main():
    data = [ int(i) for i in readfile().split() ]

    value, length, sum = mdsum( data )
    print( f"The sum of the metadata is {sum}")
    print( f"The value of the root note is {value}")

if __name__ == "__main__":
    main()
