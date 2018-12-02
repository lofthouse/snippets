#! /usr/bin/env python3
import os
import sys
from collections import Counter
from itertools import combinations

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

    for box_a,box_b in combinations(boxes,2):
        common_letters = [ al for al,bl in zip(box_a,box_b) if al == bl ]
        if len(common_letters) == len(box_b) - 1:
            print( f"The common box ID letters are {''.join(common_letters)}" )
            break

if __name__ == "__main__":
    main()
