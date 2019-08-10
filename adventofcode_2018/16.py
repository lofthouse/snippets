#! /usr/bin/env python3
import os
import sys

def execute( cmd, reg_in, hint ):
    reg_mode = hint[-1] == 'r'
    cmd_mode = hint[:-1]

    reg_out = list( reg_in )

    opcode,A,B,C = cmd

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
            else:
                reg_out[ C ] = 1 if reg_out[ A ] == B else 0
    # Total cheat:  this problem can't generate negative numbers, so just return a negative register if we encountered an invalid command for the instruction
    except IndexError:
        reg_out = [-1,-1,-1,-1]

    return tuple( reg_out )

def part1( data ):
    # opcodes will accumulate all the viable opcode strings for each opcode value
    opcodes = [ set() for i in range(16) ]
    cmds = ['addr','addi','mulr','muli','banr','bani','borr','bori','setr','seti','gtir','gtri','gtrr','eqir','eqri','eqrr']
    three_pluses = 0

    for case in data:
        matches = 0
        for hint in cmds:
            if execute(case[1],case[0],hint) == case[2]:
                opcodes[ case[1][0] ].add( hint )
                matches += 1
        if matches >= 3:
            three_pluses += 1

    print( three_pluses, "samples match 3 or more opcodes" )

    resolved = set()

    # Solving the opcodes is easy:  just keep eliminating solved codes from other candidate lists until all are solved
    # We got lucky and no more advanced logic is required
    while any( len(p)>1 for p in opcodes ):
        for q in opcodes:
            if len(q) == 1:
                opcode = list(q)[0]
                if opcode not in resolved:
                    resolved.add( opcode )
                    for r in opcodes:
                        if q != r:
                            r.discard( opcode )

    # now the instruction set is just the list of only set members in opcodes
    instructionset = [ list(q)[0] for q in opcodes ]

    return( instructionset )

def part2( data, instructionset ):
    registers = (0,0,0,0)
    for cmd in data:
        registers = execute( cmd, registers, instructionset[ cmd[0] ] )

    print( registers[0], "is the final value in register 0" )

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def main():
    lines = readfile()
    p1 = []
    p2 = []
    p1_case = None

    for line in lines:
        if line:
            if p1_case:
                if line.startswith("After"):
                    p1_case.append( tuple( int(i) for i in line.split("[")[1].split("]")[0].split(", ") ) )
                    p1.append( p1_case )
                    p1_case = None
                else:
                    p1_case.append( tuple( int(i) for i in line.split() ) )
            else:
                if line.startswith("Before"):
                    p1_case = [ tuple( int(i) for i in line.split("[")[1].split("]")[0].split(", ") ) ]
                else:
                    p2.append( tuple( int(i) for i in line.split() ) )

    instructionset = part1( p1 )
    part2( p2, instructionset )

if __name__ == "__main__":
    main()
