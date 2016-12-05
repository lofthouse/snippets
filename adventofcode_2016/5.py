#!/usr/bin/env python

import sys
import hashlib

if  len(sys.argv) != 4 :
	print "Invalid arguments"
	sys.exit(1)

input = sys.argv[1]
zeroes = int(sys.argv[2])
pwlength = int(sys.argv[3])

salt = 0
index = '0'
end = '0' * zeroes # this saves ~2 s over total run vs. doing in-line below
password = list('_'*pwlength)
hash = '1'*pwlength

for n in range(pwlength):
	# all the reasons why a candidate is no good:  order is important!  isdigit protects int protects password[]
	while hash[:zeroes] != end or not str.isdigit(index) or int(index) >= pwlength or password[int(index)] != '_' :
		salt += 1
		hash = hashlib.md5( input + str(salt) ).hexdigest()
		index = hash[zeroes]

	password[int(index)]=hash[zeroes+1]

	print "Found salt",salt
	print "Password is now",''.join(password)

print "The password is",''.join(password)

sys.exit(0)
