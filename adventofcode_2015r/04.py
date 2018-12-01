#! /usr/bin/env python3
import sys
import hashlib

def main():
    if len(sys.argv) != 3 or not sys.argv[2].isdigit():
        print( f"Usage:  {sys.argv[0]} <secret key> <zeroes>" )
        sys.exit(1)

    pad = 0
    start = "a"
    key = sys.argv[1]
    zeroes = int( sys.argv[2] )
    finish = "0" * zeroes

    while start != finish:
        pad += 1
        start = hashlib.md5( (key+str(pad)).encode('utf-8') ).hexdigest()[:zeroes]


    print( f"The number is {pad}" )

if __name__ == "__main__":
    main()
