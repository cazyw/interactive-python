##############################################
# Implementation of classic arcade game Pong #
##############################################
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# variables used in keypress functions to 
# smooth motion (incase both up and down pressed)
press_W = False
press_S = False
press_Up = False
press_Down = False

"""
initialize ball_pos and ball_vel for new bal in middle of table
if direction is RIGHT, the ball's velocity is upper right, else upper left
"""
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # starts the ball in the middle 
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # randomises the velocity and sets the direction
    horizontal = random.randrange(120, 240) / 60
    vertical = -random.randrange(60, 180) / 60
    
    if direction == RIGHT:
        ball_vel = [horizontal, vertical]
    else:
        ball_vel = [-horizontal, vertical]
        

# define event handlers

"""
Starts a brand new game of Pong
"""
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # brand new games spawn randomly
    spawn_ball(random.choice([RIGHT, LEFT]))
    
    # resets the paddle to the middle and resets the score
    paddle1_pos, paddle2_pos = HEIGHT / 2.0, HEIGHT / 2.0
    paddle1_vel, paddle2_vel, score1, score2 = 0, 0, 0, 0
    
    
"""
Draws the game and does the necessary calculations
"""
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0] 
    ball_pos[1] += ball_vel[1]
    
    # if ball hits top or bottom wall, reflect
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # if ball hits left wall, checks if hit paddle or gutter
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and \
        ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1 
        else:
            spawn_ball(RIGHT)
            score2 += 1
    
    # if ball hits right wall, checks if hit paddle or gutter
    if ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and \
        ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball(LEFT)
            score1 += 1
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')  
    
    # update paddle's vertical position, keep paddle on the screen
    # if top of paddle is at top of screen and key move is up, do nothing
    # if bottom of paddle is at bottom of screen and key move is down, do nothing
    # otherwise okay to move paddle
    if paddle1_pos <= HALF_PAD_HEIGHT and paddle1_vel < 0 or \
    paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT and paddle1_vel > 0:
        pass
    else:
        paddle1_pos += paddle1_vel
      
    if paddle2_pos <= HALF_PAD_HEIGHT and paddle2_vel < 0 or \
    paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT and paddle2_vel > 0:
        pass
    else:
        paddle2_pos += paddle2_vel
      
    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),\
                   (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), PAD_WIDTH, 'White')
    canvas.draw_line((WIDTH-HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), \
                   (WIDTH-HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), PAD_WIDTH, 'White')
 
    
    # draw scores with modifier to try and keep  
    # both scores a similar distance from centre
    canvas.draw_text(str(score1), (WIDTH/2 - 100, HEIGHT/4), 50, 'White', 'sans-serif')
    if score2 >= 10 and score1 >= 10:
        canvas.draw_text(str(score2), (WIDTH/2 + 100-two_dig, HEIGHT/4), 50, 'White', 'sans-serif')
    else:
        canvas.draw_text(str(score2), (WIDTH/2 + 100-one_dig, HEIGHT/4), 50, 'White', 'sans-serif')
    
"""
The coding for keyup/down handles situations where both keys 
are pressed and then only one is released for smoother
transitions for clumsy fingers
e.g. 
press W => move up
hold W and press S => stop
release W => move down (as S is still pressed)
hold S and press W => stop
release S => move up (as W is still pressed)
"""

def keydown(key):
    global paddle1_vel, paddle2_vel
    global press_W, press_S, press_Up, press_Down 
    
    # if the relevant key is pressed, flag as pressed and 
    # change the velocity
    
    if key == simplegui.KEY_MAP['w']:
        press_W = True
        paddle1_vel -= 5
    if key == simplegui.KEY_MAP['s']:
        press_S = True
        paddle1_vel += 5
    if key == simplegui.KEY_MAP['up']:
        press_Up = True
        paddle2_vel -= 5
    if key == simplegui.KEY_MAP['down']:
        press_Down = True
        paddle2_vel += 5

    
def keyup(key):
    global paddle1_vel, paddle2_vel
    global press_W, press_S, press_Up, press_Down 

    # extra coding - if a key is released, will check if the 
    # opposite key is pressed and if so, move in that direction
    
    if key == simplegui.KEY_MAP['w']:
        press_W = False
        if press_S:
            paddle1_vel += 5 
        else:
            paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
        press_S = False
        if press_W:
            paddle1_vel -= 5 
        else:
            paddle1_vel = 0
    if key == simplegui.KEY_MAP['up']:
        press_Up = False
        if press_Down:
            paddle2_vel += 5 
        else:
            paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        press_Down = False
        if press_Up:
            paddle2_vel -= 5 
        else:
            paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', new_game, 100)

# used to calculate text width for score placement
one_dig = frame.get_canvas_textwidth('1', 50, 'sans-serif')
two_dig = frame.get_canvas_textwidth('11', 50, 'sans-serif')

# start frame
new_game()
frame.start()
