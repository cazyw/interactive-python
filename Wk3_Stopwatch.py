# template for "Stopwatch: The Game"

import simplegui

# define global variables
time = 0
successful_stops = 0
total_stops = 0
timer_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

def format(t):
    """ Takes in time in tenths of seconds and returns 
    the time in the format A:BC.D"""
    
    minutes = ""
    tens = ""
    ones = ""
    tenths = ""
    
    minutes = str(t / 600)
    
    tens = str((t % 600) / 100)

    ones = str(((t % 600) / 10) % 10)
    
    tenths = str(t % 10)
        
    return minutes +  ":" + tens + ones + "." + tenths
    

# define event handlers for buttons; "Start", "Stop", "Reset"
def timer_starter():
    """ Starts the timer and flags as running """
    
    global timer_running
    timer.start()
    timer_running = True
    
def timer_stopper():
    """ Stops the timer. Game - calculates if stopped on a
    whole second AND the timer had been running """
    
    global total_stops, successful_stops, timer_running
    timer.stop()
    
    # increment total only if stopped when timer was running 
    if timer_running:
        total_stops += 1
        
        # increment successful if stopped on a whole second
        if time % 10 == 0:
            successful_stops += 1
    
    # flag timer as stopped
    timer_running = False

def timer_reset():
    """ Stops timer and sets totals to zero """
    
    global time, total_stops, successful_stops
    timer.stop()
    
    #resets global variables
    time = 0
    total_stops = 0
    successful_stops = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    """ When called, increments time """
    
    global time
    time += 1
    
    #print str(time) + " --> " + format(time)


    
# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time), (100, 100), 36, 'white')
    canvas.draw_text(str(successful_stops) + "/" + str(total_stops), (250, 30), 30, 'green')
    
# create frame
frame = simplegui.create_frame('Timer', 300, 200) 

# register event handlers
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer_handler)
start_but = frame.add_button('Start Timer', timer_starter, 100)
stop_but = frame.add_button('Stop Timer', timer_stopper, 100)
reset_but = frame.add_button('Reset Timer', timer_reset, 100)

# start frame
frame.start()


# Please remember to review the grading rubric
