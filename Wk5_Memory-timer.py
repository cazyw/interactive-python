# implementation of card game - Memory

import simplegui
import random

turns = 0
best_game = 0 # fewest turns
worst_game = 0 # most turns

# background images for the cards
im = simplegui.load_image("http://ichef.bbci.co.uk/images/ic/1200x675/p01lzjsf.jpg")

# helper function to initialize globals
def new_game():
    global cards_flipped, turns, numbers, exposed, time
    cards_flipped, turns, time = 0, 0, 10
    exposed = [] # holds list of all opened/flipped cards
    numbers = range(0,8)+range(0,8)
    random.shuffle(numbers)
    
    # prints the list of shuffled numbers
    print "random numbers: ", numbers
    
    # stop timer once game starts
    label_finish.set_text("")
    timer.stop()
     
# define event handlers
def mouseclick(pos):
    global cards_flipped, turns, card

    # calculates which of the 16 cards
    # was clicked (from 0-15)
    hor_pos = (pos[0] // 50)
    if(pos[1] > 100):
        card = 8 + hor_pos # second row
    else:
        card = hor_pos # first row
    
    # if the card clicked is already 'revealed'
    # do nothing
    if card in exposed:
        return
    
    # exposed[] holds a list of all 'opened' cards
    # when selecting a card...
    # if one card is already flipped open, add the selected card
    #      to exposed[]
    # if two cards are already flipped open, checks to see if they
    #      match and if so, add the selected card to exposed[]
    # if not matching, pop the last two cards opened from
    #      exposed[] and add the selected card
    
    if cards_flipped == 0:
        cards_flipped = 1
        exposed.append(card)
    elif cards_flipped == 1:
        cards_flipped = 2
        exposed.append(card)
        turns += 1
    else:
        cards_flipped = 1
        if numbers[exposed[-1]] == numbers[exposed[-2]]:
            exposed.append(card)
        else:
            exposed.pop()
            exposed.pop()
            exposed.append(card)
                 
# timer to automatically restart a new game 
# after 10 seconds if not manually reset
def timer_handler():
    global time
    time -= 1        

    if time == 0:
        new_game()

    
# cards are logically 50x100 pixels in size
# and arranged in two rows of eight cards
def draw(canvas):
    global best_game, worst_game
    card_draw = 0
    label.set_text("Turns = " + str(turns))
    
    for ver in range(2):
        for hor in range(8):
            if card_draw in exposed:
                canvas.draw_polygon([[0+50*hor,0+100*ver], [50+50*hor, 0+100*ver], \
                                 [50+50*hor, 100+100*ver], [0+50*hor, 100+100*ver]],\
                                1, 'White', 'Teal')
                canvas.draw_text(str(numbers[card_draw]), (15+50*hor, 70+100*ver), 48, 'Orange', 'sans-serif')
            else:
                #IF USING COLOR BACKGROUND
                #canvas.draw_polygon([[0+50*hor,0+100*ver], [50+50*hor, 0+100*ver], \
                #                 [50+50*hor, 100+100*ver], [0+50*hor, 100+100*ver]],\
                #                2, 'White', 'Teal')
                
                #IF USING IMAGE BACKGROUND
                canvas.draw_image(im, (1200 // 2, 675 // 2), (337, 675), (25+50*hor, 50+100*ver), (50, 100))
            
            hor += 1
            card_draw += 1
        ver += 1

        # if all cards are matched, print extra text and 
        # count down a timer to autmatically start a new 
        # game in 10 seconds if not manually reset
        if len(exposed) == 16:
            canvas.draw_text("GAME OVER!", (10,120), 60, 'Navy', 'sans-serif')
            timer.start()
            label_finish.set_text("Hit the reset button or the \
                                  game will reset in " + \
                                  str(time) + " seconds")

            # updates scores of best and worst game
            if best_game == 0 or turns < best_game:
                best_game = turns
    
            if worst_game == 0 or turns > worst_game:
                worst_game = turns   
    
            label_best.set_text("Best game = " + str(best_game) + " turns")
            label_worst.set_text("Worst game = " + str(worst_game) + " turns") 
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 400, 200)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
label_blank = frame.add_label("")
label_finish = frame.add_label("")
label_blank2 = frame.add_label("")
label_best = frame.add_label("Best game = 0 turns")
label_worst = frame.add_label("Worst game = 0 turns")
timer = simplegui.create_timer(1000, timer_handler)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
timer.start()
new_game()
frame.start()





# Always remember to review the grading rubric