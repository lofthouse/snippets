#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print( f"Usage:  {sys.argv[0]} <recipe count>" )
        sys.exit(1)

    count = int( sys.argv[1] )

    e1 = 0
    e2 = 1

    recipes = [3,7]
    l = 2
    lim = count + 10

    while l < lim:
#        print( e1, e2 )
        for x in list(str( recipes[e1] + recipes[e2] )):
            recipes.append( int(x) )
#        print(recipes)

        l = len(recipes)
        e1 = (e1 + 1 + recipes[e1]) % l
        e2 = (e2 + 1 + recipes[e2]) % l

    print( ''.join( [ str(i) for i in recipes[count:count+10] ] ) )

if __name__ == "__main__":
    main()
