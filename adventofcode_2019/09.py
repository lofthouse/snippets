#! /usr/bin/env python3
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 09')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
parser.add_argument("input", type=int, help="the input into the Intcode Computer")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def run( punchcard ):
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

        elif op == 3:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )
            address = ( o if om==0 else rb+o )

            stack[address] = args.input

            i += 2

        elif op == 4:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )

            print( stack[o] if om==0 else stack[rb+o] if om==2 else o )

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

def main():
    lines = readfile()

    for line in lines:
        run( line )

if __name__ == "__main__":
    main()
