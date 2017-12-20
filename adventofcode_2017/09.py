#!/usr/bin/env python
import sys
import os.path

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <input file> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    part = int(sys.argv[2])

    if not (part == 1 or part == 2):
        print "%s is not a valid part" % sys.argv[2]
        sys.exit(1)

    return (input,part)

# Begin actual code

def main():
    input,part = getArgs()

    for line in input:
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
                if char == '{':
                    groups = groups + 1
                    depth = depth + 1
                    score = score + depth
                elif char == '}':
                    depth = depth - 1
                elif char == '<':
                    garbage = True

        print "Found %d groups with a score of %d" % (groups,score)

if __name__=='__main__':
    main()
