#! /usr/bin/env python3
import os
import sys
import re

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    lines = readfile()

    positions = []
    velocities = []

    for line in lines:
        foo = re.findall('.*<(.+)>.*<(.+)>', line)
        positions.append( tuple( [int(x) for x in foo[0][0].split(',')] ) )
        velocities.append( tuple( [int(x) for x in foo[0][1].split(',')] ) )

    for t in range(10888):
        positions = [ tuple( [ p[0]+v[0], p[1]+v[1] ]) for p,v in zip(positions,velocities) ]
    dp = [ tuple( [ int(x) , int(y) ]) for x,y in positions ]

    for j in range(180,210):
        for i in range(160,320):
            if (i,j) in dp:
                print( "#", end='' )
            else:
                print( " ", end='' )
        print()
        
    print(t+1)

if __name__ == "__main__":
    main()
