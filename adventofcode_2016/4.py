#!/usr/bin/env python

import sys
import os.path
import collections
import string

# hat tip http://stackoverflow.com/users/496713/amillerrhodes
def caesar(plaintext, shift):
	alphabet = string.ascii_lowercase
	shift=shift%26
	shifted_alphabet = alphabet[shift:] + alphabet[:shift]
	table = string.maketrans(alphabet, shifted_alphabet)
	return plaintext.translate(table)

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

sum=0

for line in content:
	temp1=line.split('-')							# all the bits
	room=''.join(temp1[:-1])						# reassemble the room name
	temp2=temp1[-1].split('[')						# separate the sector and checksum
	sector=int(temp2[0])
	checksum=temp2[-1].split(']')[0]				# strip the trailing ] from the checksum
	decrypt=caesar(room,sector)

	if decrypt.startswith('north') :
		print "Room",room,"(",decrypt,") is in sector",sector

	letters=collections.Counter(room)				# count all the letters in the room
	letters=letters.items()							# convert to list of tuples
	letters.sort(key=lambda x: x[0])				# sort alphabetically
	letters.sort(key=lambda x: x[1], reverse=True)	# then by reverse frequency
	test=''.join([ l for l,n in letters[:5] ])		# then pull the first 5 (the tuples are letter,count)

	if test == checksum :
		sum += sector

print "The sum of the checksums is",sum

sys.exit(0)
