#!python3
'''
This module contains a function to roll and keep dice
for the 5th edition of the Legends of the Five Rings (L5R) RPG.
'''
import random
import pprint
import pyinputplus as pyip

pp = pprint.PrettyPrinter(indent=4)


def roll(ring, skill):
    '''takes in a ring value and a skill value, returns a tuple of successes,
    opportunities and strife gained.'''
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
        12: ['Explosive Success', ''],
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
        choice = pyip.inputMenu(choices + ['No more dice.'], lettered=True)
        if choice == 'No more dice.':
            break
        else:
            keptDice[choice] = rawResult[choice]
            del rawResult[choice]
            pp.pprint(rawResult)

    print("You kept:\n")
    pp.pprint(keptDice)
    # now let's make some dice explode
    # This needs to be recursive.
    # we will ask for each of those if the player wants to keep them or not.

    keptDiceToExplode = {key: value for key, value in keptDice.items() if 'Explosive' in value[0]}
    keptDiceNotToExplode = {key: value for (key, value) in keptDice.items() if 'Explosive' not in value[0]}
    explodedDice = {}

    # recursive explosion
    hasExplosionHappened = False
    while len(keptDiceToExplode):
        hasExplosionHappened = True
        print('\n\nYou have some dice to explode!\n')
        # we'll populate our dict of exploded dice
        for k in keptDiceToExplode.keys():
            if 'Ring' in k:
                explodedDice['Extra die from ' + k] = ringDice[random.randint(1, 6)]
                print('You rolled', explodedDice['Extra die from ' + k])
            elif 'Skill' in k:
                explodedDice['Extra die from ' + k] = skillDice[random.randint(1, 12)]
                print('You rolled', explodedDice['Extra die from ' + k])

        # Now let's keep some exploded dice
        keptExplodedDice = {}
        for die in explodedDice.keys():
            choice = pyip.inputYesNo(prompt=f'Do you want to keep {explodedDice[die]}?\n')
            if choice == 'yes':
                keptExplodedDice[die] = explodedDice[die]

        # now generate a new keptDiceThatHaveExploded dic from the values of keptDiceToExplode
        keptDiceThatHaveExploded = {}
        for k in keptDiceToExplode.keys():
            keptDiceThatHaveExploded[k] = [keptDiceToExplode[k][0].replace('Explosive ', ''), keptDiceToExplode[k][1]]

        # now let's reunite our kept dice
        keptDice = {}
        keptDice.update(keptDiceNotToExplode)
        keptDice.update(keptDiceThatHaveExploded)
        keptDice.update(keptExplodedDice)

        # let's regenerate our 3 temp dicts from above to check if we have new dice to explode
        keptDiceToExplode = {key: value for key, value in keptDice.items() if 'Explosive' in value[0]}
        keptDiceNotToExplode = {key: value for (key, value) in keptDice.items() if 'Explosive' not in value[0]}
        explodedDice = {}

    if hasExplosionHappened:
        print('\nAfter all these explosions, you kept:\n')
        pp.pprint(keptDice)

    print("\nFinal result:\n")
    finalList = []
    for value in keptDice.values():
        finalList += value

    # Compute the total successes, opportunity and strife gained from roll
    successes = finalList.count('Success')
    opportunities = finalList.count('Opportunity')
    strife = finalList.count('Strife')

    print(f'You gained {successes} successes, {opportunities} opportunities, and {strife} strife.')
    return (successes, opportunities, strife)
