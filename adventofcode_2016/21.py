#!/usr/bin/env python

import sys
import os.path

if len(sys.argv) < 3:
	print "Usage:  25.py <password to scramble> <instruction file>"
	sys.exit(1)

password=sys.argv[1]

with open(sys.argv[2]) as input_file:
	content = input_file.read().splitlines()

content=[line.split() for line in content]

def abort(line):
	print "invalid command",line
	sys.exit(1)


def rot_r(password,positions):
	n=positions%len(password)
	return password[-n:]+password[:-n]

def rot_l(password,positions):
	n=positions%len(password)
	return password[n:]+password[:n]

def scramble(password,line):
	cmd=line[0]

	if cmd=='swap':
		if line[1]=='position':
			x=int(line[2])
			y=int(line[5])
			if y<x:
				tmp=x
				x=y
				y=tmp
			password=password[:x]+password[y]+password[x+1:y]+password[x]+password[y+1:]
		elif line[1]=='letter':
			x=line[2]
			y=line[5]
			password=password.replace(x,'#')
			password=password.replace(y,x)
			password=password.replace('#',y)
		else:
			abort(line)

	if cmd=='rotate':
		if line[1]=='left':
			password=rot_l(password,int(line[2]))
		elif line[1]=='right':
			password=rot_r(password,int(line[2]))
		elif line[1]=='based':
			index=password.index(line[6])
			if not index:
				abort(line)
			password=rot_r(password,1+index+(0 if index < 4 else 1))
		else:
			abort(line)

	if cmd=='reverse':
		beg=int(line[2])
		end=int(line[4])
		tmp=password[beg:end+1]
		tmp=tmp[::-1]

		password=password[:beg]+tmp+password[end+1:]

	if cmd=='move':
		orig=int(line[2])
		dest=int(line[5])
		letter=password[orig]
		password=password[:orig]+password[orig+1:]
		password=password[:dest]+letter+password[dest:]

	return password

for line in content:
	password=scramble(password,line)

print password

sys.exit(0)
