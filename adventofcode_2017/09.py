#!/usr/bin/env python
import sys
import os.path

def getArgs():
    if len(sys.argv) != 2 :
        print "Invalid argument"
        print "%s <input file> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    return input

# Begin actual code

def main():
    input = getArgs()

    for line in input:
        characters = 0
        score = 0
        groups = 0
        depth = 0
        garbage = False
        ignore = False

        for char in line:
            if garbage:
                if ignore:
                    ignore = False
                elif char == '!':
                    ignore = True
                elif char == '>':
                    garbage = False
                else:
                    characters = characters + 1

            else:
                if char == '{':
                    groups = groups + 1
                    depth = depth + 1
                    score = score + depth
                elif char == '}':
                    depth = depth - 1
                elif char == '<':
                    garbage = True

        print "Found %d groups with a score of %d and %d characters" % (groups,score,characters)

if __name__=='__main__':
    main()
