#! /usr/bin/env python3
import os
import sys
import operator
import string

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()[0]

def react(line):
    deletion = True
    while deletion:
        deletion = False
        before = len(line)
        for k in string.ascii_lowercase:
            line = line.replace(k+k.upper(),'').replace(k.upper()+k,'')
        if len(line) != before:
            deletion = True
    return( len(line) )

def main():
    original = readfile()

    print( react(original) )

    counts = []
    for l in string.ascii_lowercase:
        line = original.replace(l,'').replace(l.upper(),'')
        print( f"Processing {l}")

        counts.append( react(line) )

    print( min(counts) )

if __name__ == "__main__":
    main()
