#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 4 :
        print "Invalid argument"
        print "%s <input file> <dancers> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    dancers = int(sys.argv[2])

    part = int(sys.argv[3])

    if not (part == 1 or part == 2):
        print "%s is not a valid part" % sys.argv[3]
        sys.exit(1)

    return (input[0].split(','),dancers,part)

# Begin actual code

def dance(line,input,dancers):
    for move in input:
        if move[0] == 's':
            shift = int(move[1:])
            line = line[-shift:] + line[0:(dancers - shift)]
        if move[0] == 'x':
            A,B = map(int,move[1:].split('/'))
            swapDancers(line,A,B)
        if move[0] == 'p':
            A,B = map(lambda x: line.index(x),move[1:].split('/'))
            swapDancers(line,A,B)

    return line

def swapDancers(line,A,B):
    tmp = line[B]
    line[B] = line[A]
    line[A] = tmp

def main():
    input,dancers,part = getArgs()

    line = [ chr(x + ord('a')) for x in range(dancers) ]

    line = dance(line,input,dancers)
    print "1: ",''.join(line)

    seen=set()
    seen.add(''.join(line))

    for i in xrange(2,1000000000):
        line = dance(line,input,dancers)
        debug( i,": ",''.join(line) )
        if ''.join(line) in seen:
            break
        else:
            seen.add(''.join(line))

    remaining = 1000000000 % (i-1)
    # We've already done the first of the next cycle
    # We have to start at the 2nd of the final cycle
    start = 1000000000 - remaining + 2
    print "Cycle of %d found, skipping to round %d" % ((i-1),start)

    for i in xrange(start, 1000000001):
        line = dance(line,input,dancers)
        debug( i,": ",''.join(line) )

    print "The final order is %s" % ''.join(line)

if __name__=='__main__':
    main()
