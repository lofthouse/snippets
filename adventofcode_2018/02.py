#! /usr/bin/env python3
import os
import sys
from collections import Counter

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def main():
    boxes = readfile()

    box_contents = []
    cs = 1
    for box in boxes:
        box_contents.append( Counter(box) )
    for count in [2,3]:
        cs *= sum( [1 for box in box_contents if count in box.values() ] )
    print( f"The checksum is {cs}" )

    for i,box_a in enumerate(boxes):
        for box_b in boxes[i+1:]:
            common_letters = [ al for al,bl in zip(box_a,box_b) if al == bl ]
            if len(common_letters) == len(box_b) - 1:
                print( f"The common box ID letters are {''.join(common_letters)}" )
                sys.exit(0)

if __name__ == "__main__":
    main()
