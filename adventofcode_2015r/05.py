#! /usr/bin/env python3

import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print( f"Usage: {sys.argv[0]} <input file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as input_file:
        return input_file.read().splitlines()

def main():
    vowels = set( "aeiou" )
    dirty = set( ["ab", "cd", "pq", "xy" ] )
    o_nice = n_nice = 0

    for string in readfile():
        doubles = [ l for i,l in enumerate(string[:-1]) if string[ i+1 ] == l ]
        pairs = [ l+string[i+1] for i,l in enumerate(string[:-1]) ]
        vowely = [ l for l in string if l in vowels ]

        if len( dirty.intersection( set(pairs) ) ) == 0 and\
            len( vowely) >= 3 and\
            len( doubles ) != 0:
            o_nice += 1

    for string in readfile():
        double_pairs = [ string[i:i+2] for i,l in enumerate(string[:-1]) if string[i+2:].find( string[i:i+2] ) != -1 ]
        sep_pairs = [ l+string[i+2] for i,l in enumerate(string[:-2]) if l == string[i+2] ]

        if len( double_pairs ) > 0 and len( sep_pairs ) > 0:
            n_nice += 1

    print( f"There are {o_nice} nice strings (old skool)" )
    print( f"There are {n_nice} nice strings (new skool)" )


if __name__ == "__main__":
    main()
