#!/usr/bin/env python

import sys
import os.path
from collections import defaultdict
from itertools import combinations

def main():
	if  len( sys.argv ) != 3 or not os.path.isfile( sys.argv[2] ) :
		print "Usage:  17.py <target volume> <container_list>"
		sys.exit(1)

	target_volume = int( sys.argv[1] )
	containers = []
	valid_combos = 0
	# for Part 2, we'll need to keep counts.  YAY defaultdict!
	combo_stats = defaultdict(int)

	with open( sys.argv[2] ) as input_file:
		content = input_file.read().splitlines()

	# load the list of available containers.  This has to be a list, not a set, because we have duplicates!
	for line in content:
		containers.append( int(line) )

	# try all combinations of all subcounts of available containers
	for i in range( len(containers) ):
		for j in combinations(containers,i):
			if sum(j) == target_volume:
				# for Part 2, keep some stats
				combo_stats[ len(j) ] += 1
				valid_combos += 1

	print "There are %d ways to do it, Frodo" % valid_combos
	tmp = min(combo_stats)
	print "You can do it with as few as %d containers, and there are %d ways to do that" % (tmp,combo_stats[tmp])

if __name__=="__main__":
	main()

sys.exit(0)
