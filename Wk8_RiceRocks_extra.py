# ========================================
# 
# Week 8 - Spaceship - RiceRocks
#
# The program uses and builds upon the 
# week 8 template provided (not using my 
# own Spaceship implementation)
#
# Additions:
# - different explosion images for missile
#   strike vs ship collision
# - records high score across games
# - records scores of previous 10 games
# - does not spawn rocks directly on ship
# - explosions occur between ship and rock
#
# ========================================
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
MAX_ROCKS = 12 # max 12 asteroids
POINT_VAL = 10 # score increments by 10
prev_scores = [] # keep track of previous scores
prev_scores_label = [] # label for scores
score = 0
high_score = 0
lives = 3
time = 0
game = 0 # game count
started = False


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")


# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)


    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
       
        # update friction
        self.vel[0] *= .99
        self.vel[1] *= .99
        

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        
        # creates a missile
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)

        # adds missile to the set
        missile_group.add(a_missile)
    
    # gets the radius
    def get_radius(self):
        return self.radius
    
    # gets the position
    def get_position(self):
        return self.pos
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        # checks if object is animated 
        # ie an explosion and if so draws the 
        # appropriate image
        if self.animated:
            exp_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, exp_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update age of sprite
        self.age += 1
        
        # returns true if time to delete
        return self.age > self.lifespan

    
    
    # gets radius
    def get_radius(self):
        return self.radius
    
    # gets position
    def get_position(self):
        return self.pos
    
    # returns true if the distance between the two 
    # objects is less than or equal to the sum of the 
    # radii of both objects
    def collide(self, other_object):
        distance = dist(self.pos, other_object.get_position())
        radii_sum = self.radius + other_object.get_radius()
        return distance <= radii_sum
    
    
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, high_score, prev_scores, prev_scores_label, game
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
        lives = 3
        
        # adds the game number and score to the 
        # beginning of the list
        if game > 0:
            prev_scores.insert(0, [game, score])
        
        # pops the last score off if more than 10 scores
        if len(prev_scores) > 10:
            prev_scores.pop(10)
        
        # displays the scores in the console
        # (most recent game at the top)
        for i in range(len(prev_scores)):
            prev_scores_label[i].set_text("Game: " + str(prev_scores[i][0]) + " - Score: " + str(prev_scores[i][1]))
            
        score = 0
        game += 1
        

def draw(canvas):
    global time, started, lives, score, high_score, rock_group, missile_group, my_ship, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
 
    # draw UI - drawn after sprites so scores are 'ontop'
    # of objects
    canvas.draw_text("Lives", [50, 50], 22, "White", "sans-serif")
    canvas.draw_text("Score", [680, 50], 22, "White", "sans-serif")
    canvas.draw_text(str(lives), [50, 80], 22, "White", "sans-serif")
    canvas.draw_text(str(score), [680, 80], 22, "White", "sans-serif")


    # if ship collides with rock, lose a life
    if group_collide(rock_group, my_ship, "ship"):
        lives -= 1
        
    # if missile hits rock, add to score
    # (multiple of 10s)
    score += POINT_VAL * group_group_collide(missile_group, rock_group)

    # if no more lives, end game and reset values
    if lives == 0:
        started = False
        rock_group = set([])
        soundtrack.rewind()
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())   
        if score > high_score:
            high_score = score
        h_score.set_text('HIGH SCORE = ' + str(high_score))
    
                          
            
# helper draw function to draw and update
# a group of sprites
# If update returns false (i.e. end of life
# for a missile), remove the sprite from the group
def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)
            
        
        
# timer handler that spawns a rock
# ADDITIONAL CHECKS:
# This implementation checks that a 
# spawned rock will not spawn within a
# ship's radius and therefore cause
# mysterious loss of life

def rock_spawner():
    global rock_group, my_ship
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    
    # checks that:
    # - won't spawn a direct collision with ship
    # - fewer than 12 rocks on screen
    # - game has started
    
    if not a_rock.collide(my_ship):
        if len(rock_group) < MAX_ROCKS and started:
            rock_group.add(a_rock)

# checks collisions between a group and object
# returns true if object has collided with an
# item in the group
# ADDITION:
# checks the type of collision
# the explosion image changes depending on whether
# it was a missile strike or a ship/rock collision
# ship collision - explosion appears between rock and ship
# missile hit - explosion appears at rock location
def group_collide(group, other_object, collision_type):
    global explosion_group
    for item in set(group):
        if item.collide(other_object):
            if collision_type == "ship":
                # gets position between ship and rock
                ship_pos = other_object.get_position()
                rock_pos = item.get_position()
                exp_middle = [(ship_pos[0] + rock_pos[0]) // 2, (ship_pos[1] + rock_pos[1]) // 2]
                explosion = Sprite(exp_middle, [0,0], 0, 0, explosion_ship_image, explosion_info, explosion_sound)
            else:
                explosion = Sprite(item.get_position(), [0,0], 0, 0, explosion_missile_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            group.remove(item)
            return True
        
# checks collisions between two groups
# assignment purposes - rocks and missiles
# returns how many rocks were destroyed
def group_group_collide(group1, group2):
    hits = 0
    for item in set(group1):
        if group_collide(group2, item, "missile"):
            group1.discard(item)
            hits += 1
    return hits    
        
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

# additional labels to display the 
# high score and scores of the previous 10 games
h_score = frame.add_label('HIGH SCORE = 0', 200)
frame.add_label('', 200)
frame.add_label('Scores for previous 10 games:', 200)
frame.add_label('', 200)
for i in range(10):
    prev_scores_label.append(frame.add_label(""))


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
