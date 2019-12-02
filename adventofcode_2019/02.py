#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def run( input, noun, verb ):
    stack = [ int(i) for i in input.split(",") ]

    i = 0
    stack[1] = noun
    stack[2] = verb

    while stack[i] != 99:
        a,b,o = stack[i+1:i+4]

        if stack[i] == 1:
            stack[o] = stack[a] + stack[b]
            i +=4
        elif stack[i] == 2:
            stack[o] = stack[a] * stack[b]
            i +=4
        else:
            print( "FATAL ERROR: opcode", stack[i], "at", i )
            print( stack )

    return stack[0]

def main():
    lines = readfile()

    for line in lines:
        print( "Part 1:", run( line, 12, 2 ) )

        for i in range(100):
            for j in range(100):
                if run( line, i, j ) == 19690720:
                    print( "Part 2:", 100*i+j, "(noun=",i,", verb=",j,")" )
                    return

if __name__ == "__main__":
    main()
