#!/usr/bin/env python

import sys
import os.path

def main():
	if  len( sys.argv ) != 2 or not os.path.isfile( sys.argv[1] ) :
		print "Invalid argument"
		sys.exit(1)

	with open( sys.argv[1] ) as input_file:
		content = input_file.read().splitlines()

	for line in content:

if __name__=="__main__":
	main()

sys.exit(0)
