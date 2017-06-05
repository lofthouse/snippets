#!/usr/bin/env python

import sys
import os.path

def loadData():
    data = {}

    # goal here is to allow input in any order and from as few or as many files as desired
    for arg in sys.argv[1:]:
        if not os.path.isfile(arg):
            print "Invalid argument:  need list of input files"
            sys.exit(1)

        # inBlock = header found, processing block of values
        inBlock = False
        with open( arg ) as input_file:
            content = input_file.read().splitlines()

            for line in content:
                pieces = line.split()
                # If we're not already in a block find the block labels
                if not inBlock:
                    inBlock = True
                    # The boss input is different: no header, data immediately
                    if pieces[0] == 'Hit' :
                        block = 'boss'
                        data[block] = {}
                        data[block]['Hit Points'] = int( pieces[2] )
                    else:
                        block = pieces[0][:-1]
                        labels = pieces[1:]
                        data[block] = {}
                else:
                    # End of Block
                    if len( pieces ) == 0:
                        inBlock = False
                        continue
                    else:
                        # Boss data is one per line
                        if block == 'boss':
                            data[block][pieces[0]] = int( pieces[1] )
                        # market data is columns matching column labels grabbed above
                        else:
                            if block == 'Rings':
                                item = ' '.join(pieces[0:2])
                                # Rings have extra 'column':  match up for rest by deleting 'extra'
                                del pieces[0]
                            else:
                                item = pieces[0]
                            data[block][item] = {}
                            for label,value in zip( labels, pieces[1:] ):
                                data[block][item][label] = int(value)

    response = []

    for requirement in ('boss','Weapons','Armor','Rings'):
        if data.get(requirement) is None:
            print "Invalid input:  missing definition of %s" % requirement
            sys.exit(1)
        else:
            response.append(data[requirement])

#    return ( data['boss'], data['Weapons'], data['Armor'], data['Rings'] )
    return tuple(response)

def main():
    boss, weapons, armory, rings = loadData()

    print "Boss: ",boss
    print "Weapons: ",weapons
    print "Armory: ",armory
    print "Rings: ",rings


if __name__=="__main__":
    main()

sys.exit(0)
