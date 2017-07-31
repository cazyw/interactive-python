# Rock-paper-scissors-lizard-Spock template
# http://www.codeskulptor.org/#user40_HqUB1pMrjc0qexK.py
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

# converts the input name and returns the number
def name_to_number(name):
    if name == 'rock':
        num = 0
    elif name == 'Spock':
        num = 1
    elif name == 'paper':
        num = 2
    elif name == 'lizard':
        num = 3
    elif name == 'scissors':
        num = 4
    else:
        num = 'error'
    return (num)

# converts the input number and returns the name
def number_to_name(number):
    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard'
    elif number == 4:
        name = 'scissors'
    else:
        name = 'error'
    return (name)
    

def rpsls(player_choice): 
    # delete the following pass statement and fill in your code below
    # pass
    
    # print a blank line to separate consecutive games
    print ""
    
    # print out the message for the player's choice
    print "Player chooses %s" % player_choice
    
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    if player_number == 'error':
        print "That is an invalid input"
        return
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5,1)
    
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    if comp_choice == 'error':
        print "The computer has picked an invalid entry"
        return
    
    # print out the message for computer's choice
    print "Computer chooses %s" % comp_choice

    
    # compute difference of comp_number and player_number modulo five
    difference = (comp_number - player_number) % 5 
    
    # use if/elif/else to determine winner, print winner message   
    if difference == 0:
        print "Player and computer tie!"
    elif difference <= 2:
        print "Computer wins!"
    else:
        print "Player wins!"    
        
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


