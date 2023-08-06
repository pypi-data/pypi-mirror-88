from numpy.random import choice
from .spells import spells 
from .learn_spells import learn_spells

def duel_voldemort(wand_movement_pattern):
    """
    This function returns the result of a duel with Lord Voldemort, along with the spells used in the duel. 
    Probability of winning depends on the wand movement used by the wizard during the duel.
    
    Arguments:
    wand_movement_pattern - (str) - represents the wand movement used by the wizard during the duel.
    """ 
    probability = 0

    if wand_movement_pattern == 'random':
        probability = 0.2
    else:
        print(' ')
        user_input = input("Enter the magic wand movement pattern you learned earlier: ")
        if user_input.lower() == wand_movement_pattern:
            probability = 0.3
        else:
            probability = 0.2

    obj = learn_spells()
    your_spell = obj.cast_a_spell()
    opponent_spell = obj.cast_a_spell()

    result = choice(a = [0,1], size = 1, p = [(1-probability), probability])
    return (result, your_spell, opponent_spell)
