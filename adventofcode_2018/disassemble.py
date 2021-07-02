#! /usr/bin/env python3
import os
import sys

symtable = {
    'add':'+',
    'mul':'*',
    'ban':'&',
    'bor':'|'
    }

testtable = {
    'gt':'>',
    'eq':'=='
    }


def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    lines = readfile()
    ln = 0

    for line in lines:
        pieces = line.split()

        if pieces[0][:3] in symtable:
            if pieces[0][3] == 'i':
                print( f"{ln}\treg[{pieces[3]}] = reg[{pieces[1]}] {symtable[pieces[0][:3]]} {pieces[2]}\t{line}" )
            else:
                print( f"{ln}\treg[{pieces[3]}] = reg[{pieces[1]}] {symtable[pieces[0][:3]]} reg[{pieces[2]}]\t{line}" )
        elif pieces[0][:2] in testtable:
            if pieces[0][2:4] == 'ir':
                print( f"{ln}\treg[{pieces[3]}] = {pieces[1]} {testtable[pieces[0][:2]]} reg[{pieces[2]}]\t{line}" )
            elif pieces[0][2:4] == 'ri':
                print( f"{ln}\treg[{pieces[3]}] = reg[{pieces[1]}] {testtable[pieces[0][:2]]} {pieces[2]}\t{line}" )
            else:
                print( f"{ln}\treg[{pieces[3]}] = reg[{pieces[1]}] {testtable[pieces[0][:2]]} reg[{pieces[2]}]\t{line}")
        elif pieces[0][:3] == 'set':
            if pieces[0][3] == 'i':
                print( f"{ln}\treg[{pieces[3]}] = {pieces[1]}\t{line}" )
            else:
                print( f"{ln}\treg[{pieces[3]}] = reg[{pieces[1]}]\t{line}")
        else:
            print( "INVALID INSTRUCTION: ",line )
            continue

        ln += 1


if __name__ == "__main__":
    main()
