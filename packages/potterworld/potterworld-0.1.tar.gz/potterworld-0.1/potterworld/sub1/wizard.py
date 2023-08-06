from .hogwarts import Hogwarts
from potterworld.sub2.learn_spells import learn_spells
from potterworld.sub2.quidditch import quidditch
from potterworld.sub2.duel import duel_voldemort 
from .sorting_hat_song import print_song
import random

class Wizard(Hogwarts):     
    """
    This Wizard class initiates the wizard class object and assign class attributes. Uses Hogwarts superclass attributes.
    This class provides functions and information that will be used by wizard to perform different tasks.

    Attributes
    ----------
    name (str)
    wand_movement_pattern (str)
    house_cup_points (int)
    health_points_for_duel (int)
    house_quidditch_rating (float)
    wand_wood_type (str)
    wand_core (str)
    wand_length (int)
    wand_movement_pattern (str)  

    Methods
    -------
    gringotts : Converts canadian dollar number to wizarding currency
    get_wand : Uses the superclass to assign a wand to the wizard and print the wand details
    sorting_hat : Sorts the wizard into a Hogwarts house (Gryffindor, Hufflepuff, Ravenclaw, Slytherin)
    learn_spells : Allows wizard to learn several spells, and also allows them to create their own special spell.
    night_crawl : Takes the wizard through a narrative simulating a late night exploration of hogwarts castle.
    play_quidditch : Different houses at Hogwarts compete with each other by playing Quidditch using this function. 
    house_cup_winner : Outputs house cup points score and the winner of the house cup. 
    fight_voldemort : The wizard fights Lord Voldemort to death in this duel.
    display : Displays the current class object attributes and gives the user instructions for the next step.
    """
    
    def __init__(self, name):
        '''
        Initiate the wizard class object and assign class attributes. Uses superclass attributes.

        Arguments:
        name -- (str) the name of the wizard
        '''
        Hogwarts.__init__(self, name)
        self.health_points_for_duel = 0
        self.best_friend = "yourself for now, call sorting_hat() to get assigned to a house and make friends"
        self.house_value = "not assigned yet"
        self.house_mascot = "not assigned yet"
        self.house_colors = "not assigned yet"
        self.house_ghost = "not assigned yet"
        self.house_founders_relic = "not assigned yet"
        self.spells_dict = dict()
        self.house_cup_points = 0
        self.house_quidditch_rating = 0
        self.learn_spells_flag = 0
        self.wand_wood_type = None
        self.wand_core = None
        self.wand_length = None
        self.wand_movement_pattern = None

    def __str__(self):
        '''
        Prints output of when str() is called on the class object. 

        Arguments:
        None
        '''
        message = f'Welcome to the magic world, {self.name}.\nRun my.display() for further current status.\n'
        print(message)

    def gringotts(self, currency):
        '''
        Converts canadian dollar number to wizarding currency

        Arguments:
        currency -- (int, float) the amount of canadian currency
        '''
        Hogwarts.gringotts(self, currency)

    def get_wand(self):
        '''
        Uses the superclass to assign a wand to the wizard and print the wand details

        Arguments:
        None
        '''
        if self.wand_wood_type == None:
            (self.wand_wood_type, self.wand_core, self.wand_length) = Hogwarts.get_wand(self)
            message = f'You now have a magical wand!\n'  \
                    f"It's wood type is {self.wand_wood_type}, core is made of {self.wand_core}, and it's length is {self.wand_length} inches."
            print(message)
            print(' ')
            print("Now it's time to get yourself into one of the four prestigious Houses at Hogwarts using 'sorting hat'")
            print('Example: my.sorting_hat()')
            print(' ')
        else:
            print(f"You already have a wand. It's wood type is {self.wand_wood_type}, core is made of {self.wand_core}, and it's length is {self.wand_length} inches.")
            print("Now it's time to get yourself into one of the four prestigious Houses at Hogwarts using 'sorting hat'")
            print('Example: my.sorting_hat()')
            print(' ')

    def sorting_hat(self):
        '''
        Sorts the wizard into a Hogwarts house (Gryffindor, Hufflepuff, Ravenclaw, Slytherin)

        Arguments:
        None
        '''
        if self.House == 'no':
            
            print('you will now be sorted into a hogwarts house. The sorting hat will now sing its song!')
            print('.........')  
            print('......')
            print('...')        
            print_song()
            print('...')
            print('......')
            print('.........')
            print(' ')
            print('Do you wish to choose the House yourself (or) are you okay with random house assignment ?\n')
            user_input = input("Enter y to choose your house, or enter any other character if not interested : ")
            if user_input.lower() == 'y':
                print(' ')
                house_input = input(f'Enter one of these characters ( g r h s ) which represent {Hogwarts.hogwarts_houses_list} : ')
                if house_input.lower() == 'g':
                    self.House = Hogwarts.hogwarts_houses_list[0]
                    self.best_friend = random.choice(Hogwarts.friends_list[self.House])
                elif house_input.lower() == 'r':
                    self.House = Hogwarts.hogwarts_houses_list[1]
                    self.best_friend = random.choice(Hogwarts.friends_list[self.House])
                elif house_input.lower() == 'h':
                    self.House = Hogwarts.hogwarts_houses_list[2]
                    self.best_friend = random.choice(Hogwarts.friends_list[self.House])
                elif house_input.lower() == 's':
                    self.House = Hogwarts.hogwarts_houses_list[3]
                    self.best_friend = random.choice(Hogwarts.friends_list[self.House])
                else:
                    print(f"\nYour input '{house_input}' did not match the given options ( g r h s ), you will now be randomly assigned to a House.\n")
                    self.House = random.choice(Hogwarts.hogwarts_houses_list)
                    self.best_friend = random.choice(Hogwarts.friends_list[self.House])
                print(' ')
            else:
                print(f'\nYou will now be randomly assigned to a House.\n')
                self.House = random.choice(Hogwarts.hogwarts_houses_list)
                self.best_friend = random.choice(Hogwarts.friends_list[self.House])
            self.house_value = Hogwarts.value_list[self.House]
            self.house_mascot = Hogwarts.mascot_list[self.House]
            self.house_colors = Hogwarts.colors_list[self.House]
            self.house_ghost = Hogwarts.ghost_list[self.House]
            self.house_founders_relic = Hogwarts.relic_list[self.House]
            self.house_cup_points = 50
            self.health_points_for_duel = 100
            self.house_quidditch_rating = Hogwarts.default_quidditch_rating[self.House]          
            self.display()            
        else:
            print(f'You are already assigned to {self.House} house, and your best friend is {self.best_friend}.')

    def learn_spells(self):
        """
        This function first displays all the spells learned by the wizard that they can use with their magic wand.

        If the wizard is interested in making their own wand movement for a special spell, 
        this funciton creates that wand movement pattern based on inputs from the wizard.
        This special spell will help the wizard when they fight Lord Voldemort.
        
        Arguments:
        None
        """         
        self.learn_spells_flag = 1
        obj = learn_spells()
        self.spells_dict = obj.get_all_spells()
        print('Great! These are the spells you learned.\n')
        for key, value in self.spells_dict.items():
            print(f'{key} : {value}')
        self.wand_movement_pattern = obj.get_wand_movement_pattern()
        if self.wand_movement_pattern == 'random':
            print('\nYou did not learn any special spell with magic wand movement. A random spell will be used when you fight.')
        else:
            print(f'\nGreat! The special spell you learned is {self.wand_movement_pattern}')
            print('Remember to use this when you fight Lord Voldemort')
        print("\nNow it's time for some fun!\n")
        print('Go for a night crawl (or) Play Quidditch (or) fight Lord Voldemort')
        print('Examples:')  
        print('my.night_crawl()')
        print('my.play_quidditch()')
        print('my.fight_voldemort()')
        print(' ') 
        print("You can call the 'my.display()' method at any time to see your current attribute information.")   

    def night_crawl(self):
        '''
        Takes the wizard through a narrative simulating a late night exploration of hogwarts castle. 
        The user makes a few decisions that affect the course of the exploration. 
        End result is a gain or loss of house points.

        Arguments:
        None
        '''       
        print('''You have decided to sneak out of your dormitory and explore the castle after hours. 
Throughout this adventure, you will have to make some decisions. Hopefully you don't get caught by any professors.\n
Your first decision: Would you like to explore the "Great Hall" or the "Astronomy Tower"?\n''')
        while True:
            location = input('For "Great Hall" enter "g", For "Astronomy Tower" enter "a":')
            if location == 'a':
                dest = 'Astronomy Tower'
                print('\nOff to the Astronomy Tower!\n')
                break
            elif location == 'g':
                dest = 'Great Hall'
                print('\nOff to the Great Hall!\n')
                break
            else:
                print('please enter "g" or "a"')
                continue

        input("Press 'Enter' to continue")

        print(f'''\nOn your way to the {dest}. You hear in the distance the janitor, August Filch, calling for his cat, Mrs. Norris.
You continue walking and come accross a scroll on the floor.\n''')
        while True:
            map = input('If you would like to pick up the scroll, input "y". If you would like to leave it, input "n":')
            if map == 'y':
                print('''\nYou picked up the Marauder's Map. It helps you to see where other people are located in the castle. 
What a great find!\n''')
                break
            elif map == "n":
                print('''\nYou decided not to pick up the Maurauder's Map. It helps the owner to see where other people in the castle are located.
Hopefully you will not regret that decision later... You continue onward.\n''')
                break
            else:
                print('please enter "y" or "n"')
        input("Press 'Enter' to continue")

        print(f'''You have arrived at the {dest}. In the northeast corner of the {dest}, you hear a 'meow' noise coming from the cabinets.
You decide to investigate.''')
        input("Press 'Enter' to continue")

        print('\nThere are 5 cabinets labelled 1, 2, 3, 4, 5.\n')
        cat_loc =  random.randint(1,5)
        while True:
            try:
                cab = int(input('Which cabinet would you like to unlock? Input a single integer 1, 2, 3, 4, or 5:'))
                if cab == cat_loc:
                    print('\nCongratulations! You found Mrs. Norris. Now you should find Mr. Filch to give him the good news.')
                    break
                else:
                    print('\nNothing in here. Try another cabinet.\n')
                    continue
            except ValueError:
                print('\nYou must enter a valid integer. Please try again.\n')
                continue
        
        print(f'''As you search the castle for Mr. Filch, you hear footsteps coming from the other end of the corridor.
If only you had a way of finding out who it is...''')

        input("Press 'Enter' to continue")

        if map == 'y':
            print('''\nYou remembered that you have the Marauder's Map. 
You pull it out and see that the person approaching you is Professor McGonagall.
You hide behind a suit of armour until she is out of sight.\n''')
            input("Press 'Enter' to continue")
            print('You then use the map and locate Mr. Filch. He is in the potions classroom. You head over there and return his cat to him.\n')
            input("Press 'Enter' to continue")
            print(f'''When you hand him the cat, he happily says,
'Thank you {self.name}, I'm so glad you found Mrs. Norris. I'm awarding 20 house points to your house. What is your house again?'\n 
You respond 'It's {self.House} Sir'.
Filch then says, 'Well then, I'm awarding 25 house points to {self.House}. Now run along to bed'\n''')
            self.house_cup_points = self.house_cup_points + 25
            input("Press 'Enter' to continue")
            print(f'''You make it back to your dormitory with a smile on your face.
You can't wait for the morning so you can tell {self.best_friend} and the rest of the house the good news.''')

        if map == 'n':
            print('''\nIf only you had the Marauder's Map. You would then be able to tell who it is.
You decide to jump behind a suit of armour to hide.\n''')
            input("Press 'Enter' to continue")
            print(f'''As the footsteps draw closer, you peek your head out to see who it is. 
To your dismay, Professor McGonagall sees your head and shouts,
"{self.name}! What are you doing out of bed. I'm removing 25 house points from {self.House} and assigning you detention for one week.
Now get off to bed. I hope you have learned your lesson."\n''')
            self.house_cup_points = self.house_cup_points - 25
            input("Press 'Enter' to continue")
            print(f'''You make it back to your dormitory with a glum look on your face.
You are dreading the morning when you will have to tell {self.best_friend} and the rest of the house the bad news.''')

         
    def play_quidditch(self):
        """
        Different houses at Hogwarts compete with each other by playing Quidditch using this function. 

        In the first game, winner is selected based on some randomness and also based on house rating of the wizard. 
        And in the second game, this function gets inputs from the wizard for catching a snitch. 
        House points are awarded or deducted from the house in each game.  
        
        Arguments:
        None
        """         
        self.house_cup_points = quidditch(self.house_quidditch_rating, self.house_cup_points, self.House)
        print(' ')
        print('Go for a night crawl (or) Play Quidditch again (or) fight Lord Voldemort')
        print('Examples:')  
        print('my.night_crawl()')
        print('my.play_quidditch()')
        print('my.fight_voldemort()')
        print('\nIf you would like to find out who won the house cup at the end of the school year, call the method my.house_cup_winner()')
        print(' ') 

    def house_cup_winner(self):
        '''
        Outputs house cup points score and the winner of the house cup. 

        Arguments:
        None
        '''
        print(f'{self.House} house now has a total of {self.house_cup_points} house cup points.')
        if self.house_cup_points > 100:
            print(f'\nCongratulations! {self.House} won the house cup!')
        else:
            temp_dict = Hogwarts.hogwarts_houses_list 
            winner_house = random.choice(temp.remove(self.House)) 
            print('\nYou did not win the house cup. This years winner is {winner_house}.')  
   

    def fight_voldemort(self):
        """
        The wizard fights Lord Voldemort to death in this duel.

        In alternating order, user casts a spell, then voldemort casts a spell.
        Spells used by the wizard and Lord Voldemort are displayed, and they lose some energy each time a spell is cast.
        Wizard can improve their chances of winning by using the wand movement that they learned earlier. 
        
        Arguments:
        None
        """          
        self.health_points_for_duel = 100
        if self.learn_spells_flag == 0:
            print("You haven't learned any spells yet.")
            print("You need to go to charms class with Professor Flitwick to learn some magic spells.")
            print('Example: my.learn_spells()')
        else:
            game_over = 0
            while game_over == 0:
                (result, your_spell, opponent_spell) = duel_voldemort(self.wand_movement_pattern)
                self.health_points_for_duel -= 20
                print(f"\nLord Voldemort's spell was {opponent_spell} : {self.spells_dict[opponent_spell]}.")
                print(f"\nYour spell was {your_spell} : {self.spells_dict[your_spell]}.")
                if result == 0:
                    print(f'you have {self.health_points_for_duel} % energy to cast spells.\n')    
                if result == 0 and self.health_points_for_duel > 0:
                    print(f'Keep fighting...')            
                elif result == 1:
                    print("*******************************")
                    print("You win! Lord Voldemort is dead.")
                    print("*******************************")
                    game_over = 1
                else:
                    print("You lost the duel, better luck next time.")
                    game_over = 1
            print(' ')
            print('Go for a night crawl (or) Play Quidditch again (or) fight Lord Voldemort')
            print('Examples:')  
            print('my.night_crawl()')
            print('my.play_quidditch()')
            print('my.fight_voldemort()')
            print(' ') 
        
    def display(self):
        '''
        Displays the current class object attributes and gives the user instructions for the next step.

        Arguments:
        None
        '''
        message = f'Hello wizard {self.name}.\n'  \
                  f'You are currently assigned to {self.House} house in Hogwarts magic school.\n'  \
                  f'Your best friend is {self.best_friend}.\n'  \
                  f"Your magical wand wood type is {self.wand_wood_type}, core is made of {self.wand_core}, and it's length is {self.wand_length}.\n"   \
                  f'You currently have {self.Golden_Galleons} Golden Galleons, {self.Silver_Sickles} Silver Sickles, {self.Bronze_Knuts} Bronze Knuts.\n'  \
                  f'Your house value is {self.house_value}, '  \
                  f'house mascot is {self.house_mascot}, '  \
                  f'house colors are {self.house_colors}, '  \
                  f'house ghost is {self.house_ghost}, '  \
                  f'house founders relic is {self.house_founders_relic}.\n'  \
                  f'You have {self.house_cup_points} house cup points.\n'  \
                  f'Your house quidditch rating is {self.house_quidditch_rating}.\n'  \
                  f'You have {self.health_points_for_duel} health points for a fight with Lord Voldemort.'
        print(message)
        if self.learn_spells_flag == 1:
            print(' ')
            print("Now it's time for some fun!")
            print('Go for a night crawl (or) Play Quidditch (or) fight Lord Voldemort')
            print('Examples:')  
            print('my.night_crawl()')
            print('my.play_quidditch()')
            print('my.fight_voldemort()')
            print(' ')
        else:
            print(' ')
            print("You have not learned any spells yet. It's time to go to charms class with Professor Flitwick to learn some magic spells!")
            print('Example: my.learn_spells()')
            print(' ')
        