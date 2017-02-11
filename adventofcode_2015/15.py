#!/usr/bin/env python

import sys
import os.path
from numpy import array,prod,transpose
from scipy.optimize import brute

def parseInput():
	if  len( sys.argv ) != 2 or not os.path.isfile( sys.argv[1] ) :
		print "Invalid argument"
		sys.exit(1)

	with open( sys.argv[1] ) as input_file:
		content = input_file.read().splitlines()

	ingredients=[]

	for line in content:
		tmp = line.replace(',','').split()
		tmp = [ tmp[2], tmp[4], tmp[6], tmp[8], tmp[10] ]
		ingredients.append( [ int(x) for x in tmp ] )

	return transpose(array(ingredients))

def score( recipe, ingredients, use_calories ):
	nutritional_value = array( [ max(0,sum(i)) for i in ingredients*recipe ] )

	if use_calories:
		if nutritional_value[-1] != 500:
			return 0

	return prod(nutritional_value[:-1])

def optimize( ingredients, as_meal ):
	max_score = 0

	for a in range(101):
		for b in range(101-a):
			for c in range(101-(a+b)):
				d = 100-(a+b+c)
				n = score( (a,b,c,d), ingredients, as_meal )
				if n > max_score:
					max_score = n
					max_recipe = (a,b,c,d)

	print max_score,":",max_recipe

def main():
	ingredients = parseInput()
	optimize( ingredients, False )
	optimize( ingredients, True )

if __name__=="__main__":
	main()

sys.exit(0)
