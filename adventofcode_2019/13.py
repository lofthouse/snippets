#! /usr/bin/env python3
import argparse
import readchar
from collections import defaultdict
from collections import deque

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 09')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-i", "--interactive", help="Actually play the game",action="store_true")
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
#parser.add_argument("input", type=int, help="the input into the Intcode Computer")
args = parser.parse_args()

# Screen boundaries to be populated during Part 1
mx = my = Mx = My = 0

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def run( punchcard, part, interactive ):
    global mx,my,Mx,My
    playing = False

    tiles = defaultdict( list )
    screenbuffer = []
    score = 0

    rb = 0

    stack = defaultdict( int )
    for address,i in enumerate( punchcard.split(",") ):
        stack[ address ] = int( i )

    i = 0

    if part == 2:
        stack[ 0 ] = 2

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

            playing = True
            joystick = 0
            if interactive:
                keypress = readchar.readkey()
                if keypress == readchar.key.LEFT:
                    joystick = -1
                elif keypress == readchar.key.RIGHT:
                    joystick = 1

            stack[address] = joystick

            i += 2

        # Creating Output
        elif op == 4:
            o = stack[i+1]
            modes,om = divmod( modes, 10 )

            screenbuffer.append( stack[o] if om==0 else stack[rb+o] if om==2 else o )

            if len( screenbuffer ) == 3:
                x,y,tile = screenbuffer

                if x == -1 and y == 0:
                    score = tile
                else:
                    for t in tiles:
                        try:
                            tiles[ t ].remove( tuple( [x,y] ) )
                        except ValueError:
                            pass
                    tiles[ tile ].append( tuple( [x,y] ) )
                    if part == 1:
                        mx = min( mx, x )
                        Mx = max( Mx, x )
                        my = min( my, y )
                        My = max( My, y )
                    elif playing and interactive:
                        # Clear Screen
                        print( chr(27) + "[2J" )

                        # Full redraw:  time to learn ncurses again...
                        print( "Score:", score )
                        for y in range(My, my-1, -1 ):
                            print()
                            for x in range( mx, Mx + 1):
                                # empty
                                if (x,y) in tiles[0]:
                                    print( " ", end="" )
                                # wall
                                elif (x,y) in tiles[1]:
                                    print( "#", end="" )
                                # block
                                elif (x,y) in tiles[2]:
                                    print( "|", end="" )
                                # paddle
                                elif (x,y) in tiles[3]:
                                    print( "=", end="" )
                                # ball
                                elif (x,y) in tiles[4]:
                                    print( "O", end="" )
                                else:
                                    print( "?", end="" )

                screenbuffer = []

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
            raise SystemExit(1)

    if part == 1:
        print( "We painted", len( tiles[2] ), "blocks" )
    if part == 2:
        print( "The final score was", score )

def main():
    print( "To avoid having to play Part 2, edit the input file to make the entire '3' row of gameboard data solid 3's.  It should begin at character 4097" )

    lines = readfile()

    run( lines[0], 1, False )
    run( lines[0], 2, args.interactive )

if __name__ == "__main__":
    main()
