#! /usr/bin/env python3
import os
import sys

def test(c):
    e = [ int(i) for i in str(c) ]
    max = len(e)

    # Part 1, Part 2
    passed = [ False, False ]
    # 112222 is good, but fail happens after pass, pass needs to override
    # we we'll keep track of good and bad digits
    bad_digit = ''
    good_digit = ''

    for j in range( max - 1 ):
        if e[j] == e[j+1]:
            # Part 1 only needs a single pair:  PASS
            passed[0] = True
            if j < max-2 and e[j+1] == e[j+2]:
                passed[1] = False
                bad_digit = e[j]
                if good_digit == bad_digit:
                    good_digit = ''
            elif e[j] != bad_digit:
                passed[1] = True
                good_digit = e[j]
        if e[j] > e[j+1]:
            return [ False, False ]

    if good_digit != '':
        # If we got here, both parts Passed
        return [ True, True ]

    return passed

def main():
    valid = [ 0, 0 ]

    for i in range( 273025, 767253+1 ):
        # This actually doesn't take any more time:  python does the right thing and doesn't recompute test(i)
        valid = [ v+1 if r else v for v,r in zip( valid, test(i) ) ]

    print( "There are", valid[0], "part 1 passwords" )
    print( "There are", valid[1], "part 2 passwords" )


if __name__ == "__main__":
    main()
