#!/usr/bin/env python

import sys
import os.path
from re import findall
from numpy import array,prod,transpose

def parseInput():
	if  len( sys.argv ) != 2 or not os.path.isfile( sys.argv[1] ) :
		print "Invalid argument"
		sys.exit(1)

	with open( sys.argv[1] ) as input_file:
		content = input_file.read().splitlines()

	ingredients=[]

	for line in content:
		tmp = findall(r"-?[0-9]+",line)
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
				max_score = max(max_score, score( (a,b,c,d), ingredients, as_meal ))

	return max_score

def main():
	ingredients = parseInput()
	print "Best Cookie is", optimize( ingredients, False )
	print "Best Meal is", optimize( ingredients, True )

if __name__=="__main__":
	main()

sys.exit(0)
