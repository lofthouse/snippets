#!/usr/bin/env python

import sys
import hashlib

if  len(sys.argv) != 4 :
	print "Invalid arguments"
	sys.exit(1)

input = sys.argv[1]
zeroes = int(sys.argv[2])
pwlength = int(sys.argv[3])

salt = index = 0
password = list('_'*pwlength)
hash = '1'*pwlength
valid_index = False

for n in range(pwlength):
	# slightly easier to read condition and simpler password storage
	while hash[:zeroes] != '0'*zeroes or not valid_index or password[index] != '_' :
		salt += 1
		hash = hashlib.md5( input + str(salt) ).hexdigest()
		# has the unfortunate side affect of requiring more careful index handling
		valid_index = str.isdigit(hash[zeroes]) and int(hash[zeroes]) < pwlength
		if valid_index :
			index=int(hash[zeroes])

	password[index]=hash[zeroes+1]

	print "Found salt",salt
	print "Password is now",''.join(password)

print "The password is",''.join(password)

sys.exit(0)
