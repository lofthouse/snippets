#!/usr/bin/env python

import sys
from itertools import dropwhile, islice, product
from string import ascii_lowercase as letters

# FUGLY.  dropwhile is supposed to work but I could not figure out why it didn't for the life of me
# islice is supposed to work but I could not figure out why not for the life of me
def passwords():
	for t in product(letters[7:],letters[4:], letters[15:], letters, letters, letters, letters, letters):
		yield "".join(t)

def hasRun(line):
	for n in range(len(line)-2):
		if ord(line[n])+1 == ord(line[n+1]) and ord(line[n])+2 == ord(line[n+2]) :
			return True
	return False

def hasIOL(line):
	if 'i' in line or 'o' in line or 'l' in line:
		return True
	return False

def hasTwoDoubles(line):
	doubles=set()
	skipnext=False
	for n in range(len(line)-1):
		if skipnext:
			skipnext=False
			continue
		if line[n] == line[n+1]:
			doubles.add(line[n:n+2])
			skipnext=True
	return len(doubles) > 1

if  len(sys.argv) != 2 :
	print "Invalid arguments"
	sys.exit(1)

old_password = sys.argv[1]
#op_index=0
#for i in range(8):
#	op_index += (2**(8-i))*(ord(old_password[i])-ord('a'))

#print op_index
#op_index=10
#print list(islice(passwords, op_index, op_index+10))

messaged=False
for candidate in passwords():
	if candidate < old_password:
		continue
	if not messaged:
		messaged=True
		print "Ready...searching"
	if hasRun(candidate) and not hasIOL(candidate) and hasTwoDoubles(candidate):
		print candidate
		break

sys.exit(0)
