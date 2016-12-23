#!/usr/bin/env python

import sys
from hashlib import md5

def hasRun(line,length,all):
	found=[]
	for n in range(len(line)-(length-1)):
		first=line[n]
		for i in range(1,length):
			if line[n+i] != first:
				break
		else:
			if all:
				found.append(first)
			else:
				return first
	if all and found:
		return found
	else:
		return False

if  len(sys.argv) != 2 :
	print "Invalid arguments"
	sys.exit(1)

salt = sys.argv[1]
index = 0
candidates=[]
drops=set()
keys=[]
last_index=None

while True:
	candidate = md5( salt + str(index) ).hexdigest()

	triplet=hasRun( candidate, 3, False)
	if triplet:
		candidates.append( (index, triplet) )
#		print "Adding %d,%s: candidate" % (index,triplet)

	pentlets=hasRun( candidate, 5, True)
	if pentlets:
		for i,d in candidates:
			if index-i > 1001:
				drops.add( (i,d) )
#				print "Dropping %d,%s: stale" % (i,d)
				continue
			if d in pentlets and i != index:
				keys.append( (i, index, d) )
				drops.add( (i,d) )
#				print "Keeping %d,%s: valid key!" % (i,d)
				if len(keys) >= 64:
					if not last_index:
						print "Have 64 keys now...flushing"
						last_index=index
					if candidates[0][0] > last_index:
						keys.sort()
						i=1
						for a,b,c in keys:
							print "%d: triplet at %d, pentlet at %d, %s" % (i,a,b,c)
							i += 1
						print "The 64th index was %d" % keys[63][0]
						sys.exit(0)
		# This set me back over an hour!
		# If you remove inline, it changes the iteration and you end up SKIPPING valid candidates!!!!
		while drops:
			candidates.remove( drops.pop() )
#			del drops[ (i,d) ]
#		drops=set()
	index += 1
