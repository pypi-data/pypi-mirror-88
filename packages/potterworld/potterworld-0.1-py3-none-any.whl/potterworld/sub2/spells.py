class spells:
    """
    This Class has a dictionary of spells that can be learned.
    Also contains a method called get_all_spells that returns this dictionary.
    """  
    spells_dict = {
    'Expelliarmus' : 
    'disarms your enemy by knocking their want out of their hand.'
    ,
    'Lumos' :
    'Use your wand as a light.'
    ,
    'Nox' :
    'Put out the light on your wand.'
    ,
    'Protego' :
    'Shield charm used whild duelling.'    
    ,
    'Accio' :
    'Summons whatever you say after the spell to fly into your hand.'
    ,
    'Stupefy' :
    'Stun your opponent.'
    ,
    'Wingardium Leviosa' :
    'Make things levitate'
    ,
    'Petrificus Totalus' :
    'Temporarily bind and paralyze your opponent.'
    ,
    'Expecto Patronum' :
    'Summons your patronus to repel evil dementors that want to suck out your soul. Should assign an animal to the patronus (eg. wolf, stag, bear, etc.).'
    ,
    'Reparo' :
    'Repair things that are broken.'
    }

    counter = 0

    def __init__(self):
        self.counter += 1

    def __str__(self):
        message = f'This is the super Class for magical spells used at Hogwarts school.'
        return message

    def get_all_spells(self):
        """
        This function returns all the spells present in the spells dictionary of spells class.
        
        Arguments:
        no arguments, only the self object.
        """        
        return self.spells_dict
