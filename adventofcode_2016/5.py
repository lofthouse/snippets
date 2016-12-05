#!/usr/bin/env python

import sys
import hashlib

if  len(sys.argv) != 4 :
	print "Invalid arguments"
	sys.exit(1)

input = sys.argv[1]
zeroes = int(sys.argv[2])
pwlength = int(sys.argv[3])
password={}
salt = 0
end = '0'*zeroes
hash = '1'*pwlength

for n in range(pwlength):
	while hash[:zeroes] != end or not str.isdigit(hash[zeroes]) or int(hash[zeroes]) >= pwlength or hash[zeroes] in password :
		salt += 1
		hash = hashlib.md5( input + str(salt) ).hexdigest()

	password[hash[zeroes]]=hash[zeroes+1]

	print "Found salt",salt
	print "Password is now",''.join([value for (key,value) in sorted(password.items())])

print "The password is",''.join([value for (key,value) in sorted(password.items())])

sys.exit(0)
