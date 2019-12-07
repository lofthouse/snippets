#! /usr/bin/env python3
import argparse
from itertools import permutations

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day N')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def run( punchcard, a, b):
    inputs = [ b, a ]
    stack = [ int(i) for i in punchcard.split(",") ]

    i = 0

    while stack[i] != 99:
        modes,op = divmod( stack[i], 100 )

        if op == 1:
            a,b,o = stack[i+1:i+4]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )

            stack[o] = (stack[a] if am==0 else a) + (stack[b] if bm==0 else b)

            i += 4

        elif op == 2:
            a,b,o = stack[i+1:i+4]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )

            stack[o] = (stack[a] if am==0 else a) * (stack[b] if bm==0 else b)

            i += 4

        elif op == 3:
            o = stack[i+1]
            stack[o] = inputs.pop()

            i += 2

        elif op == 4:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )

            return stack[o] if om==0 else o

            i += 2

        elif op == 5:
            a,b = stack[i+1:i+3]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )

            if ( stack[a] if am==0 else a ) != 0:
                i = ( stack[b] if bm==0 else b )
            else:
                i += 3

        elif op == 6:
            a,b = stack[i+1:i+3]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )

            if ( stack[a] if am==0 else a ) == 0:
                i = ( stack[b] if bm==0 else b )
            else:
                i += 3

        elif op == 7:
            a,b,c = stack[i+1:i+4]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )
            modes,cm = divmod( modes, 10 )

            if ( stack[a] if am==0 else a ) < ( stack[b] if bm==0 else b ):
                stack[c] = 1
            else:
                stack[c] = 0

            i += 4

        elif op == 8:
            a,b,c = stack[i+1:i+4]
            modes,am = divmod( modes, 10 )
            modes,bm = divmod( modes, 10 )
            modes,cm = divmod( modes, 10 )

            if ( stack[a] if am==0 else a ) == ( stack[b] if bm==0 else b ):
                stack[c] = 1
            else:
                stack[c] = 0

            i += 4

        else:
            print( "FATAL ERROR: opcode", stack[i], "at", i )
            print( stack )

def main():
    lines = readfile()

    for line in lines:
        results = {}
        for perm in permutations( [0,1,2,3,4] ):
            out = 0
            for phase in perm:
                out = run( line, phase, out )
#            print( perm, "==>", out )
            results[ out ] = perm
        win = max( results )

        print( results[ win ], "===>", win )

if __name__ == "__main__":
    main()
