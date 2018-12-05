#! /usr/bin/env python3
import os
import sys
import string

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()[0]


def main():
    original = readfile()

    counts = {}
    for l in string.ascii_lowercase:
        line = original.replace(l,'').replace(l.upper(),'')
        print( f"Processing {l}")

        deletion = True
        while deletion:
            #print( line )
            for n,i in enumerate(line[:-1]):
                if i.islower() and line[n+1] == i.upper() or \
                    i.isupper() and line[n+1] == i.lower():
                    deletion = True
                    line = line[:n] + line[n+2:]
                    break
                else:
                    deletion = False
        counts[l] = len(line)

    print(counts)


if __name__ == "__main__":
    main()
