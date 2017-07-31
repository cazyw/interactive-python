# implementation of card game - Memory

import simplegui
import random

turns = 0

# helper function to initialize globals
def new_game():
    global cardsFlipped, turns, numbers, revealed
    cardsFlipped, turns = 0, 0
    revealed = []
    numbers = range(0,8)+range(0,8)
    random.shuffle(numbers)
    print numbers
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global cardsFlipped, turns, card

    horPos = (pos[0] // 50) + 1
    if(pos[1] > 100):
        card = 8 + horPos
    else:
        card = horPos
    
    if card in revealed:
        return
    if cardsFlipped == 0:
        cardsFlipped = 1
        revealed.append(card)
    elif cardsFlipped == 1:
        cardsFlipped = 2
        revealed.append(card)
        turns += 1
    else:
        cardsFlipped = 1
        if numbers[revealed[-1]-1] == numbers[revealed[-2]-1]:
            revealed.append(card)
        else:
            revealed.pop()
            revealed.pop()
            revealed.append(card)
                       
# cards are logically 50x100 pixels in size
# and arranged in two rows
def draw(canvas):
    cardDraw = 1
    label.set_text("Turns = " + str(turns))
    
    for ver in range(2):
        for hor in range(8):
            if cardDraw in revealed:
                canvas.draw_polygon([[0+50*hor,0+100*ver], [50+50*hor, 0+100*ver], \
                                 [50+50*hor, 100+100*ver], [0+50*hor, 100+100*ver]],\
                                2, 'White', 'Black')
                canvas.draw_text(str(numbers[cardDraw-1]), (15+50*hor, 70+100*ver), 48, 'White', 'sans-serif')
            else:
                canvas.draw_polygon([[0+50*hor,0+100*ver], [50+50*hor, 0+100*ver], \
                                 [50+50*hor, 100+100*ver], [0+50*hor, 100+100*ver]],\
                                2, 'White', 'Teal')
            hor += 1
            cardDraw += 1
        ver += 1

        if len(revealed) == 16:
            canvas.draw_text("GAME OVER!", (10,120), 60, 'Orange', 'sans-serif')
        
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