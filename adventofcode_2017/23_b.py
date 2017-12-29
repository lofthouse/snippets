#!/usr/bin/env python
import sys
import os

# Begin actual code
def isprime(n):
    """Returns True if n is prime."""
    # Credit:  https://stackoverflow.com/a/1801446/3300042
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

# What the pseudo-code is actually doing:
# count all non-primes from 108400 to 125400 in steps of 17
def main():
    b = 108400
    c = 125400
    inc = 17
    primes = 0
    nonprimes = 0

    for can in range(b,c+1,inc):
        if isprime(can):
            primes += 1
        else:
            nonprimes += 1

    print "Non-Primes:",nonprimes


if __name__=='__main__':
    main()
