from .spells import spells
from numpy.random import choice

class learn_spells(spells):
    """
    This class has two major functions.

    1. get_wand_movement_pattern : 
    This function gets the input wand movements from the wizard and returns the wand movement pattern (as a string). 
    If no meaningful input is received string 'random' is returned.

    2. cast_a_spell : 
    This function returns a random spell form the list of available spells. 
    This random spell will be used when the wizard is fighting Lord Voldemort.
    """ 
    def __init__(self):
        spells.__init__(self)
        self.spells_dict = spells.spells_dict

    def get_wand_movement_pattern(self):
        """
        This function gets the input wand movements from user and returns the wand movement pattern (as a string). 
        If no meaningful input is received string 'random' is returned.
        
        Arguments:
        None
        """        
        print(' ')
        print('You can learn a special spell that helps you when fighting Lord Voldemort.')
        print('Wand movements are >>  u : up , d : down , l : left, r : right')
        print('For example, lrd means left-right-down  &  udr means up-down-right')
        print('If you prefer to not learn a special spell, enter x at any time to quit learning. A random spell will be used when you fight.')
        print(' ')
        movement = 'random'
        valid_set = ('l','r','u','d')
        exit_code = False
        while True:
            user_input = input("Enter your favorite wand movement pattern. (input x if you do not want to learn a special spell): ")  
            if user_input.lower() == 'x':
                movement = 'random'
                break
            for char in user_input:
                if char.lower() in valid_set:
                    movement = user_input
                    exit_code = True
                else:
                    print(' ')
                    print('Enter valid wand movement: only (l r u d) characters are allowed.')
                    print('For example, lrd means left-right-down  &  udr means up-down-right')
                    print('Enter x at any time to quit learning. A random spell will be used when you fight.')
                    print(' ')
                    exit_code = False
                    break
            if exit_code:
                break
        return movement

    def cast_a_spell(self):
        """
        This function returns a random spell form the list of available spells. This random spell will be used when fighting Lord Voldemort.

        Arguments:
        None
        """        
        return choice(list(self.spells_dict.keys()))
