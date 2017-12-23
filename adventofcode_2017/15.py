#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <input file>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    part = int( sys.argv[2] )
    if part != 1 and part != 2:
        print "%s is not a valid part" % part
        sys.exit(1)

    return ( int(input[0].split()[4]), int(input[1].split()[4]), part )

# Begin actual code

def main():
    A,B,part = getArgs()
    Af = 16807
    Bf = 48271

    divisor = 2147483647
    matches = 0

    if part == 1:
        for i in range(40000000):
            A = A*Af % divisor
            B = B*Bf % divisor

            if (A & 65535) == (B & 65535):
                matches = matches + 1

        print "%d matches found" % matches

    else:
        for i in range(5000000):
            A = A*Af % divisor
            while A % 4 != 0:
                A = A*Af % divisor

            B = B*Bf % divisor
            while B % 8 != 0:
                B = B*Bf % divisor

            if (A & 65535) == (B & 65535):
                matches = matches + 1

        print "%d matches found" % matches

if __name__=='__main__':
    main()
