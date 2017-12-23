#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 2 :
        print "Invalid argument"
        print "%s <input file>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    return ( int(input[0].split()[4]), int(input[1].split()[4]) )

# Begin actual code

def main():
    A,B = getArgs()
    Af = 16807
    Bf = 48271

    divisor = 2147483647
    matches = 0

    for i in range(40000000):
        A = A*Af % divisor
        B = B*Bf % divisor

        if (A & 65535) == (B & 65535):
            matches = matches + 1

    print "%d matches found" % matches

if __name__=='__main__':
    main()
