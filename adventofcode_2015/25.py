#!/usr/bin/env python
import sys
import os
import primefac
from math import sqrt

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

def modex(b,e,n):
    c = 1
    ep = 0
    while ep < e:
        ep += 1
        c = b * c % n
    return c

def main():
    input = getArgs()

    a = 20151125
    b = 252533
    n = 33554393

    r = int( input[0].split()[15].strip(',') )
    c = int( input[0].split()[17].strip('.') )

    # entries are in the form a * b^k (mod n), where k is as follows:
    # (the grid entries follow the triangular numbers formula, with some
    #  column shifting and a final "- 1" because the first entry is not
    #  multiplied by b)
    k = ( (r+c-2)*(r+c-1)/2 + c ) - 1
    print "k=",k

    # break k up into prime factors
    kf = [ i for i in primefac.primefac(k) ]

    print "k factors into",kf

    sub = modex(b,kf[0],n)
    for i in range(1,len(kf)):
        sub = modex(sub, kf[i], n)
        print "sub-product through f[%d]" % i,sub

    print "a * b ^ k = ",a * sub % n


if __name__=='__main__':
    main()
