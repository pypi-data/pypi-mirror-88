'''
This package simulates user becoming a wizard. 
Wizards complete various tasks, learns spells, plays Quidditch, Duels with Lord Voldemort etc. using various modules of this package.

Subpackages >> Classes
----------------------
sub1
    Hogwarts
    Wizard
sub2
    spells
    learn_spells
'''
from potterworld.sub1.hogwarts import Hogwarts
from potterworld.sub1.wizard import Wizard
from potterworld.sub1.sorting_hat_song import print_song

from potterworld.sub2.spells import spells 
from potterworld.sub2.learn_spells import learn_spells
from potterworld.sub2.duel import duel_voldemort
from potterworld.sub2.quidditch import quidditch

print("Thank you for your interest in the potter world!")
print("Please start by sending in your application to Hogwarts magic school by following the example below - use your name instead of John")
print(" ")
print('me = Wizard("John")')
print(" ")