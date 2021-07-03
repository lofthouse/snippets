#! /usr/bin/env python3
import os
import sys

p1 = False
iterations = 1
seen = set()

def execute( cmd, reg_in ):
    global p1
    global iterations
    global seen

    reg_out = list( reg_in )

    command,A,B,C = cmd
    reg_mode = command[-1] == 'r'
    cmd_mode = command[:-1]

    try:
        if cmd_mode == 'add':
            if reg_mode:
                reg_out[ C ] = reg_out[ A ] + reg_out[ B ]
            else:
                reg_out[ C ] = reg_out[ A ] + B

        elif cmd_mode == 'mul':
            if reg_mode:
                reg_out[ C ] = reg_out[ A ] * reg_out[ B ]
            else:
                reg_out[ C ] = reg_out[ A ] * B

        elif cmd_mode == 'ban':
            if reg_mode:
                reg_out[ C ] = reg_out[ A ] & reg_out[ B ]
            else:
                reg_out[ C ] = reg_out[ A ] & B

        elif cmd_mode == 'bor':
            if reg_mode:
                reg_out[ C ] = reg_out[ A ] | reg_out[ B ]
            else:
                reg_out[ C ] = reg_out[ A ] | B

        elif cmd_mode == 'set':
            if reg_mode:
                reg_out[ C ] = reg_out[ A ]
            else:
                reg_out[ C ] = A

        elif cmd_mode == 'gti':
            if reg_mode:
                reg_out[ C ] = 1 if A > reg_out[ B ] else 0
            else:
                print( "Fatal ERROR:  no such opcode 'gtii'" )
                exit(-1)

        elif cmd_mode == 'gtr':
            if reg_mode:
                reg_out[ C ] = 1 if reg_out[ A ] > reg_out[ B ] else 0
            else:
                reg_out[ C ] = 1 if reg_out[ A ] > B else 0

        elif cmd_mode == 'eqi':
            if reg_mode:
                reg_out[ C ] = 1 if A == reg_out[ B ] else 0
            else:
                print( "Fatal ERROR:  no such opcode 'eqii'" )
                exit(-1)

        elif cmd_mode == 'eqr':
            if reg_mode:
                reg_out[ C ] = 1 if reg_out[ A ] == reg_out[ B ] else 0
                if not p1:
                    print( f"Part 1: {reg_out[A]}")
                    p1 = True
                else:
                    print( f"{iterations}\r", end='' )
                if reg_out[A] in seen:
                    print( f"\nPart 2: {previous}")
                    exit(0)
                previous = reg_out[A]
                seen.add( reg_out[A] )
                iterations += 1
            else:
                reg_out[ C ] = 1 if reg_out[ A ] == B else 0
    # Total cheat:  this problem can't generate negative numbers, so just return a negative register if we encountered an invalid command for the instruction
    except IndexError:
        reg_out = [-1,-1,-1,-1]

    return reg_out

def part( ip_shadow, program, start_state ):
    registers = start_state
    ip = 0

    while ip < len(program) and all( i>=0 for i in registers ):
#    while ip < len(program) and all( i>=0 for i in registers ) and ip != 1:
        registers[ ip_shadow ] = ip
        cmd = program[ ip ]
        registers = execute( cmd, registers )
        ip = registers[ ip_shadow ]
        ip += 1

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def main():
    lines = readfile()
    ip_shadow = 0
    program = []

    for line in lines:
        if line:
            if line.startswith("#ip"):
                ip_shadow = int( line.split()[1] )
            else:
                scratch = line.split()
                program.append( ( scratch[0], int(scratch[1]), int(scratch[2]), int(scratch[3]) ) )

# seed registers for fun!
# put your own input in [2] and then just modify the program to jump to 1 instead of 16 and let the fun begin
# to see inputs, modify the second line of the program to jump out of bounds
    part( ip_shadow, program, [0,0,0,0,0,0] )


if __name__ == "__main__":
    main()
