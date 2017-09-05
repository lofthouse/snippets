#!/usr/bin/env python

import sys
import os.path
from pprint import pprint
from ast import literal_eval
from itertools import combinations

DEBUG = False

def loadData():
    global DEBUG

    data = {}
    data['player']={}
    data['player']['Hit Points'] = 100
    data['player']['Armor'] = 0
    data['player']['Damage'] = 0


    # goal here is to allow input in any order and from as few or as many files as desired
    for arg in sys.argv[1:]:
        if not os.path.isfile(arg):
            if arg.upper() == 'DEBUG':
                DEBUG = True
                continue
            else:
                argx = literal_eval(arg)
                if isinstance(argx,tuple) and len(argx) == 3:
                    data['player']['Hit Points'],data['player']['Damage'],data['player']['Armor'] = literal_eval(arg)
                    continue
                else:
                    print "Invalid argument: " + arg
                    print
                    print "Usage: 21.py <input data file(s)> [player stat tuple in Hit Point, Damage, Armor order]"
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
                            # Annoying ":" at end of label go bye-bye
                            data[block][pieces[0][:-1]] = int( pieces[1] )
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

    for requirement in ('player','boss','Weapons','Armor','Rings'):
        if data.get(requirement) is None:
            print "Invalid input:  missing definition of %s" % requirement
            sys.exit(1)
        else:
            response.append(data[requirement])

#    return ( data['boss'], data['Weapons'], data['Armor'], data['Rings'] )
    return tuple(response)

def arm(player,bundle):
    global DEBUG

    cost = 0
    powers = ('Armor','Damage')
    package = ''

    for goody in bundle:
        cost += bundle[goody]['Cost']
        package += goody + " "

        for p in powers:
            player[p] += bundle[goody][p]

    return (cost,package)

def attack(attacker, defender):
    global DEBUG

    damage = max(1,attacker['Damage'] - defender['Armor'])

    defender['Hit Points'] -= damage

def fight(player, boss):
    attacker = player
    defender = boss

    while player['Hit Points'] > 0 and boss ['Hit Points'] > 0:
        attack(attacker, defender)
        temp = defender
        defender = attacker
        attacker = temp

    return player['Hit Points'] > 0

def main():
    global DEBUG

    lowest_cost = 99999
    highest_cost = 0
    player_orig, boss_orig, weapons, armory, ringery = loadData()
    gamepieces = {'Player: ':player_orig,'Boss: ':boss_orig,'Weapons: ':weapons,'Armor: ':armory,'Rings: ':ringery}

    if DEBUG:
        for element in gamepieces:
            print element
            pprint( gamepieces[element] )

    for weapon in weapons:
        for arms in (0,1):
            for armor in combinations(armory,arms):
                for rings in (0,1,2):
                    for ringset in combinations(ringery,rings):
                        player = player_orig.copy()
                        boss = boss_orig.copy()
                        bundle = {}

                        bundle[weapon]=weapons[weapon]
                        for a in armor:
                            bundle[a]=armory[a]
                        for r in ringset:
                            bundle[r]=ringery[r]

                        cost,description = arm(player,bundle)
                        if fight(player,boss):
                            if cost < lowest_cost:
                                lowest_cost = cost
                                if DEBUG:
                                    print "%d will buy you %s and victory" % (lowest_cost, description)
                        else:
                            if cost > highest_cost:
                                highest_cost = cost
                                if DEBUG:
                                    print "%d will buy you %s and defeat" % (highest_cost, description)

    print "The lowest cost for victory is %d" % lowest_cost
    print "The highest cost for defeat is %d" % highest_cost

if __name__=="__main__":
    main()

sys.exit(0)
