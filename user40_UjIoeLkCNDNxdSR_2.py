# implementation of card game - Memory

import simplegui
import random

turns = 0
# background images for the cards
im = simplegui.load_image("http://ichef.bbci.co.uk/images/ic/1200x675/p01lzjsf.jpg")

# helper function to initialize globals
def new_game():
    global cards_flipped, turns, numbers, exposed
    cards_flipped, turns = 0, 0
    exposed = [] # holds list of all opened/flipped cards
    numbers = range(0,8)+range(0,8)
    random.shuffle(numbers)
    
    # prints the list of shuffled numbers
    print "random numbers: ", numbers
     
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
    #      if not matching, pop the last two cards opened from
    #           exposed[] and add the selected card
    
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
                       
# cards are logically 50x100 pixels in size
# and arranged in two rows of eight cards
def draw(canvas):
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
                #canvas.draw_polygon([[0+50*hor,0+100*ver], [50+50*hor, 0+100*ver], \
                #                 [50+50*hor, 100+100*ver], [0+50*hor, 100+100*ver]],\
                #                2, 'White', 'Teal')
                canvas.draw_image(im, (1200 // 2, 675 // 2), (337, 675), (25+50*hor, 50+100*ver), (50, 100))
            
            hor += 1
            card_draw += 1
        ver += 1

        # if all cards are matched, print extra text
        if len(exposed) == 16:
            canvas.draw_text("GAME OVER!", (10,120), 60, 'Navy', 'sans-serif')
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 400, 200)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric