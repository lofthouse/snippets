#! /usr/bin/env python3
import os
import sys
from collections import defaultdict

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    boxes = readfile()

    box_contents = []
    for box in boxes:
        foo = defaultdict(int)
        for l in box:
            foo[l] += 1
        box_contents.append( foo )
    
    counts = defaultdict( int )
    for box in box_contents:
        for count in [2,3]:
            for bin in box:
                if box[bin] == count:
                    counts[count] += 1
                    break

    print( f"The checksum is {counts[2] * counts[3]}" )

    for i,boxa in enumerate(boxes):
        for boxb in boxes[i+1:]:
            miss = 0
            answer = ""
            for j in range( len( boxa )):
                if boxa[j] != boxb[j]:
                    miss += 1
                else:
                    answer += boxa[j]
            if miss == 1:
                print( f"The common box ID letters are {answer}" )
                sys.exit(0)

if __name__ == "__main__":
    main()
