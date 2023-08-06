from math import floor
from numpy.random import choice

class Hogwarts:
    """
    This class represents the super class of Hogwarts to be inherited by Wizard class.

    This class provides functions and information that will be used by wizard -
    that allows them to convert their currency into wizard currency, 
    and also allows to buy a wand using the currency.

    Attributes
    ----------
    name (str)
    hogwarts_houses_list (list)
    friends_list (dict)
    value_list (dict)
    mascot_list (dict) 
    colors_list (dict) 
    ghost_list (dict)
    relic_list (dict)
    default_quidditch_rating (float)

    Methods
    -------
    gringotts(self, currency) : allows wizard to convert their currency into wizard currency
    get_wand(self) : allows wizard to buy a wand using their currency
    """
    
    hogwarts_houses_list = ['Gryffindor', 'Ravenclaw', 'Hufflepuff', 'Slytherin']
    friends_list = {
        'Gryffindor' : ['Harry Potter', 'Ron Weasley', 'Hermione Granger', 'Ginny Weasley', 'Neville Longbottom'],
        'Ravenclaw' : ['Cho Chang', 'Padma Patil', 'Luna Lovegood', 'Michael Corner'],
        'Hufflepuff' : ['Cedric Diggory', 'Justin Finch-Fletchley', 'Hannah Abbott', 'Zacharias Smith', 'Susan Bones'],
        'Slytherin' : ['Draco Malfoy', 'Gregory Goyle', 'Vincent Crabbe', 'Millicent Bulstrode', 'Marcus Flint']
    } 
    value_list = {
        'Gryffindor' : 'Courage',
        'Ravenclaw' : 'Intelligence',
        'Hufflepuff' : 'Loyalty',
        'Slytherin' : 'Cunning'
    }  
    mascot_list = {
        'Gryffindor' : 'Lion',
        'Ravenclaw' : 'Eagle',
        'Hufflepuff' : 'Badger',
        'Slytherin' : 'Serpent'
    } 
    colors_list = {
        'Gryffindor' : 'Maroon and Gold',
        'Ravenclaw' : 'Blue and Bronze',
        'Hufflepuff' : 'Yellow and Black',
        'Slytherin' : 'Green and Silver'
    }
    ghost_list = {
        'Gryffindor' : 'Nearly Headless Nick',
        'Ravenclaw' : 'The Grey Lady',
        'Hufflepuff' : 'The Fat Friar',
        'Slytherin' : 'The Bloody Baron'
    }  
    relic_list = {
        'Gryffindor' : "Sword of Gryffindor",
        'Ravenclaw' : "Ravenclaw's Diadem",
        'Hufflepuff' : "Hufflepuff's Cup",
        'Slytherin' : "Slytherin's Locket"
    }  
    default_quidditch_rating = {
        'Gryffindor' : 0.9,
        'Ravenclaw' : 0.7,
        'Hufflepuff' : 0.6,
        'Slytherin' : 0.9
    }                            
    
    def __init__(self, name):
        '''
        Extend greeting and instructions to new wizard and initiate starting wizard currency amounts.

        Arguments:
        name -- (str) the name of the wizard
        '''
        self.name = name        
        str = "#" * len(self.name)
        print("####################################" + str)
        print(f"    Welcome to the magic world, {self.name}   ")
        print("####################################" + str)
        print(' ')
        print(f'Go to gringotts bank to convert your Canadian dollars to wizard currencies.')
        print('Example: my.gringotts(1400)')
        print(' ')
        self.House = "no"
        self.Golden_Galleons = 0
        self.Silver_Sickles = 0
        self.Bronze_Knuts = 0
        
    def gringotts(self, currency):
        '''
        Converts canadian dollar number to wizarding currency

        Arguments:
        currency -- (int, float) the amount of canadian currency
        '''
        if isinstance(currency, (int, float)):
            self.Golden_Galleons = floor(currency / 246.50)
            self.Silver_Sickles = floor((currency - self.Golden_Galleons * 246.50) / 14.50)
            self.Bronze_Knuts = floor((currency - self.Golden_Galleons * 246.50 - self.Silver_Sickles * 14.50) / 0.50)
            message = f'Currency exchange completed.\n'  \
                      f'You currently have {self.Golden_Galleons} Golden Galleons, {self.Silver_Sickles} Silver Sickles, and {self.Bronze_Knuts} Bronze Knuts.'
            print(message)
        else:
            print("Please enter a valid number of canadian dollars, for example: gringotts(10000) , gringotts(5010.50)")
        print(' ')
        print("Now it's time to buy yourself a wand to learn and perform magic spells!")
        print('Example: my.get_wand()')
        print(' ')

    def get_wand(self):
        '''
        Selects a wand for the wizard (wood type, core, and length) and returns these values. 
        Updates and states wizarding currency based on cost of the wand. 

        Arguments:
        None
        '''
        wood_type = choice(['Ash', 'Black Walnut', 'Cedar', 'Cherry', 'Elm', 'Hawthorn', 'Poplar', 'Red Oak', 'Sycamore', 'Walnut'])
        core = choice(['Unicorn Hair', 'Dragon Heart String', 'Pheonix Feather'])
        length = choice([9,10,11,12,13,14])
        if self.Golden_Galleons > 0:
            self.Golden_Galleons -= 1
        elif self.Silver_Sickles > 0:
            self.Silver_Sickles -= 1
        elif self.Bronze_Knuts > 0:
            self.Bronze_Knuts -= 1
        print(f'Your updated currency balance is {self.Golden_Galleons} Golden Galleons, {self.Silver_Sickles} Silver Sickles, and {self.Bronze_Knuts} Bronze Knuts.')
        print(' ')
        return (wood_type, core, length)
