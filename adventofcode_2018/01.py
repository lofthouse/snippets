#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    lines = readfile()

    f = 0
    fs = set( [0,] )
    repeat = first = False

    while not repeat:
        for line in lines:
            f += int( line )

            if f not in fs:
                fs.add( f )
            else:
                repeat = True
                break

        if not first:
            print( f"The first loop frequency is {f}" )
            first = True

    print( f"The first repeated frequency is {f}" )

if __name__ == "__main__":
    main()
