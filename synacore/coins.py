#!/usr/bin/env python
import sys
import os
from itertools import permutations

def main():
    for combo in permutations( [2,3,5,7,9] ):
        if ( combo[0] + combo[1] * combo[2] ** 2 + combo[3] ** 3 - combo[4] ) == 399:
            print combo

if __name__=='__main__':
    main()
