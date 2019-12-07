#! /usr/bin/env python3
import argparse
from itertools import permutations
from threading import Thread, enumerate
from queue import Queue

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day N')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def run( punchcard, id, next ):
    if args.verbose:
        print( "Thread", id, "starting!" )

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
            stack[o] = queues[ id ].get()
            if args.verbose:
                print( "Thread", id, "here receiving", stack[o] )
            queues[ id ].task_done()

            i += 2

        elif op == 4:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )

            if args.verbose:
                print( "Thread", id, "here sending along", stack[o] if om==0 else o )
            queues[ next ].put( stack[o] if om==0 else o )

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

    alive[ id ].get()
    alive[ id ].task_done()

def main():
    lines = readfile()

    for line in lines:
        results = {}
        for perm in permutations( [5,6,7,8,9] ):
            threads = {}
            global queues
            global alive
            queues = { "A":Queue(), "B":Queue(), "C":Queue(), "D":Queue(), "E":Queue() }
            queues[ "A" ].put( perm[0] )
            queues[ "B" ].put( perm[1] )
            queues[ "C" ].put( perm[2] )
            queues[ "D" ].put( perm[3] )
            queues[ "E" ].put( perm[4] )

            alive = { "A":Queue(), "B":Queue(), "C":Queue(), "D":Queue(), "E":Queue() }
            alive[ "A" ].put( True )
            alive[ "B" ].put( True )
            alive[ "C" ].put( True )
            alive[ "D" ].put( True )
            alive[ "E" ].put( True )

            threads[ "A" ] = Thread(target=run, args=( line, "A", "B" ) )
            threads[ "B" ] = Thread(target=run, args=( line, "B", "C" ) )
            threads[ "C" ] = Thread(target=run, args=( line, "C", "D" ) )
            threads[ "D" ] = Thread(target=run, args=( line, "D", "E" ) )
            threads[ "E" ] = Thread(target=run, args=( line, "E", "A" ) )

            for t in threads:
                threads[t].start()

            queues[ "A" ].put(0)

            for a in alive:
                alive[a].join()

            if args.verbose:
                print( "All threads should be dead now" )

            for t in threads:
                threads[t].join()

#            print( queues )
#            out = run( line, phase, out )
#            print( perm, "==>", out )
#            results[ out ] = perm
#        win = max( results )

#        print( results[ win ], "===>", win )

if __name__ == "__main__":
    main()
