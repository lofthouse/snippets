#! /usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day N')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
parser.add_argument("x", type=int, help="the number x")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

def main():
    lines = readfile()

if __name__ == "__main__":
    main()
