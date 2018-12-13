#! /usr/bin/env python3
import os
import sys
from collections import defaultdict

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        contents = in_file.read().splitlines()
        state = contents[0].split(': ')[1]

        genes = defaultdict(lambda: '.')
        for line in contents[2:]:
            gene,out = line.split(' => ')
            genes[gene] = out

        return state,genes

def main():
    initial_state,genes = readfile()

    ending = ['.','.','.','.']
    state = ending + list(initial_state) + ending
    offset = 4
    swap = []

    print( " 0: %s" % ''.join(state) )
    for gen in range(20):
        swap = []
        prepend = extend = 2

        for c in range( 2,len(state)-2 ):
            plant = genes[ ''.join( state[c-2:c+3] ) ]
            if c <= 3 and plant=='#':
                prepend = max(prepend, 6-c)
            if c >= len(state) - 4 and plant == '#':
                extend = max(extend, 7+c-len(state))
            swap.append( plant )

        offset += prepend - 2
        swap = ending[:prepend] + swap + ending[:extend]
        state = swap
        print( "%2d: %s" % (gen+1, ''.join(state) ) )

    score = 0
    for i,c in enumerate(state):
        if c == '#':
            score += i-offset

    print( score )


if __name__ == "__main__":
    main()
