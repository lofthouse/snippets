#! /usr/bin/env python3
import argparse
from collections import defaultdict
from collections import deque

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 09')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
#parser.add_argument("input", type=int, help="the input into the Intcode Computer")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def run( punchcard, start_tile ):
    hull = defaultdict( int )
    position = [0,0]
    hull[ tuple( position ) ] = start_tile
    mx = my = Mx = My = 0
    direction = deque( [ [0,1], [1,0], [0,-1], [-1,0] ] )
    painting = True

    rb = 0

    stack = defaultdict( int )
    for address,i in enumerate( punchcard.split(",") ):
        stack[ address ] = int( i )

    i = 0

    while stack[i] != 99:
        modes,op = divmod( stack[i], 100 )

        if op == 1:
            a = stack[i+1]
            b = stack[i+2]
            o = stack[i+3]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )
            modes,om = divmod( modes, 10 )
            address = ( o if om==0 else rb+o )

            stack[address] = (stack[a] if am==0 else stack[rb+a] if am==2 else a) + (stack[b] if bm==0 else stack[rb+b] if bm==2 else b)

            i += 4

        elif op == 2:
            a = stack[i+1]
            b = stack[i+2]
            o = stack[i+3]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )
            modes,om = divmod( modes, 10 )
            address = ( o if om==0 else rb+o )

            stack[address] = (stack[a] if am==0 else stack[rb+a] if am==2 else a) * (stack[b] if bm==0 else stack[rb+b] if bm==2 else b)

            i += 4

        # Taking input
        elif op == 3:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )
            address = ( o if om==0 else rb+o )

            stack[address] = hull[ tuple(position) ]

            i += 2

        # Creating Output
        elif op == 4:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )

            if painting:
                hull[ tuple(position) ] = (stack[o] if om==0 else stack[rb+o] if om==2 else o)
                painting = False
            else:
                if (stack[o] if om==0 else stack[rb+o] if om==2 else o) == 0:
                    direction.rotate(1)
                else:
                    direction.rotate(-1)

                position = [ p+d for p,d in zip( position, direction[0] ) ]
                mx = min( mx, position[0] )
                Mx = max( Mx, position[0] )
                my = min( my, position[1] )
                My = max( My, position[1] )

                painting = True

            i += 2

        elif op == 5:
            a = stack[i+1]
            b = stack[i+2]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )

            if ( stack[a] if am==0 else stack[rb+a] if am==2 else a ) != 0:
                i = ( stack[b] if bm==0 else stack[rb+b] if bm==2 else b )
            else:
                i += 3

        elif op == 6:
            a = stack[i+1]
            b = stack[i+2]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )

            if ( stack[a] if am==0 else stack[rb+a] if am==2 else a ) == 0:
                i = ( stack[b] if bm==0 else stack[rb+b] if bm==2 else b )
            else:
                i += 3

        elif op == 7:
            a = stack[i+1]
            b = stack[i+2]
            c = stack[i+3]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )
            modes,cm = divmod( modes, 10 )
            address = ( c if cm==0 else rb+c )

            if ( stack[a] if am==0 else stack[rb+a] if am==2 else a ) < ( stack[b] if bm==0 else stack[rb+b] if bm==2 else b ):
                stack[address] = 1
            else:
                stack[address] = 0

            i += 4

        elif op == 8:
            a = stack[i+1]
            b = stack[i+2]
            c = stack[i+3]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )
            modes,cm = divmod( modes, 10 )
            address = ( c if cm==0 else rb+c )

            if ( stack[a] if am==0 else stack[rb+a] if am==2 else a ) == ( stack[b] if bm==0 else stack[rb+b] if bm==2 else b ):
                stack[address] = 1
            else:
                stack[address] = 0

            i += 4

        elif op == 9:
            a = stack[i+1]
            modes,am = divmod( modes, 10 )

            rb += ( stack[a] if am==0 else stack[rb+a] if am==2 else a )

            i += 2

        else:
            print( "FATAL ERROR: opcode", stack[i], "at", i )
            print( stack )

    print( "We're done!" )
    print( "We painted", len( hull ), "panels" )
    for j in range(My, my-1, -1 ):
        for i in range( mx, Mx + 1):
            if hull[ (i,j) ] == 0:
                print( " ", end="" )
            else:
                print( "#", end="" )
        print()

def main():
    lines = readfile()

    run( lines[0], 0 )
    run( lines[0], 1 )

if __name__ == "__main__":
    main()
