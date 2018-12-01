#! /usr/bin/env python3
import os
import sys


def read_input():
    if len( sys.argv ) != 2:
        print( "Missing input file argument!" )
        sys.exit(1)

    if os.path.isfile( sys.argv[1] ):
        with open( sys.argv[1] ) as input_file:
            lines = input_file.read().splitlines()
            line = lines[0]
    else:
        print( f"{sys.argv[1]} is not a file!" )
        sys.exit(1)

    return line


def main():
    line = read_input()

    floor = 0
    delivered_basement_message = False

    for step, char in enumerate( line,1 ):
        if char == "(":
            floor = floor + 1
        if char == ")":
            floor = floor - 1
        if not delivered_basement_message and floor == -1:
            print( f"Santa entered the basement on step {step}" )
            delivered_basement_message = True

    print( f"Santa ended up at floor {floor}" )

if __name__ == "__main__":
    main()
