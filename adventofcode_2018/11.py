#! /usr/bin/env python3
import os
import sys
import numpy as np

def readserial():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print( f"Usage:  {sys.argv[0]} <input>" )
        sys.exit(1)

    return int( sys.argv[1] )


def main():
    input = readserial()

    # Because the formula for power assumes 1-indexed grid,
    # cheat and just pad with an unused 0-column and 0-row
    grid = np.zeros((301,301))

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

    total_powers = {}
    for size in range(1,301):
        print( f"Processing target size {size}" )
        for j in range( 1, 302-size ):
            for i in range( 1,302-size ):
                # Store the sum of the grid range:  thanks Numpy!
                total_powers[ (i,j,size) ] = grid[i:i+size,j:j+size].sum()

    print( max(total_powers, key=total_powers.get) )

if __name__ == "__main__":
    main()
