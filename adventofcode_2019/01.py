#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def fuel( load ):
    fuel_required = load // 3 - 2
    if fuel_required <= 0:
        return 0
    return fuel_required + fuel( fuel_required )


def main():
    lines = readfile()

    total_fuel = 0
    for line in lines:
        total_fuel += ( int(line) // 3 - 2 )

    print( total_fuel )

    total_fuel = 0
    for line in lines:
        total_fuel += fuel( int(line) )

    print( total_fuel )


if __name__ == "__main__":
    main()
