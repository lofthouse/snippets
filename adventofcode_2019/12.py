#! /usr/bin/env python3
import argparse
import numpy as np
from pprint import pprint
from itertools import combinations

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 12')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
parser.add_argument("n", type=int, help="the number of steps to stop at")
args = parser.parse_args()

class moon:
    def __init__(self, x, y, z):
        self.p = np.array( (x,y,z) )
        self.v = np.array( (0,0,0) )

    def apply_g(self, target):
        for i in range(3):
            d = -1 if (target.p[i] < self.p[i]) else \
                0 if (target.p[i] == self.p[i]) else \
                1
            target.v[i] -= d
            self.v[i] += d

    def apply_v(self):
        self.p += self.v

    def energy(self):
        pot = sum( [ abs(i) for i in self.p ] )
        kin = sum( [ abs(i) for i in self.v ] )
        if args.verbose:
            print( "pot: %3d;   kin: %3d;   total: %d" % (pot, kin, pot*kin) )
        return pot*kin

    def __repr__(self):
        return "pos=<x=%3d, y=%3d, z=%3d>, vel=<x=%3d, y=%3d, z=%3d>" % (self.p[0],self.p[1],self.p[2],self.v[0],self.v[1],self.v[2])

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def state( moons ):
    return [ tuple( np.concatenate( [m.p,m.v] ) ) for m in moons ]

def main():
    moons=[]
    lines = readfile()
    # format: <x=-1, y=0, z=2>
    for line in lines:
        x,y,z = [ int( l.strip(" xyz=") ) for l in line.strip("<>").split(",") ]
        moons.append( moon( x,y,z ) )

    i_state = state( moons )
    pprint( moons )

    step = 0
    cycles = {}

    while len( cycles ) < 3:
#    for step in range( args.n ):
        for a,b in combinations( moons, 2 ):
            a.apply_g( b )
        for m in moons:
            m.apply_v()

        if args.verbose:
            print( "After", step+1, "steps:" )
            pprint( moons )

        step += 1
        if step == args.n:
            E = 0
            for m in moons:
                E += m.energy()

            print( "Sum of total energy: ", E )

        c_state = state( moons )
        for i in range(3):
            if c_state[i] == i_state[i]:
                print( "Found cycle after", step, "steps for axis", i )
                cycles[i] = step
                pprint( moons )


if __name__ == "__main__":
    main()
