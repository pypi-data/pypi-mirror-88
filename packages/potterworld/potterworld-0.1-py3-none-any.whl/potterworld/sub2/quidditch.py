from numpy.random import choice

def quidditch(rating, points, house):
    """
    This function selects the winner of the first game of Quidditch game based on house rating of the wizard. 
    And in the second game, this function gets inputs from the wizard for catching a snitch. 

    House points are awarded or deducted from the house in each game. 
    Function returns the updated house points.
    
    Arguments:
    rating - (int or float) - represents the house rating of the player.
    points - (int or float) - represents house cup points of the player's house.
    house - (str) - represents the house of the player.
    """      
    plus_minus = 0
    win_flag = choice(a = [0,1], size = 1, p = [(1-rating), rating])
    if win_flag == 1:
        plus_minus += 10
        print('\nCongratulations !!!')
        print(f"The chasers for your house ({house}) scored the quaffle by throwing it through the hoops past the opponents keeper.")
        print('You scored 10 house points!')
        print(f'{house} house now has a total of {points + plus_minus} house cup points.')
    else:
        plus_minus -= 10
        print(f"\nSorry, your house ({house}) beater performed an illegal illegally hit th opponents seeker with their club. The referee deducts 10 points from your team.")
        print(f'{house} house now has a total of {points + plus_minus} house cup points.')
    print('\nDo you want to catch the snitch, which ends the game and awards you 150 bonus house points?')
    user_input = input("Enter y to catch the snitch, or enter any other character if not interested: ") 
    if user_input.lower() == 'y':  
        print(' ')
        print('There are five doors (1,2,3,4,5) and a snitch is in one of them. Guess where is the snitch, you can only check 2 doors.')
        print(' ')
        counter = 0
        while counter < 2:
            try:
                door = int(input('Enter the door number :'))
                counter += 1
                if door in [1,3,5]:
                    plus_minus += 150
                    print(f"\nCongratulations! You caught the snitch. The game is over and you get 150 bonus points! {house} house now has a total of {points + plus_minus} points.")
                    break
                else:
                    if counter < 2:
                        print('\nSnitch is not here, try another door. You have one more chance\n')
                    else:
                        print(f"\nSorry, the Snitch escaped and your opponent's seeker caught it. The game is over and you receive no bonus points.\n")
                    continue
            except ValueError:
                print('\nYou must enter a valid integer 1,2,3,4,5. Please try again.\n')
                continue
        return (points + plus_minus)
    else:
        print('\nYour opponent house seeker caught the snitch and the game is over.\n')
        return (points + plus_minus)
