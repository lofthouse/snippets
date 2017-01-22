#!/usr/bin/env python

import sys
import os.path
from collections import defaultdict

def whoWins( reindeer, finish_line ):
	positions=set()

	for deer_data in reindeer:
		name, speed, runtime, resttime = deer_data
		full_cycles = finish_line / (runtime + resttime)
		partial = finish_line % (runtime + resttime)
		position = full_cycles * speed * runtime + min(runtime,partial) * speed
		positions.add( ( position, name ) )

	win = max(positions)[0]
	return( [ (k,v) for k,v in positions if k == win ] )

def main():
	if  len( sys.argv ) != 3 or not os.path.isfile( sys.argv[1] ) or not sys.argv[2].isdigit() :
		print "Invalid arguments"
		print "Usage: 14.py <input file> <finish line in kms>"
		sys.exit(1)

	finish_line = int(sys.argv[2])

	with open( sys.argv[1] ) as input_file:
		content = input_file.read().splitlines()

	reindeer=set()
	points=defaultdict(int)

	for line in content:
		fields=line.split()
		reindeer.add( ( fields[0], int( fields[3] ), int( fields[6] ), int( fields[13] ) ) )

	distance, winner = whoWins( reindeer, finish_line )[0]

	print "The leader at %d seconds is %s (%d kms)" % ( finish_line, winner, distance )

	for time in range(1, finish_line+1):
		for t,leader in whoWins( reindeer, time ):
			points[ leader ] += 1

	print "The winner is %s with %d points" % ( max(points, key=points.get), max(points.values()) )

if __name__=="__main__":
	main()

sys.exit(0)
