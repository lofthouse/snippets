#!/usr/bin/env python

import sys
import hashlib

if  len(sys.argv) != 4 :
	print "Invalid arguments"
	sys.exit(1)

input = sys.argv[1]
zeroes = int(sys.argv[2])
pwlength = int(sys.argv[3])
password=''
salt = 0
end = "00000000000000000000000000000000"[:zeroes]

for n in range(pwlength):
	salt += 1
	while hashlib.md5( input + str(salt) ).hexdigest()[:zeroes] != end :
		salt += 1

	password += hashlib.md5( input + str(salt) ).hexdigest()[5]
	print "Found salt",salt
	print "Password is now",password

print "The password is",password

sys.exit(0)
