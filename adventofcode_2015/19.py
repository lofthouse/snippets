#!/usr/bin/env python

import sys
import os.path
from pprint import pprint

def usageAndExit():
	print "19.py <part> <input_file>"
	sys.exit(1)

def readData():
	if not ( len(sys.argv) == 3 and sys.argv[1].isdigit() and os.path.isfile(sys.argv[2]) ):
		usageAndExit()

	part = int(sys.argv[1])
	if part not in (1,2):
		usageAndExit()

	with open(sys.argv[2]) as input_file:
		content = input_file.read().splitlines()

	reps=[]

	for line in content[:-2]:
		reps.append( line.split(" => ") )

	return reps, content[-1], part

def react(seed,reps,reverse=False):
	#	Theory of operation
	#	>>> a="H".join("HOHOHO".split("H")[0:1])
	#	>>> b="H".join("HOHOHO".split("H")[1:])
	#	>>> "X".join(list((a,b)))
	#	'XOHOHO'
	#	>>> a="H".join("HOHOHO".split("H")[0:2])
	#	>>> b="H".join("HOHOHO".split("H")[2:])
	#	>>> "X".join(list((a,b)))
	#	'HOXOHO'
	#	>>> b="H".join("HOHOHO".split("H")[3:])
	#	>>> a="H".join("HOHOHO".split("H")[0:3])
	#	>>> "X".join(list((a,b)))
	#	'HOHOXO'
	products=set()

	for x,y in reps:
		if reverse:
			x,y = y,x
		skeleton = seed.split(x)
		for i in range(1,len(skeleton)):
			products.add( x.join(skeleton[:i])+y+x.join(skeleton[i:]) )

	return products

def distill(molecule, reps):
	# Theory of operation:  Make most aggressive terminal reverse substitions first until none work
	# Then make most aggressive non-terminal reverse subsitutions until none work
	# repeat until you reach "e"
	count = 0
	fl=len(molecule)

	while molecule != "e":
		sl=fl+1
		while fl<sl:
			sl=fl
			for x,y in reps:
				skeleton = molecule.split(y)
				if len(skeleton) > 1:
					molecule = y.join(skeleton[:1])+x+y.join(skeleton[1:])
					count += 1
					fl = len(molecule)
					break

	return count

def main():
	reps, molecule, part = readData()

	if part == 1:
		print "%d molecules can be created" % len(react(molecule,reps))

	if part == 2:
		print "It took %d steps to make our molecule from 'e'" % distill(molecule,reps)

if __name__ == '__main__':
	main()

sys.exit(0)
