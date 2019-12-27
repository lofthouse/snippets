#! /usr/bin/env python3
import argparse
import operator
from functools import reduce
from numpy import array


parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 12')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
parser.add_argument("n", type=int, help="the number of steps to stop at")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

# Stolen from https://stackoverflow.com/questions/15347174/python-finding-prime-factors
def prime_factors( n ):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)

    return factors

def main():
    print( "WARNING:  this will take about a minute to run.  Ctrl-C to give up..." )

    axes = [ 'x', 'y', 'z' ]
    p = { 'x': array([0,0,0,0]), 'y': array([0,0,0,0]), 'z': array([0,0,0,0]) }
    v = { 'x': array([0,0,0,0]), 'y': array([0,0,0,0]), 'z': array([0,0,0,0]) }

    lines = readfile()
    # format: <x=-1, y=0, z=2>
    for i,line in enumerate(lines):
        x,y,z = [ int( l.strip(" xyz=") ) for l in line.strip("<>").split(",") ]
        p['x'][i] = x
        p['y'][i] = y
        p['z'][i] = z


    pot = array([0,0,0,0])
    kin = array([0,0,0,0])
    pf = {}

    for axis in axes:
        i_p_state = tuple( p[axis] )

        step = 0
        cycled = False

        while not cycled:
            for m in range(4):
                v[axis][m] -= sum( p[axis] < p[axis][m] )
                v[axis][m] += sum( p[axis] > p[axis][m] )
            p[axis] += v[axis]

            step += 1

            if args.verbose:
                print( "After", step, "steps:" )
                pprint( p )
                pprint( v )

            if step == args.n:
                pot += abs( p[axis] )
                kin += abs( v[axis] )

            if all( v[axis] == 0 ):
                if tuple( p[axis] ) == i_p_state:
                    print( "Found cycle after", step, "steps for axis", axis )
                    cycled = True

        pf[ axis ] = prime_factors( step )

    print( "Total Energy at step %d: %d" % (args.n, sum( [ a*b for a,b in zip(pot,kin) ] ) ) )

    answer_factors = []
    # Kludgy, but it works.  Basically hardcoding the "take out any common factor in 2 or more numbers"
    # rule to find the LCM by doing x-y-z, then y-z
    for factor in pf[ 'x' ]:
        if factor in pf[ 'y' ] or factor in pf['z']:
            try:
                pf[ 'y' ].remove( factor )
                pf[ 'z' ].remove( factor )
            except IndexError:
                pass
        answer_factors.append( factor )

    for factor in pf[ 'y' ]:
        if factor in pf['z']:
                pf[ 'z' ].remove( factor )
        answer_factors.append( factor )

    answer_factors += pf[ 'z' ]

    print( "The universe returns to the starting state after", reduce(operator.mul, answer_factors, 1), "steps" )


if __name__ == "__main__":
    main()
