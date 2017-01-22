#!/usr/bin/env python

import sys
import os.path
from itertools import permutations
from collections import defaultdict

def maximizeHappiness( attendees, happiness ):
	places_to_permute = len(attendees) # actually 1 less, because place 0 is always the same!
	max = 0

	for seating in permutations( range( 1, places_to_permute ) ):
		h = 0
		seating = (0,) + seating # Place 0 is always the same:  rest of table revolves around
		for seat,who in enumerate(seating):
			place_l = (seat-1) % places_to_permute
			place_r = (seat+1) % places_to_permute
			h += happiness[ attendees[who] ][ attendees[seating[place_l]] ]
			h += happiness[ attendees[who] ][ attendees[seating[place_r]] ]
		if h > max:
			max = h

	return max

def main():
	if  len( sys.argv ) != 2 or not os.path.isfile( sys.argv[1] ) :
		print "Invalid argument"
		sys.exit(1)

	with open( sys.argv[1] ) as input_file:
		content = input_file.read().splitlines()

	happiness=defaultdict(lambda: defaultdict(int))
	# We need some way to rigidly order the attendees for permutation
	# That's why we can't just use happiness
	attendees=[]

	for line in content:
		pieces = line.split()
		attendee = pieces[0]
		points = -int(pieces[3]) if pieces[2] == 'lose' else int(pieces[3])
		neighbor = pieces[10][:-1]

		if attendee not in attendees:
			attendees.append(attendee)

		happiness[attendee][neighbor] = points

	print "The Happiest party is %d" % maximizeHappiness( attendees, happiness )

	attendees.append('Me')
	print "The Happiest party with me is %d" % maximizeHappiness( attendees, happiness )


if __name__=="__main__":
	main()

sys.exit(0)
