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
        7: ['Success', 'Strife'],
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
    print('')
    print(f"You can keep up to {ring} dice from this roll.\n")
    

    # Now let's select the dice we want to keep.
    keptDice = {}
    
    for die in range(ring):
        choices = list(rawResult.keys())
        choice = pyip.inputMenu(choices, lettered=True)
        keptDice[choice] = rawResult[choice]
        del rawResult[choice]
        pp.pprint(rawResult)
    
    print("You kept:\n")
    pp.pprint(keptDice)
    # now let's make some dice explode
    # we will iterate over the keptDice, and if 'Explosive' is in them, roll a new dice of the same type, and add them to a separate dict.
    # we will ask for each of those if the player wants to keep them or not.
    # TODO if there are explosive successes in this explodedDice dict, we need to explose them as well.
    

    # this horror will create a giant string of all the kept dice, just to check if there are Explosive Successes left to explode.
    keptDiceFaces = ",".join(str(x) for x in keptDice.values())
    
    while 'Explosive Success' in keptDiceFaces:
        explodedDice = {}
        print('\n\nYou have some dice to explode!\n')
        for die in keptDice.keys():
            if 'Explosive Success' in keptDice[die][0] and 'Ring' in die:
                explodedDice['extra die from ' + die] = ringDice[random.randint(1, 6)]
                print('You rolled', explodedDice['extra die from ' + die])
                keptDice[die][0] = keptDice[die][0].replace('Explosive Success', 'Success')
            elif 'Explosive Success' in ",".join(keptDice[die]) and 'Skill' in die:
                explodedDice['extra die from ' + die] = skillDice[random.randint(1, 12)]
                print('You rolled', explodedDice['extra die from ' + die])
                # Remove 'Explosive ' from the kept dice that exploded
                keptDice[die][0] = keptDice[die][0].replace('Explosive Success', 'Success')
            
        
        print('You got these new dice:\n')
        pp.pprint(explodedDice)

        #let's select the ones we want to keep.
        for die in explodedDice.keys():
            choice = pyip.inputYesNo(prompt=f'Do you want to keep {explodedDice[die]}?\n')
            if choice == 'yes':
                keptDice[die] = explodedDice[die]
        
        # recreate the string of kept dice for the while loop to check
        keptDiceFaces = ",".join(str(x) for x in keptDice.values())
    

    print("Final result:\n")
    pp.pprint(keptDice)
    
    #TODO : compute the total successes, opportunity and strife gainde from roll