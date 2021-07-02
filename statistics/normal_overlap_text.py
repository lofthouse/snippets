#! /usr/local/opt/python@3.8/bin/python3

from statistics import NormalDist

inputs = ["Mean A: ", "StdDev A: ", "Mean B: ", "StdDev B: "]

while True:
    ins = []
    for i in range( len( inputs ) ):
        ins.append( float( input( inputs[i] ) ) )

    print( NormalDist(mu=ins[0], sigma=ins[1]).overlap(NormalDist(mu=ins[2], sigma=ins[3])) )
