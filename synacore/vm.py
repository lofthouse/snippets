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

def halt(memory,ptr):
    return False

def set():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def push():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def pop():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def eq():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def gt():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def jmp():
    global ptr
    ptr = memory[ ptr + 1 ]

def jt():
    global memory
    global ptr

    if not memory[ ptr + 1 ] == 0:
        ptr = memory[ ptr + 2 ]
    else:
        ptr = ptr + 3

def jf():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def add():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def mult():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def mod():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def _and():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def _or():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def _not():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def rmem():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def wmem():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def call():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def ret():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def out():
    global memory
    global ptr

    print( chr(memory[ptr+1]), end='' )

    ptr = ptr + 2

def _in():
    print( "%s is not defined yet" % sys._getframe().f_code.co_name)
    return noop()

def noop():
    global ptr

    ptr = ptr + 1

def main():
    checkArgs()

    global memory
    memory = loadBinary()

    global ptr
    ptr = 0

    global regs
    regs = [0,0,0,0,0,0,0,0]

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
        if memory[ptr] == 0:
            break
        else:
            debug( "Pointer: %d" % ptr )
            debug( "Memory at %d: %s" % (ptr,memory[ptr:ptr+4]) )
            execute[ memory[ptr] ]()

if __name__=='__main__':
    main()
