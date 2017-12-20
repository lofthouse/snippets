#!/usr/bin/env python

import sys
import os.path
from itertools import permutations

if len(sys.argv) != 2 :
    print "Invalid argument"
    print "%s <file containing passphrases>" % sys.argv[0]
    sys.exit(1)

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as input_file:
        input = input_file.read().splitlines()
else:
    print "%s is not a file" % sys.argv[1]
    sys.exit(1)

count1 = 0
count2 = 0

for passphrase in input:
    valid1 = True
    valid2 = True
    words = {}
    for word in passphrase.split():
        if word in words:
            valid1 = False

        for anagram in permutations(word):
            if ''.join(anagram) in words:
                valid2 = False
                break

        words[word] = True

    if valid1:
        count1 = count1 + 1

    if valid2:
        count2 = count2 + 1

print "There are %d valid passphrases for Part 1" % count1
print "There are %d valid passphrases for Part 2" % count2
