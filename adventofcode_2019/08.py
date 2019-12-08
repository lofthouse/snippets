#! /usr/bin/env python3
import argparse
from collections import Counter
import textwrap

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day 8')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
parser.add_argument("width", type=int, help="the width of the image")
parser.add_argument("height", type=int, help="the height of the image")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def main():
    lines = readfile()

    layer_stats = []
    num_0_count = args.width * args.height
    num_0_layer = -1

    layers = textwrap.wrap( lines[0], num_0_count )

    # Let counter do all the dirty work for us, and track the lowest 0 count as we go
    for n,layer in enumerate(layers):
        stats = Counter( layer )
        layer_stats.append( stats )
        if stats[ '0' ] < num_0_count:
            num_0_count = stats[ '0' ]
            num_0_layer = n

    print( "The layer with the few 0's is", num_0_layer, "with", num_0_count )
    print( "The 1 count * the 2 count is", layer_stats[ num_0_layer ][ '1' ] * layer_stats[ num_0_layer ][ '2' ] )

    # Create the image as all undecided pixels
    image = [ '_' ] * ( args.width * args.height )

    for layer in layers:
        layer = list( layer )
        for n,pair in enumerate( zip( image, layer ) ):
            # if this pixel is undecided and this layer has a non-transparent value, render it!
            if pair[0] == '_' and pair[1] != '2':
                image[n] = ( ' ' if pair[1] == '0' else '#' )

    print()
    # collapse image list into a string and format it to <width> lines
    print( textwrap.fill( ''.join( image ), args.width ) )

if __name__ == "__main__":
    main()
