#!/usr/bin/env python

import sys
import os.path
import json
import heapq
from pprint import pprint
from ast import literal_eval
from itertools import combinations

DEBUG = False
part = 1

def usageAndExit():
    print "Usage: 22.py <input data file(s)>\
[dict of input tuples for player, boss, and/or moves:\
'player':(Hit Point, Armor, Mana)\
'boss':(Hit Point, Damage)\
'moves':['M','D','S']\
]"
    sys.exit(1)

def loadData():
    global DEBUG
    global part

    data = {}
    data['player']={}
    data['boss']={}
    data['spells']={}
    data['moves']=[]

    data['player']['Hit Points'] = 50
    data['player']['Armor'] = 0
    data['player']['Mana'] = 500

    data['spells']['M'] = {
        'name':'Magic Missile',
        'cost':53,
        'damage':4
    }
    data['spells']['D'] = {
        'name':'Drain',
        'cost':73,
        'damage':2,
        'heal':2
    }
    data['spells']['S'] = {
        'name':'Shield',
        'cost':113,
        'effect':6,
        'armor':7
    }
    data['spells']['P'] = {
        'name':'Poison',
        'cost':173,
        'effect':6,
        'damage':3
    }
    data['spells']['R'] = {
        'name':'Recharge',
        'cost':229,
        'effect':5,
        'mana':101
    }


    # goal here is to allow input in any order and from as few or as many files as desired
    for arg in sys.argv[1:]:
        if not os.path.isfile(arg):
            if arg.upper() == 'DEBUG':
                DEBUG = True
            if arg.isdigit() and (arg == '1' or arg == '2'):
                part = int(arg)
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
                        elif character == 'moves':
                            data['moves'] = argx['moves']
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
                    # This is not quite working:  all data comes in as unicode
                    # I don't feel like dealing with unicode now...
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
        if len(data[requirement]) == 0:
            print "Invalid input:  missing definition of %s" % requirement
            sys.exit(1)
        else:
            response.append( data[requirement] )

    response.append( data['moves'] )
    return tuple(response)


def stateWorkingCopy(state):
    return {'player_hp':state[0],'player_mana':state[1],'player_armor':0,'boss_hp':state[2],'S':state[3],'P':state[4],'R':state[5]}

def workingCopyToState(wc):
    return ( wc['player_hp'], wc['player_mana'], wc['boss_hp'], wc['S'], wc['P'], wc['R'] )

# will return True if boss was killed so caller can Do The Right Thing
def processTimers(wc):
    timed_spells = ['S','P','R']

    # Execute all timed spells
    for timer in timed_spells:
        if wc[timer] > 0:
            wc[timer] -= 1
            if timer == 'S':
                if DEBUG:
                    print "Shields activated"
                wc['player_armor'] = 7
            if timer == 'P':
                if DEBUG:
                    print "Poison activated"
                wc['boss_hp'] -= 3
                if wc['boss_hp'] <= 0:
                    # you win!  return proof and let caller deal with consequences
                    return True
            if timer == 'R':
                if DEBUG:
                    print "Recharge activated"
                wc['player_mana'] += 101

    return False

# play needs to return either a new state or False (invalid move)
def play(move,state):
    global DEBUG
    global spells
    global player
    global boss

    player_armor = 0
    timed_spells = ['S','P','R']

    wc = stateWorkingCopy(state)
    if DEBUG:
        print "\nPLAYER TURN"
        print wc

    if part == 2:
        wc['player_hp'] -= 1
        if wc['player_hp'] <= 0:
            if DEBUG:
                print "Hard mode die!"
            return workingCopyToState(wc)

    # all timers will decrement momentarily, but if the spell cast
    # is not about to expire, it is invalid
    if move in timed_spells:
        if wc[move] > 1:
            if DEBUG:
                print "%s is already active:  you can't recast it yet" % spells[move]['name']
            return False

    # Let all timed spells do their damage
    if processTimers(wc):
        return workingCopyToState(wc)

    # We're not explicitly handling "can't afford = lose"
    # we're just saying it's an invalid move since all we care about is winning
    if spells[move]['cost'] > wc['player_mana']:
        if DEBUG:
            print "You can't afford to cast %s now" % spells[move]['name']
        return False
    else:
        wc['player_mana'] -= spells[move]['cost']

    if DEBUG:
        print "Casting %s" % spells[move]['name']

    if move == 'M':
        wc['boss_hp'] -= spells[move]['damage']
    elif move == 'D':
        wc['boss_hp'] -= spells[move]['damage']
        wc['player_hp'] += spells[move]['heal']
    elif move == 'S' or move == 'P' or move == 'R':
        wc[move] = spells[move]['effect']
    else:
        print "Invalid move %s" % move
        sys.exit(1)

    if wc['boss_hp'] <= 0:
        # you win!  return proof and let caller deal with consequences
        return workingCopyToState(wc)

    # Execute boss's turn
    if DEBUG:
        print "BOSS TURN"
        print wc

    # Instructions seemed very clear this only happened on PLAYER'S TURN
    # turns out it happens on Boss turn as well.  Overly complicated rules.
    if part == 2:
        wc['player_hp'] -= 1
        if wc['player_hp'] <= 0:
            if DEBUG:
                print "Hard mode die!"
            return workingCopyToState(wc)

    if processTimers(wc):
        return workingCopyToState(wc)

    wc['player_hp'] -= max(0, (boss['Damage'] - wc['player_armor']) )

    return workingCopyToState(wc)


def main():
    global DEBUG
    global spells
    global player
    global boss

    lowest_cost = 99999
    highest_cost = 0
    player, boss, spells, moves = loadData()
    gamepieces = {'Player: ':player,'Boss: ':boss,'Spells: ':spells, 'Moves: ':moves}

    if DEBUG:
        for element in gamepieces:
            print element
            pprint( gamepieces[element] )

    # State Tuple:
    #(hp,mana, <- player
    # hp, <- boss
    # S,P,R <- Spell timers
    #)

    state = ( player['Hit Points'], player['Mana'], boss['Hit Points'], 0,0,0 )

    # If moves were provided (for debugging), process them
    if len(moves) > 0:
        for move in moves:
            state = play(move,state)
            if state[0] <= 0:
                print "Player loses"
                break
            if state[2] <= 0:
                print "Boss loses"
                break
    # Otherwise, solve the part
    else:
        heapq.heappush( moves, (0, '', state) )
        min_cost = 999999
        min_path = ''
        visited = set()
        visited.add( state )

        print moves

        while len(moves) > 0:
            cost,path,state = heapq.heappop( moves )
            for spell in spells:
                new_cost = cost + spells[spell]['cost']
                new_path = path + spell

                if DEBUG:
                    print "Trying to cast %s from %s" % (spell,path)

                new_state = play( spell, state )
                if new_state:
                    if new_state[0] <= 0:
                        if DEBUG:
                            print "Player loses casting %s from %s" % (spell,path)
                    elif new_state[2] <= 0:
                        if DEBUG:
                            print "Boss loses casting %s from %s" % (spell,path)
                        if new_cost < min_cost:
                            min_cost = new_cost
                            min_path = new_path
                    else:
                        if new_state not in visited and new_cost < min_cost:
                            heapq.heappush( moves, (new_cost, new_path, new_state) )

        print "The minimum cost to win was %d, achieved by casting %s" % (min_cost,min_path)


    # create a costed tree
    # initialize min winning cost with a very very large value
    # load tree with each possible opening spell and the resulting state...
    # While min cost in tree < min winning cost
        # play the next possible moves
            # execute spell queue
            # if a winning state, update min winning cost

#HERE

    return 0


if __name__=="__main__":
    main()

sys.exit(0)
