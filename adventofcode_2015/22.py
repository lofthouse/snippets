#!/usr/bin/env python

import sys
import os.path
import json
import heapq
from ast import literal_eval

DEBUG = False
part = 1
timed_spells = ['S','P','R']

def usageAndExit():
    print "Usage: 22.py <input data file(s)>\
[dict of input tuples for player, boss, and/or moves:\
'player':(Hit Point, Armor, Mana)\
'boss':(Hit Point, Damage)\
'moves':['M','D','S']\
]"
    sys.exit(1)

# From https://stackoverflow.com/a/13105359/3300042
# needed to support loading the spells from a JSON
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def loadData():
    global DEBUG
    global part

    data = {}
    data['player']={}
    data['boss']={}
    data['moves']=[]
    data['spells']={}

    # defaults
    data['player']['Hit Points'] = 50
    data['player']['Armor'] = 0
    data['player']['Mana'] = 500

    # goal here is to allow input in any order and from as few or as many files as desired
    for arg in sys.argv[1:]:
        if not os.path.isfile(arg):
            if arg.upper() == 'DEBUG':
                DEBUG = True
            elif arg.isdigit() and (arg == '1' or arg == '2'):
                part = int(arg)
            else:
                argx = literal_eval(arg)
                if isinstance(argx,dict):
                    for character in argx:
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
                try:
                    # json.load creates a list of unicode-content dicts
                    # we need a dict of string-content:  make go
                    content = { x['key']:x for x in byteify( json.load(input_file) ) }
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
            print "Incomplete input:  missing definition of %s" % requirement
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
    global timed_spells

    # Execute all timed spells
    for timer in timed_spells:
        if wc[timer] > 0:
            wc[timer] -= 1
            if timer == 'S':
                wc['player_armor'] = spells['S']['armor']
            if timer == 'P':
                wc['boss_hp'] -= spells['P']['damage']
                if wc['boss_hp'] <= 0:
                    # You Win!
                    return True
            if timer == 'R':
                wc['player_mana'] += spells['R']['mana']

    return False

# play needs to return either a new state or False (invalid move)
def play(move,state):
    global DEBUG
    global spells
    global player
    global boss
    global timed_spells

    player_armor = 0

    wc = stateWorkingCopy(state)
    if DEBUG:
        print "\nPLAYER TURN"
        print wc

    if part == 2:
        wc['player_hp'] -= 1
        if wc['player_hp'] <= 0:
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

        while len(moves) > 0:
            cost,path,state = heapq.heappop( moves )

            for spell in spells:
                new_cost = cost + spells[spell]['cost']
                new_path = path + spell

                new_state = play( spell, state )
                if new_state:
                    if new_state[0] <= 0:
                        # Player lost:  nothing more to do with this
                        pass
                    elif new_state[2] <= 0:
                        # Boss lost:  if this is a winning strategy, update mins
                        if new_cost < min_cost:
                            min_cost = new_cost
                            min_path = new_path
                    else:
                        # otherwise, schedule this result for more study unless
                        # we've already been here or its already too expensive
                        if new_state not in visited and new_cost < min_cost:
                            heapq.heappush( moves, (new_cost, new_path, new_state) )

        print "The minimum cost to win was %d, achieved by casting %s" % (min_cost,min_path)

if __name__=="__main__":
    main()

sys.exit(0)
