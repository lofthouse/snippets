#!/usr/bin/env python

import sys
import os.path
from operator import add

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

# Keypad
'''
    1
  2 3 4
5 6 7 8 9
  A B C
    D
'''

buttons={
	  1:{'U':1,   'D':3,   'L':1,   'R':1},
	  2:{'U':2,   'D':6,   'L':2,   'R':3},
	  3:{'U':1,   'D':7,   'L':2,   'R':4},
	  4:{'U':4,   'D':8,   'L':3,   'R':4},
	  5:{'U':5,   'D':5,   'L':5,   'R':6},
	  6:{'U':2,   'D':'A', 'L':5,   'R':7},
	  7:{'U':3,   'D':'B', 'L':6,   'R':8},
	  8:{'U':4,   'D':'C', 'L':7,   'R':9},
	  9:{'U':9,   'D':9,   'L':8,   'R':9},
	'A':{'U':6,   'D':'A', 'L':'A', 'R':'B'},
	'B':{'U':7,   'D':'D', 'L':'A', 'R':'C'},
	'C':{'U':8,   'D':'C', 'L':'B', 'R':'C'},
	'D':{'U':'B', 'D':'D', 'L':'D', 'R':'D'},
	}

here=5
print "The bathroom code is",

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

for line in content:
	for c in line:
		here=buttons[here][c]
	print here,

sys.exit(0)
