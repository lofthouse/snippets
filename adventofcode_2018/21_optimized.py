#! /usr/bin/env python3
A=0
B=0
C=0
D=0
E=0

p1=False
seen=set()
iterations=1

while True:
    C = E | 65536
    E = 7586220

    while True:
        A = C & 255
        E = E + A
        E = E & 16777215
        E = E * 65899
        E = E & 16777215

        if C < 256:
            if not p1:
                print( f"Part 1: {E}" )
                p1 = True

            if E in seen:
                print( f"Part 2: {previous} after {iterations} iterations" )
                exit(0)

            seen.add(E)
            previous = E
            iterations += 1
            break
        else:
            C = C // 256
