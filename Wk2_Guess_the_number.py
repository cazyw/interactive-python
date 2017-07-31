# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# the game initially defaults to a range of 100
num_range = 100

# helper function to start and restart the game
def new_game():
    """ Initialises a new game """
    
    # initialize global variables used in your code here
    # randomly select the secret number
    
    global secret_number, num_range, initial_count
    secret_number = random.randrange(0, num_range)
    
    # sets the maximum number of guesses
    
    initial_count = int(math.ceil(math.log(num_range, 2)))

    
    print "\nNew game. Range is [0,"+str(num_range)+")"
    print "Number of remaining guesses is ",initial_count


# define event handlers for control panel
def range100():
    """ Sets the upper limit to 100 and starts a new game """

    global num_range
    num_range = 100
    new_game()


def range1000():  
    """ Sets the upper limit to 1000 and starts a new game """

    global num_range
    num_range = 1000
    new_game()

    
def input_guess(guess):
    """ The player enters input to guess the secret number. The numbers are
    compared and a hint (if required) is provided. If the guess is correct 
    or there are no more guesses, the game resets """

    print "\nGuess was", guess

    # calculates the number of guesses remaining
    
    global initial_count
    initial_count -= 1
    print "Number of remaining guesses is ",initial_count

    # if the input is not a positive integer, 
    # prints an error message    
    
    if not guess.isdigit():
        print "Invalid entry. Please enter an integer in range [0," + str(num_range) + ")"
        return
    
    # converts the input into an integer
    
    guess_number = int(guess)
       
    # compares the guess with the secret number and also considers
    # how many guesses are remaining
    
    if guess_number == secret_number:
        print "Correct!"
        new_game()
    elif initial_count == 0:
        print "You ran out of guesses.  The number was", secret_number
        new_game()
    elif guess_number < secret_number:
        print "Higher!"
    elif guess_number >= num_range:
        print "Lower! - also the range is [0," + str(num_range) + ")"
    else:
        print "Lower!"

    
# create frame
frame = simplegui.create_frame('Guess the number', 200,200)
frame.start()

# register event handlers for control elements and start frame
inp = frame.add_input('Guess:', input_guess,100)
button1 = frame.add_button("Range is [0,100)", range100, 200)
button2 = frame.add_button("Range is [0,1000)", range1000, 200)

# call new_game 
new_game()



# always remember to check your completed program against the grading rubric
