#!/usr/bin/env python
import sys
import os
from itertools import combinations
from operator import mul

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

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

    packages = set( map( int, input ) )
    target = sum( packages ) / 3
    candidates = set()
    min_length = len( packages )

    for i in range( len(packages) - 2 ):
        for candidate in combinations( packages, i ):
            if sum(candidate) == target:
                balance = packages - set(candidate)

                try:
                    for j in range( len( balance ) - 2 ):
                        for b_candidate in combinations( balance, j ):
                            if sum( b_candidate ) == target:
                                raise StopIteration
                    print candidate,"does not work as there is no way to split the balance"
                except StopIteration:
                    print candidate,"works with",b_candidate,"and",tuple( balance-set(b_candidate) )
                    candidates.add( candidate )
                    min_length = min( min_length, len(candidate) )

    final_candidates = [ i for i in candidates if len(i) == min_length ]

    print final_candidates

    QEs = [ reduce(mul,i) for i in final_candidates ]

    print min(QEs),"is the winner"

if __name__=='__main__':
    main()
