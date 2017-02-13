#!/usr/bin/env python

import sys
import os.path

def main():
	lab_results={}
	memory={}

	if  len( sys.argv ) != 3 or not os.path.isfile( sys.argv[1] ) or not os.path.isfile( sys.argv[2] ) :
		print "Invalid argument"
		print "Usage:  16.py <lab_results> <memoir>"
		sys.exit(1)

	with open( sys.argv[1] ) as input_file:
		content = input_file.read().splitlines()

	# load lab results
	for line in content:
		tmp = [ i.rstrip(':') for i in line.split() ]
		lab_results[ tmp[0] ] = int( tmp[1] )

	with open( sys.argv[2] ) as input_file:
		content = input_file.read().splitlines()

	# review each memory in turn
	for line in content:
		memory.clear()
		p1_failure = False
		p2_failure = False

		tmp = [ i.rstrip(':,') for i in line.split() ]
		for i in range(2,7,2):
			memory[ tmp[i] ] = int( tmp[i+1] )

		# attempt to find matches between the lab result and the memory
		for key in lab_results:
			if key in memory:
				if memory[key] != lab_results[key]:
					p1_failure = True

				if key == 'cats' or key == 'trees':
					if memory[key] <= lab_results[key]:
						p2_failure = True
				elif key == 'pomeranians' or key == 'goldfish':
					if memory[key] >= lab_results[key]:
						p2_failure = True
				elif memory[key] != lab_results[key]:
					p2_failure = True

		if not p1_failure:
			print "Part 1 No Conflicts Found:",line
		if not p2_failure:
			print "Part 2 No Conflicts Found:",line


if __name__=="__main__":
	main()

sys.exit(0)
