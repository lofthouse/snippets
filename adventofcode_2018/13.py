#! /usr/bin/env python3
import os
import sys
from pprint import pprint
from collections import deque
import numpy as np

right = np.array([[0,1],[-1,0]])
straight = np.array([[1,0],[0,1]])
left = np.array([[0,-1],[1,0]])

r_slash = np.array([[0,-1],[-1,0]])
l_slash = np.array([[0,1],[1,0]])
slashes = { '/': r_slash, '\\': l_slash }

locations = set()
removed = set()

grid = []
carts = []
ID_counter = 0
x = 0
y = 0

first_collision = False

class Cart:
    def __init__(self,x,y,vector):
        global ID_counter
        self.ID = ID_counter
        ID_counter += 1
        self.position = np.array( (x,y) )
        self.vector = np.array( vector )
        self.intersection = deque( [left,straight,right] )
        locations.add( (x,y) )

    def __lt__(self,other):
        return self.position[1] < other.position[1] or \
               ( self.position[1] == other.position[1] and self.position[0] < other.position[0] )

    def __eq__(self,other):
        return np.array_equal(self.position,other.position)

    def __hash__(self):
        return self.ID

    def __repr__(self):
        return "%3d: (%3d,%3d)" % (self.ID,self.position[0],self.position[1])

    def __str__(self):
        return "(%3d,%3d)" % (self.position[0],self.position[1])

    def tick(self):
        global first_collision,carts

        locations.remove( tuple(self.position) )

        self.position += self.vector

        if tuple(self.position) in locations:
            locations.remove( tuple(self.position) )
            if not first_collision:
                print( f"First collision is at {self}" )
                first_collision = True

            for cart in carts:
                if cart == self:
                    removed.add(cart.ID)
            return

        locations.add( tuple(self.position) )

        segment = grid[self.position[1]][self.position[0]]
        if segment in slashes:
            self.vector = np.matmul( self.vector, slashes[segment] )
        elif segment == '+':
            self.vector = np.matmul( self.vector, self.intersection[0] )
            self.intersection.rotate(-1)

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def pgrid():
    for j in range(y):
        for i in range(x):
            if (i,j) in locations:
                print( "x", end="" )
            else:
                print( grid[j][i], end="" )
        print()

def main():
    global x,y,grid,carts

    lines = readfile()
    x = len( lines[0] )
    y = len( lines )

    c_sym = set( ['<','>','^','v'] )
    c_sym_h = set( ['<','>'] )
    c_sym_v = set( ['^','v'] )
    vectors = { '^': (0,-1), 'v': (0,1), '<': (-1,0), '>': (1,0) }

    grid = [ [" " for i in range(x)] for j in range(y) ]

    for j,line in enumerate(lines):
        for i,segment in enumerate(line):
            if segment in c_sym:
                carts.append( Cart(i,j,vectors[segment]) )
                if segment in c_sym_h:
                    grid[j][i] = '-'
                elif segment in c_sym_v:
                    grid[j][i] = '|'
            else:
                grid[j][i] = segment


    while True:
        carts.sort()

        for cart in carts:
            if cart.ID not in removed:
                cart.tick()

        if len( carts ) - len( removed ) == 1:
            for cart in carts:
                if cart.ID not in removed:
                    print( f"Last elf rolling is at {cart}" )
                    sys.exit(0)


if __name__ == "__main__":
    main()
