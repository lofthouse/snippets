#! /usr/bin/env python3
import os
import sys

def test(c,Part2):
    e = [ int(i) for i in str(c) ]
    max = len(e)

    passed = False
    # 112222 is good, but fail happens after pass, pass needs to override
    # we we'll keep track of good and bad digits
    bad_digit = ''
    good_digit = ''

    for j in range( max - 1 ):
        if e[j] == e[j+1]:
            if not Part2:
                passed = True
            else:
                if j < max-2 and e[j+1] == e[j+2]:
                    passed = False
                    bad_digit = e[j]
                    if good_digit == bad_digit:
                        good_digit = ''
                elif e[j] != bad_digit:
                    passed = True
                    good_digit = e[j]
        if e[j] > e[j+1]:
            return False

    if good_digit != '':
        return True

    return passed

def main():
    valid1 = 0
    valid2 = 0

    for i in range( 273025, 767253+1 ):
        if test(i,False):
            valid1 += 1
        if test(i,True):
            valid2 += 1

    print( "There are", valid1, "part 1 passwords" )
    print( "There are", valid2, "part 2 passwords" )


if __name__ == "__main__":
    main()
