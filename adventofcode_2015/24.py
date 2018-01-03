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

def findBalance( pool, target, n ):
    if n == 1:
        return True

    for j in range( 2, len(pool) - 2 ):
        for group in combinations( pool, j ):
            if sum(group) == target and findBalance( pool - set(group), target, n - 1):
                # can balance!
                debug( pool,"splits",n,"ways into",group,"and",tuple( pool - set(group) ) )
                return True
    debug( pool,"does not split %d ways" % n )
    return False

def main():
    global packages

    input,part = getArgs()

    packages = set( map( int, input ) )
    if part == 1:
        target = sum( packages ) / 3
    else:
        target = sum( packages ) / 4

    candidates = set()
    valid_groups = set()
    min_length = len( packages )

    # start by making a list of the valid package combos, starting with 2
    # The winner will be the shortest length, so only progress if there's no winner
    for i in range( 2, len(packages) - 2 ):
        print "Trying groups of length %d" % i
        for group in combinations( packages, i ):
            if sum(group) == target:
                valid_groups.add( group )

        # now find which can be balanced
        for candidate in valid_groups:
            # balance into part + 1 sub-groups
            if findBalance( packages - set(candidate), target, part + 1 ):
                candidates.add( candidate )
                min_length = min( min_length, len(candidate) )

        if len(candidates) != 0:
            # we have a winner!!!!
            break

    final_candidates = [ i for i in candidates if len(i) == min_length ]

    QEs = [ reduce(mul,i) for i in final_candidates ]

    print min(QEs),"is the winner"

if __name__=='__main__':
    main()
