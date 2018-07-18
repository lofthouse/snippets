#!/usr/bin/env python
from __future__ import print_function
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print( " ".join(map(str,args)) )

def checkArgs():
    if len(sys.argv) != 2 :
        print( "Invalid argument" )
        print( "%s <input file>" % sys.argv[0] )
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print( "%s is not a file" % sys.argv[1] )
        sys.exit(1)

def loadBinary():
    memory = []

    with open(sys.argv[1], 'rb') as file:
        while True:
            low = file.read(1)
            high = file.read(1)

            if low and high:
                memory.append( int(ord(low)) + 256 * int(ord(high)) )
            else:
                break

    return memory

# Begin actual code

### vm instructions ###

def halt():
    return False

def set():
    global ptr
    write_register( ptr + 1 , read_memory( ptr + 2 ) )

    ptr = ptr + 3

def push():
    global ptr
    global stack

    stack.append( read_memory( ptr + 1 ) )
    ptr = ptr + 2

def pop():
    global ptr
    global stack

    if len(stack) > 0:
        write_register( ptr + 1, stack.pop() )
        ptr = ptr + 2
    else:
        print( "Popped empty stack:  system halting" )
        sys.exit(1)

def eq():
    global ptr

    if read_memory( ptr + 2 ) == read_memory( ptr + 3 ):
        write_register( ptr + 1, 1 )
    else:
        write_register( ptr + 1, 0 )

    ptr = ptr + 4

def gt():
    global ptr

    if read_memory( ptr + 2 ) > read_memory( ptr + 3 ):
        write_register( ptr + 1, 1 )
    else:
        write_register( ptr + 1, 0 )

    ptr = ptr + 4

def jmp():
    global ptr
    ptr = read_memory( ptr + 1 )

def jt():
    global ptr

    if not read_memory( ptr + 1 ) == 0:
        ptr = read_memory( ptr + 2 )
    else:
        ptr = ptr + 3

def jf():
    global ptr

    if read_memory( ptr + 1 ) == 0:
        ptr = read_memory( ptr + 2 )
    else:
        ptr = ptr + 3

def add():
    global ptr

    write_register( ptr + 1, ( read_memory( ptr + 2 ) + read_memory( ptr + 3 ) ) % 32768 )
    ptr = ptr + 4

def mult():
    global ptr

    write_register( ptr + 1, ( read_memory( ptr + 2 ) * read_memory( ptr + 3 ) ) % 32768 )
    ptr = ptr + 4

def mod():
    global ptr

    write_register( ptr + 1, ( read_memory( ptr + 2 ) % read_memory( ptr + 3 ) ) % 32768 )
    ptr = ptr + 4

def _and():
    global ptr

    write_register( ptr + 1, ( read_memory( ptr + 2 ) & read_memory( ptr + 3 ) ) % 32768 )
    ptr = ptr + 4

def _or():
    global ptr

    write_register( ptr + 1, ( read_memory( ptr + 2 ) | read_memory( ptr + 3 ) ) % 32768 )
    ptr = ptr + 4

def _not():
    global ptr

    write_register( ptr + 1, ( ~ read_memory( ptr + 2 ) & 32767 ) % 32768 )
    ptr = ptr + 3

def rmem():
    global memory
    global ptr
    global regs

    # if asked to read from a register, read from the memory address IN that register!
    write_register( ptr + 1 , read_memory( read_memory( ptr + 2 ) ) )

    ptr = ptr + 3

def wmem():
    global memory
    global ptr

    # if asked to write to a register, write to the memory address IN that register!
    memory[ read_memory( ptr + 1 ) ] =  read_memory( ptr + 2 )

    ptr = ptr + 3

def call():
    global ptr
    global stack

    stack.append( ptr + 2 )
    ptr = read_memory( ptr + 1 )


def ret():
    global ptr
    global stack

    if len(stack) > 0:
        ptr = stack.pop()
    else:
        print( "Return attempted with empty stack:  system halting" )
        sys.exit(1)

def out():
    global ptr

    print( chr( read_memory( ptr+1 ) ), end='' )

    ptr = ptr + 2

def _in():
    global input_buffer
    global memory
    global ptr

    if len( input_buffer ) == 0:
        input_buffer = list( raw_input() )
        # make sure we pass the newline!
        input_buffer.append( '\n' )

    write_register( ptr + 1 , ord( input_buffer.pop( 0 ) ) )

    ptr = ptr + 2

def noop():
    global ptr

    ptr = ptr + 1

### my instructions ###

def read_memory( ptr ):
    global memory
    global regs

    if memory[ ptr ] > 32767:
        return regs[ memory[ ptr ] - 32768 ]
    else:
        return memory[ ptr ]

def write_register( ptr, value ):
    global memory
    global regs

    if memory[ ptr ] > 32767:
        regs[ memory[ ptr ] - 32768 ] = value
    else:
        print( "Register write attempted with literal:  system halting" )
        sys.exit(1)

def main():
    checkArgs()

    global memory
    memory = loadBinary()
    print( "Loaded address space of size %d" % len(memory) )

    global ptr
    ptr = 0

    global regs
    regs = [0,0,0,0,0,0,0,0]

    global stack
    stack = []

    global input_buffer
    input_buffer = []

    max_ptr = 0

    execute = {
        0: halt,
        1: set,
        2: push,
        3: pop,
        4: eq,
        5: gt,
        6: jmp,
        7: jt,
        8: jf,
        9: add,
        10: mult,
        11: mod,
        12: _and,
        13: _or,
        14: _not,
        15: rmem,
        16: wmem,
        17: call,
        18: ret,
        19: out,
        20: _in,
        21: noop
    }

    while True:
        if read_memory( ptr ) == 0:
            break
        else:
            if ptr > max_ptr:
                max_ptr = ptr
            execute[ memory[ptr] ]()


    print( "Pointer: %d" % ptr )
    print( "Max Ptr: %d" % max_ptr )
    print( "Memory at %d: %s" % (ptr,memory[ptr:ptr+4]) )
    print( "Registers: %s" % regs )
    print( "Stack: %s" % stack )

if __name__=='__main__':
    main()
