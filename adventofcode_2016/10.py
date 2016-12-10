#!/usr/bin/env python

import sys
import os.path

class bot:
	def __init__(self,id,low=None,high=None):
		self.id=id
		self.values=[]

	def set(self,low,high):
		self.low=low
		self.high=high

	def give(self):
		if self.id.startswith('output'):
			return
		if len(self.values) == 2:
			bots[self.low].receive(min(self.values))
			bots[self.high].receive(max(self.values))
			del self.values[:]

	def receive(self,value):
		if value not in self.values:
			self.values.append(value)
		if 17 in self.values and 61 in self.values:
			print "I'm bot %s and just found the golden ticket!" % self.id
			print "I have",self.values

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

bots={}

for line in content:
	if not line :
		continue
	parse=line.split()
	if 'gives' in parse:
		bot_id='bot'+parse[1]
		low_id=parse[5]+parse[6]
		high_id=parse[10]+parse[11]

		for id in (bot_id,low_id,high_id):
			if not id in bots:
				bots[ id ] = bot( id )

		bots[ bot_id ].set( low_id, high_id )

	elif 'value' in parse:
		bot_id = 'bot'+parse[5]
		if not bot_id in bots:
			bots[ bot_id ] = bot( bot_id )
		bots[ bot_id ].values.append( int(parse[1]) )

	else:
		print "Unable to parse %s" % line

outs={out:bots[out] for out in bots if out.startswith('output')}
while True:
	for bot in bots:
		bots[bot].give()

	done=True
	for out in outs.values():
		if not out.values:
			done=False
	if done:
		print outs['output0'].values[0]*outs['output1'].values[0]*outs['output2'].values[0]
		sys.exit(0)
