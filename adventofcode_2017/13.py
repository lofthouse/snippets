#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

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
    severity = 0
    scanner = {}

    for line in input:
        dpth,rnge = line.split()
        dpth = int(dpth.strip(':'))
        rnge = int(rnge)

        scanner[dpth] = rnge

    debug( scanner )

    for dpth, rnge in scanner.iteritems():
        if dpth % (2 * (rnge - 1)) == 0:
            severity = severity + (dpth * rnge)

    print "The severity is %d" % severity

    offset = 10

    while True:
        severity = 0
        for dpth, rnge in scanner.iteritems():
            if (dpth+offset) % (2 * (rnge - 1)) == 0:
                break
        else:
            print "You escape with offset %d !" % offset
            sys.exit(0)

        offset = offset + 2

if __name__=='__main__':
    main()
