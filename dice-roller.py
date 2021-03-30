#!python3
'''
This module contains a function to roll and keep dice
for the 5th edition of the Legends of the Five Rings (L5R) RPG
'''
import random
import pprint
import pyinputplus as pyip

pp = pprint.PrettyPrinter(indent=4)

def roll(ring, skill):
    ringDice = {
        1: [''],
        2: ['Opportunity', 'Strife'],
        3: ['Opportunity'],
        4: ['Success', 'Strife'],
        5: ['Success'],
        6: ['Explosive Success', 'Strife'],
    }

    skillDice = {
        1: [''],
        2: [''],
        3: ['Opportunity'],
        4: ['Opportunity'],
        5: ['Opportunity'],
        6: ['Success', 'Strife'],
        7: ['Success','Strife'],
        8: ['Success'],
        9: ['Success'],
        10: ['Success', 'Opportunity'],
        11: ['Explosive Success', 'Strife'],
        12: ['Explosive Success'],
    }

    rawResult = {}

    for die in range(ring):
        face = random.randint(1, 6)
        rawResult['Ring die ' + str(die + 1)] = ringDice[face]
    
    for die in range(skill):
        face = random.randint(1, 12)
        rawResult['Skill die ' + str(die + 1)] = skillDice[face]
    
    pp.pprint(rawResult)
    

    # Now let's select the dice we want to keep.
    keptDice = {}
    
    for die in range(ring):
        choices = list(rawResult.keys())
        choice = pyip.inputMenu(choices, lettered=True)
        keptDice[choice] = rawResult[choice]
        del rawResult[choice]
    
    # now let's make some dice explode
    # TODO


    pp.pprint(keptDice)