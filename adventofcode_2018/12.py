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

        genes = defaultdict( lambda: '.' )
        for line in contents[2:]:
            gene, out = line.split(' => ')
            genes[ gene ] = out

        return state, genes

def main():
    initial_state, genes = readfile()

    ending = ['.'] * 4
    state = ending + list(initial_state) + ending
    offset = 4
    swap = []
    current = ''.join(state)

    print( " 0: %s" % current )

    for gen in range(1,2000):
        swap = []
        prepend = extend = 2
        length = len(state)
        previous = current

        # there are _always_ four empty pots on both ends
        # only the 3rd in from either end could possibly grow something
        for c in range( 2,length-2 ):
            plant = genes[ ''.join( state[c-2:c+3] ) ]
            if c >= length - 4 and plant == '#':
                # if 3 or 2 of the end pots grows a plant, add more to the end so there are 4 total empties again
                extend = max(extend, 7+c-length)
            swap.append( plant )

        # if 2 or 3 grew a plant, add more to the beginning so there are 4 total empties again
        # if 4+ died, subtract empties so there are 4 total empties again!
        prepend -= ( swap.index('#') - 2 )
        # if we shifted the line, correct the 0 offset
        # prepend == 2 is the "normal" case (2 always + 2 buffer that didn't grow this round, and a plant in 4)
        offset += prepend - 2
        swap = ending[:prepend] + swap + ending[:extend]
        state = swap
        current = ''.join(state)

        print( "%2d: %s" % (gen, current ) )

        if gen == 20 or previous == current:
            score = sum( [ i - offset for i,c in enumerate(state) if c == '#' ] )
            print( score )

        if previous == current:
            break

if __name__ == "__main__":
    main()
