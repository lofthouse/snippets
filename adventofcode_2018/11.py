#! /usr/bin/env python3
import os
import sys
import string

def readfile():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print( f"Usage:  {sys.argv[0]} <input>" )
        sys.exit(1)

    return int( sys.argv[1] )


def main():
    input = readfile()

    grid = [ [0 for i in range( 0, 301 )] for j in range( 0, 301 ) ]

    for j in range( 1, 301 ):
        for i in range( 1,301 ):
            rack_ID = i + 10
            power = rack_ID * j
            power += input
            power *= rack_ID
            if power > 100:
                power = int( str(power)[-3] )
            else:
                power = 0
            power -= 5
            grid[i][j] = power

    for size in range(1,301):
        total_powers = {}
        print( f"Processing target size {size}" )
        for j in range( 1, 302-size ):
            for i in range( 1,302-size ):
                tp = 0
                for y in range( j, j+size ):
                    for x in range( i, i+size ):
                        tp += grid[x][y]
                total_powers[ (i,j,size) ] = tp

    print( max(total_powers, key=total_powers.get) )

if __name__ == "__main__":
    main()
