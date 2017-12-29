#!/usr/bin/env python
import sys
import os
import numpy as np

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <input file> <iterations>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    iterations = int(sys.argv[2])

    if not (iterations > 0):
        print "%s is not a valid iteration count" % sys.argv[2]
        sys.exit(1)

    return (input,iterations)

# Begin actual code
def null( thing ):
    return thing

def printArray(array):
    for row in array:
        for cell in row:
            print cell,
        print

def saveArray(array, i):
    f = open("21_array_%d" % i, 'w')

    for row in array:
        for cell in row:
            f.write(cell)
        f.write('\n')

    f.close()

def printArrayList(arraylist):
    for row in arraylist:
        print "Row Begin:"
        for subarray in row:
            printArray(subarray)

def printBookList(booklist):
    for ain,aout in booklist:
        printArray(ain)
        print " \|/ "
        printArray(aout)
        print

def findMatches( images, book, pieces ):
    outputs = []

    for row in range( pieces ):
        outputs.append( [] )
        for subarray in range( pieces):
            try:
                for match,output in book:
                    if match.shape == images[row][subarray].shape:
                        for func in [ null, np.flipud ]:
                            for k in range(4):
                                if np.array_equal(match, func( np.rot90( images[row][subarray], k ) )):
                                    outputs[row].append( output )
                                    raise StopIteration
            except StopIteration:
                pass

    for row in range( pieces ):
        outputs[row] = np.concatenate( outputs[row], axis = 1 )

    image = np.concatenate( outputs )

    return image

def main():
    input,iterations = getArgs()

    book=[]

    for line in input:
        pin,pout = line.split(' => ')
        ary_in = np.array([ list(x) for x in pin.split('/') ])
        ary_out = np.array([ list(x) for x in pout.split('/') ])

        book.append( [ary_in,ary_out] )

#    printBookList( book )

    image = np.array([['.','#','.'],['.','.','#'],['#','#','#']])
#    printArray( image )

    for i in range(iterations):
        print "Iteration %d Begin" % i
        dim = len(image)

        if dim % 2 == 0:
            pieces = dim / 2
        else:
            pieces = dim / 3

        images = map( lambda x: np.split(x, pieces, axis = 1), np.split( image, pieces ) )
        image = findMatches( images, book, pieces )

        saveArray( image, i )
        print "There are %d cells on" % (image == '#').sum()

        print

if __name__=='__main__':
    main()
