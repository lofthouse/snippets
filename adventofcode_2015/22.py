#!/usr/bin/env python

import sys
import os.path
import json
from pprint import pprint
from ast import literal_eval
from itertools import combinations

DEBUG = False

def usageAndExit():
    print "Usage: 22.py <input data file(s)> [dict of character stat tuples in Hit Point, Armor, Mana order for player, Hit Point, Damage order for boss]"
    sys.exit(1)

def loadData():
    global DEBUG

    data = {}
    data['player']={}
    data['boss']={}
    data['player']['Hit Points'] = 50
    data['player']['Armor'] = 0
    data['player']['Mana'] = 500


    # goal here is to allow input in any order and from as few or as many files as desired
    for arg in sys.argv[1:]:
        if not os.path.isfile(arg):
            if arg.upper() == 'DEBUG':
                DEBUG = True
            else:
                argx = literal_eval(arg)
                if isinstance(argx,dict):
                    for character in argx:
                        if DEBUG:
                            print "Processing " + character + " as " + repr( argx[character] )
                        if character == 'player':
                            data['player']['Hit Points'],data['player']['Armor'],data['player']['Mana'] = argx['player']
                        elif character == 'boss':
                            data['boss']['Hit Points'],data['boss']['Damage'] = argx['boss']
                        else:
                            print "Unknown character " + character
                            print
                            usageAndExit()
                else:
                    print "Invalid argument: " + arg
                    print
                    usageAndExit()
        else:
            with open( arg ) as input_file:
                if DEBUG:
                    print "Processing " + arg
                try:
                    content = json.load(input_file)
                    data['spells'] = content
                except ValueError as err:
                    input_file.seek(0)

                    content = input_file.read().splitlines()
                    for line in content:
                        pieces = line.split()
                        if pieces[0] == 'Hit':
                            data['boss']['Hit Points'] = int( pieces[2] )
                        else:
                            data['boss'][pieces[0][:-1]] = int( pieces[1] )

    response = []

    for requirement in ('player','boss','spells'):
        if data.get(requirement) is None:
            print "Invalid input:  missing definition of %s" % requirement
            sys.exit(1)
        else:
            response.append(data[requirement])

    return tuple(response)


#HERE
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
    player_orig, boss_orig, spells = loadData()
    gamepieces = {'Player: ':player_orig,'Boss: ':boss_orig,'Spells: ':spells}

    if DEBUG:
        for element in gamepieces:
            print element
            pprint( gamepieces[element] )

    # State:
        # player
        # boss
        # spell queue

    # create a costed tree
    # initialize min winning cost with a very very large value
    # load tree with each possible opening spell and the resulting state...
    # While min cost in tree < min winning cost
        # play the next possible moves
            # execute spell queue
            # if a winning state, update min winning cost

    return 0

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
