#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def run( punchcard ):
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
            ui = input( 'Intcode: ' )
            stack[o] = int( ui )

            i += 2

        elif op == 4:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )

            print( stack[o] if om==0 else o )

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
        run( line )

if __name__ == "__main__":
    main()
