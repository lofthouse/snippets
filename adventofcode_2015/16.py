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

	for line in content:
		tmp = [ i.rstrip(':') for i in line.split() ]
		lab_results[ tmp[0] ] = int( tmp[1] )

	with open( sys.argv[2] ) as input_file:
		content = input_file.read().splitlines()

	for line in content:
		tmp = [ i.rstrip(':,') for i in line.split() ]
		memory.clear()
		failure = False

		for i in range(2,7,2):
			memory[ tmp[i] ] = int( tmp[i+1] )

#		print lab_results
#		print memory
#		raw_input()

		for key in lab_results:
#			print "Testing key",key
			if key in memory and lab_results[key] != memory[key]:
				failure = True

		if not failure:
			print "No Conflicts Found:",line


if __name__=="__main__":
	main()

sys.exit(0)
