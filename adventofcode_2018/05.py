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
    new = []
    for c in line:
        if not new:
            new.append(c)
        else:
            if c.isupper() and new[-1] == c.lower() or\
                c.islower() and new[-1] == c.upper():
                new.pop()
            else:
                new.append(c)
    return( len(new) )

def main():
    original = readfile()
    print( react(original) )

    counts = []
    for l in string.ascii_lowercase:
        line = original.replace(l,'').replace(l.upper(),'')
        counts.append( react(line) )

    print( min(counts) )

if __name__ == "__main__":
    main()
