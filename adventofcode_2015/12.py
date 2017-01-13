#!/usr/bin/env python

import sys
import os.path
import json

def accounting( line, part ):
	part_two = True if part==2 else False

	if not line:
		return 0
	elif isinstance( line, dict ):
		if part_two and u'red' in line.values():
			return 0
		else:
			return sum( [ accounting( n, part ) for n in line.values() ] )
	elif isinstance( line, list ) or isinstance( line, tuple ):
		return sum( [ accounting( n, part ) for n in line ] )
	elif isinstance( line, int ):
		return line
	else:
		return 0

def main():
	if  len( sys.argv ) != 2 or not os.path.isfile( sys.argv[1] ) :
		print "Invalid argument"
		sys.exit(1)

	with open( sys.argv[1] ) as input_file:
		content = input_file.read().splitlines()

	for line in content:
		decode=json.loads( line )

		print "Part 1:", accounting( decode, 1 )
		print "Part 2:", accounting( decode, 2 )

if __name__=="__main__":
	main()

sys.exit(0)
