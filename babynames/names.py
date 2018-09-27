#!/usr/bin/env python3
from collections import defaultdict
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print(" ".join(map(str,args)) )

def getArgs():
    if (len(sys.argv) - 1 ) % 2 != 0 :
        print("Invalid argument")
        print("%s -i <include file> -e <exclude file>" % sys.argv[0])
        sys.exit(1)

    sys.argv.pop(0)

    names_m_good = set()
    names_f_good = set()
    names_m_bad = set()
    names_f_bad = set()
    stats = defaultdict(int)

    while len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            with open(sys.argv[1]) as input_file:
                input = input_file.read().splitlines()
                for line in input:
                    line = line.replace(',', '')
                    _,m_name,m_stat,f_name,f_stat = line.split()

                    stats[ m_name ] = stats[ m_name ] + int( m_stat )
                    stats[ f_name ] = stats[ f_name ] + int( f_stat )

                    if sys.argv[0] == "-i":
                        names_m_good.add( m_name )
                        names_f_good.add( f_name )
                    elif sys.argv[0] == "-e":
                        names_m_bad.add( m_name )
                        names_f_bad.add( f_name )
                    else:
                        print("%s is not a valid file command" % sys.argv[0])
                        sys.exit(1)
        else:
            print("%s is not a file" % sys.argv[1])
            sys.exit(1)

        sys.argv.pop(0)
        sys.argv.pop(0)

    return (names_m_good.difference(names_m_bad), names_f_good.difference(names_f_bad), stats)

# Begin actual code

def main():
    m,f,stats = getArgs()

    print("Good Male Names:")
    print(sorted(m))

    print("Good Female Names:")
    print(sorted(f))



if __name__=='__main__':
    main()
