#!/usr/bin/env python3
from collections import defaultdict
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print(" ".join(map(str,args)) )

def stuff(file,list,stats):
    with open(file) as input_file:
        input = input_file.read().splitlines()
        for line in input:
            line = line.replace(',', '')
            _,m_name,m_stat,f_name,f_stat = line.split()

            stats[ m_name ] = stats[ m_name ] + int( m_stat )
            stats[ f_name ] = stats[ f_name ] + int( f_stat )

            list[0].add( m_name )
            list[1].add( f_name )

    return (list, stats)

def getArgs():
    if (len(sys.argv) - 1 ) % 2 != 0 :
        print("Invalid argument")
        print("%s -i <include file> -e <exclude file>" % sys.argv[0])
        sys.exit(1)

    sys.argv.pop(0)

    names_good = [ set(), set() ]
    names_bad = [ set(), set() ]
    stats = defaultdict(int)

    includes = []
    excludes = []

    while len(sys.argv) > 1:
        file = sys.argv.pop()
        mode = sys.argv.pop()

        if os.path.isfile( file ):
            if mode == "-i":
                includes.append( file )
            elif mode == "-e":
                excludes.append( file )
            else:
                print("%s is not a valid file command" % mode)
                sys.exit(1)
        else:
            print("%s is not a file" % file)
            sys.exit(1)

    for file in includes:
        names_good,stats = stuff(file,names_good,stats)

    for file in excludes:
        names_bad,stats = stuff(file,names_bad,stats)

    return (names_good[0].difference(names_bad[0]), names_good[1].difference(names_bad[1]), stats)

# Begin actual code

def main():
    m,f,stats = getArgs()

    print("Good Male Names:")
    for name in sorted(m):
        print(name)

    print("\n=====\n")

    print("Good Female Names:")
    for name in sorted(f):
        print(name)


if __name__=='__main__':
    main()
