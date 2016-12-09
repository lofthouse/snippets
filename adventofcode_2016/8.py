#!/usr/bin/env python

import sys
import os
import time

x=50
y=6

def print_panel():
	tmp=os.system('clear')
	for j in range(y):
		for i in range(x):
			if panel[i][j]:
				print '#',
			else:
				print ' ',
		print
	time.sleep(0.02)

def rotate(row,shift):
	return row[-int(shift):]+row[:-int(shift)]

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

panel=[[0 for j in range(6)] for i in range(50)]

print_panel()

for line in content:
	buffer=line.split()
	if buffer[0]=='rect':
		coords=buffer[1].split('x')
		for i in range(int(coords[0])):
			for j in range(int(coords[1])):
				panel[i][j]=1
	if buffer[0]=='rotate':
		if buffer[1]=='row':
			r=int(buffer[2][-1])
			row=[ panel[i][r] for i in range(x) ]
			row=rotate(row,buffer[4])
			for i in range(x):
				panel[i][r]=row[i]
		else: #column
			col=int(buffer[2].split('=')[-1])
			panel[col]=rotate(panel[col],buffer[4])
	print_panel()

print "That took",sum(sum(panel,[])),"pixels"

sys.exit(0)
