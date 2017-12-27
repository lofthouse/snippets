#!/usr/bin/env python
import sys
import os

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <input file> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    part = int(sys.argv[2])

    if not (part == 1 or part == 2):
        print "%s is not a valid part" % sys.argv[2]
        sys.exit(1)

    return (input,part)

# Begin actual code

def main():
    input,part = getArgs()

    particles = []

    for line in input:
        particles.append( dict(zip(['p','v','a','active'],map(lambda x: map(int,x),map(lambda x: x.split(','),map(lambda x: x.strip('<').split('>')[0],line.split('=')))[1:]) + [True]) ) )

    pcount = len(particles)

    for tick in range(1000):
        closest = [0,999999999]
        stable = True

        for i in range(pcount):
            if particles[i]['active']:
                particles[i]['v'] = map( sum, zip(particles[i]['v'],particles[i]['a']) )
                particles[i]['p'] = map( sum, zip(particles[i]['p'],particles[i]['v']) )

                dist = sum(map(abs,particles[i]['p']))
                if dist < closest[1]:
                    closest = [i,dist]

                if stable and (
                # The sign of position and velocity need to match
                    not all( p*v >= 0 for p,v in zip(particles[i]['p'],particles[i]['v']) ) or
                # The sign of velocity and acceleration need to match and
                # zero velocity is only allowed if zero acceleration
                    not all( a == 0 or v*a > 0 for v,a in zip(particles[i]['v'],particles[i]['a']) )
                    ):
                    stable = False

        if part == 2:
            to_destroy = []

            for p1 in range(pcount):
                for p2 in range(p1+1,pcount):
                    if particles[p1]['active'] and particles[p2]['active'] and particles[p1]['p'] == particles[p2]['p']:
                        to_destroy = to_destroy + [p1,p2]

            for p in to_destroy:
                particles[p]['active'] = False

        if stable:
            break

    print "%d is closest at %d and the simulation is stable at tick %d" % tuple(closest + [tick])

    if part == 2:
        survivors = len( [x for x in particles if x['active'] ] )
        print "There are %d surviving particles" % survivors

if __name__=='__main__':
    main()
