#! /usr/bin/env python3
import os
import sys
import numpy as np

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    lines = readfile()
    map = np.zeros((1000,1000),dtype=int)
    claims = []

    for line in lines:
        claim,_,loc,size = line.split()
        ID = int( claim[1:] )
        x0,y0 = ( int(a) for a in loc[:-1].split(',') )
        w,h = ( int(a) for a in size.split('x') )

        claims.append( (ID,x0,y0,w,h) )

        for i in range(x0,x0+w):
            for j in range(y0,y0+h):
                if map[i,j] == 0:
                    map[i,j] = ID
                else:
                    map[i,j] = -1

    count = ( map < 0 ).sum()
    print( f"There are {count} disputed claims" )

    for claim in claims:
        ID,x0,y0,w,h = claim
        if np.all( map[x0:x0+w,y0:y0+h] == ID ):
            print( f"Claim ID {ID} is intact!")        

if __name__ == "__main__":
    main()
