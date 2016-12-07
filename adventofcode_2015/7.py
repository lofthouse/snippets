#!/usr/bin/env python

import sys
import hashlib
import json
import os.path
#import string

def hashDict(dictionary):
	return hashlib.md5(json.dumps(dictionary, sort_keys=True)).hexdigest()

def getinput(wires,gate):
	if gate.isdigit() :
		return int(gate)
	else:
		return wires[gate]


class ANDGate:
	def __init__(self,in_A,in_B,out,wires):
		self.in_A=in_A
		self.in_B=in_B
		self.out=out
		wires[self.out]=0

	def tick(self,wires):
		wires[self.out] = getinput(wires,self.in_A) & getinput(wires,self.in_B)

class ORGate:
	def __init__(self,in_A,in_B,out,wires):
		self.in_A=in_A
		self.in_B=in_B
		self.out=out
		wires[self.out]=0

	def tick(self,wires):
		wires[self.out] = getinput(wires,self.in_A) | getinput(wires,self.in_B)

class LSHIFTGate:
	def __init__(self,input,shift,out,wires):
		self.input=input
		self.shift=shift
		self.out=out
		wires[self.out]=0

	def tick(self,wires):
		wires[self.out] = getinput(wires,self.input) << self.shift

class RSHIFTGate:
	def __init__(self,input,shift,out,wires):
		self.input=input
		self.shift=shift
		self.out=out
		wires[self.out]=0

	def tick(self,wires):
		wires[self.out] = getinput(wires,self.input) >> self.shift

class NOTGate:
	def __init__(self,input,out,wires):
		self.input=input
		self.out=out
		wires[self.out]=0

	def tick(self,wires):
		wires[self.out] = 65536 - getinput(wires,self.input) - 1

class ASSIGNGate:
	def __init__(self,input,out,wires):
		self.input=input
		self.out=out
		wires[self.out]=0

	def tick(self,wires):
		wires[self.out]=getinput(wires,self.input)


with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

gates=[]
wires={}
hash=''
ticks=0

for line in content:
	if not line :
		continue
	parse=line.split()
	if 'AND' in parse :
		gates.append(ANDGate(parse[0],parse[2],parse[4],wires))
	elif 'OR' in parse :
		gates.append(ORGate(parse[0],parse[2],parse[4],wires))
	elif 'LSHIFT' in parse :
		gates.append(LSHIFTGate(parse[0],int(parse[2]),parse[4],wires))
	elif 'RSHIFT' in parse :
		gates.append(RSHIFTGate(parse[0],int(parse[2]),parse[4],wires))
	elif 'NOT' in parse :
		gates.append(NOTGate(parse[1],parse[3],wires))
	else :
		gates.append(ASSIGNGate(parse[0],parse[2],wires))

while hash != hashDict(wires) :
	hash = hashDict(wires)
	ticks += 1
	for gate in gates:
		gate.tick(wires)

print "That took",ticks,"ticks"
print "Wire a is",wires['a']
print "Wire b is",wires['b']
print

gates = [ gate for gate in gates if not gate.out == 'b' ]

gates.append(ASSIGNGate(str(wires['a']),'b',wires))

for key in wires:
	wires[key]=0

ticks=0
while hash != hashDict(wires) :
	hash = hashDict(wires)
	ticks += 1
	for gate in gates:
		gate.tick(wires)

print "That took",ticks,"ticks"
print "Wire a is",wires['a']
print "Wire b is",wires['b']

sys.exit(0)
