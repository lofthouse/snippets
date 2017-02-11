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
	if sum(recipe) != 100:
		return 0

	nutritional_value = [ sum(i) for i in ingredients*recipe ]
	nutritional_value = array( [ max(0,i) for i in nutritional_value ] )

	if not use_calories:
		nutritional_value = nutritional_value[:-1]

	return -prod(nutritional_value)

def main():
	ingredients = parseInput()
	bnds = [ (0,100) for i in ingredients[0] ]

	print ingredients
	print bnds

	res = brute(lambda x: score(x, ingredients, False), bnds, finish=None, Ns=50)
	print res
	print score( res, ingredients, False )


if __name__=="__main__":
	main()

sys.exit(0)
