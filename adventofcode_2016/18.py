#!/usr/bin/env python

import sys
import os.path

safe_count=0

def rowFrom(row):
	global safe_count
	new_row='.'

	for n in range(1,len(row)-1):
		if row[n-1] == row[n+1]:
			new_row += '.'
			safe_count += 1
		else:
			new_row += '^'

	return new_row + '.'

if len(sys.argv) == 3:
	num_rows=int(sys.argv[1])
	with open(sys.argv[2]) as input_file:
		rows=[ '.' + input_file.read().splitlines()[0] + '.' ]
	safe_count += rows[0].count('.') - 2
else:
	print "Usage: <rows> <row1_file.txt>"
	sys.exit(0)

while len(rows) < num_rows:
	rows.append(rowFrom(rows[-1]))

#for row in rows:
#	print row[1:-1]
#	safe_count += row.count('.') - 2

print "There are %d safe tiles" % safe_count
