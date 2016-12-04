#!/usr/bin/env python

import sys
import hashlib

if  len(sys.argv) != 3 :
	print "Invalid arguments"
	sys.exit(1)

input = sys.argv[1]
zeroes = int(sys.argv[2])
salt = 1
end = "00000000000000000000000000000000"[:zeroes]

while hashlib.md5( input + str(salt) ).hexdigest()[:zeroes] != end :
	salt += 1

print "Santa's coin number is",salt

sys.exit(0)
