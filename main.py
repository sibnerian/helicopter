#Import Modules
import os, pygame
from pygame.locals import *
from random import random

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Wall(pygame.sprite.Sprite):
    """The boundaries of the helicopter's tunnel"""
    def __init__(self, left=600, top = 200):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('wall.png', None)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = left, top
        self.move = -1 * scrollspeed
    def update(self):
        if(scrollspeed ==0):
            return
        newpos = self.rect.move((self.move, 0))
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_rect().right :
            self.kill()
        self.rect = newpos


class Obstacle(Wall):
    """ A mischievously floating piece of rock to make the game interesting."""
    def __init__(self, left, top):
        Wall.__init__(self, left, top)
        self.image, self.rect = load_image('wall.png', None)
        self.image = pygame.transform.scale(self.image, obstacle_size )
        self.rect.size = obstacle_size
        self.rect.topleft = left, top
        print "Making obstacle " + str(left) + "," + str(top)

    def update(self):
        Wall.update(self)

class Helicopter(pygame.sprite.Sprite):
    """The helicopter- i.e., the only game object to be affected by gravity"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('heli.gif', -1)
        self.image = pygame.transform.scale(self.image, (135/2, 75/2))
        self.rect.size = 133/2, 73/2
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.centery = self.area.height/2
        self.rect.left = 5
        self.acceleration = 0.05
        self.velocity = 0.0

    def update(self):
        if scrollspeed ==  0 :
            return
        self.rect = self.rect.move(0, self.velocity)
        self.velocity += self.acceleration*5
        self.velocty = min(self.velocity, 15)
    def hit_gas(self):
        self.acceleration = -0.03

    def release_gas(self):
        self.acceleration = 0.04

class Level_controller:
    """ Controls the game logic, keeping track of scores and such"""
    def __init__(self):
        self.distance_travelled = 0
        for i in range(width/25):
            wall = Wall(25*i, height-75)
            bottom_wall_sprites.add(wall)
            self.last_added_bottom = wall
            ceiling = Wall(25*i)
            ceiling.rect.bottom = 75
            top_wall_sprites.add(ceiling)
            self.last_added_top = ceiling
            self.number_of_blocks_added = 0

    def move_level(self):
        global separation
        if scrollspeed == 0: 
            return
        self.distance_travelled += scrollspeed
        if self.last_added_bottom.rect.right <=width :
            height_diff = (random()-0.5) * 40
            new_height = min(height-5, self.last_added_bottom.rect.top + height_diff)
            new_height = max(5 + separation, new_height)
            wall = Wall(self.last_added_bottom.rect.right -1, new_height)
            bottom_wall_sprites.add(wall)
            self.last_added_bottom = wall
            ceiling = Wall(self.last_added_top.rect.right -1)
            ceiling.rect.bottom = new_height - separation
            self.last_added_top = ceiling
            top_wall_sprites.add(ceiling)


            #Put in obstacles at the appropriate juncture
            if(self.number_of_blocks_added % 7 == 0):
                obstacle_top_height = ceiling.rect.bottom + random() * (separation - 50)
                obstacle = Obstacle(ceiling.rect.left, obstacle_top_height)
                top_wall_sprites.add(obstacle)
                print self.number_of_blocks_added


            self.number_of_blocks_added += 1


            if(self.number_of_blocks_added % 50 == 0 ):
                separation = max(150, separation - 25 )

    def get_score(self):
        return self.distance_travelled/8


#Sprite groups
bottom_wall_sprites = pygame.sprite.RenderPlain()
top_wall_sprites = pygame.sprite.RenderPlain()
obstacle_sprites = pygame.sprite.RenderPlain()
copter = pygame.sprite.RenderPlain()

#Globals
width, height = 1200, 600
scrollspeed = 3
separation = 400
obstacle_width, obstacle_height = 30, 50
obstacle_size = obstacle_width, obstacle_height
clock = pygame.time.Clock()

#pygame objects
screen = None
background = None
controller = None
helicopter = None

#initialize pygame
pygame.init()

birds = [" plucky lark", " European swallow", "n African swallow", " majestic sparrow", " hawk", "n eagle", " flamingo", " lame chicken "]
birdnum = None

def initialize_everything():
    #Initialize Everything
    global scrollspeed
    scrollspeed = 3
    global screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Helicopter')
    pygame.mouse.set_visible(1)
    global bottom_wall_sprites
    bottom_wall_sprites = pygame.sprite.RenderPlain()
    global top_wall_sprites 
    top_wall_sprites = pygame.sprite.RenderPlain()
    global obstacle_sprites 
    obstacle_sprites = pygame.sprite.RenderPlain()

    #Create The Backgound
    global background 
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((25, 25, 25))


    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Prepare Game Objects
    global controller 
    controller = Level_controller()
    global helicopter
    helicopter = Helicopter()
    global copter
    copter = pygame.sprite.RenderPlain()
    copter.add(helicopter)

    #Very important. This tells the "game over" message what bird to compare your flight with.
    global birdnum
    birdnum = int(random() * len(birds))

#functions to create resources- from the pygame tutorial
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound






def get_score_surface(score_num):
    if pygame.font:
        font = pygame.font.Font(None, 20)
        text = font.render("Score: " + str(score_num), 1, (250, 250, 250))
        return text

def get_game_over_surface(score):
    if pygame.font: 
        font = pygame.font.Font(None, 45)
        text = font.render("Like a" + birds[birdnum] +", you flew "+str(score)+" meters. Press R to fly again.", 1, (250, 250, 250))
        return text






def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    initialize_everything()

#Main Loop
    while 1:
        clock.tick(60)
        controller.move_level()

    	#Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN or \
            event.type == KEYDOWN and event.key == K_UP:
                helicopter.hit_gas()
            elif event.type is MOUSEBUTTONUP or \
            event.type == KEYUP and event.key == K_UP:
                helicopter.release_gas()
            elif event.type is KEYDOWN and event.key == K_r:
                initialize_everything()

        bottom_wall_sprites.update()
        top_wall_sprites.update()
        obstacle_sprites.update()
        copter.update()

    	#Draw Everything
        screen.blit(background, (0, 0))
        bottom_wall_sprites.draw(screen)
        top_wall_sprites.draw(screen)
        obstacle_sprites.draw(screen)
        copter.draw(screen)

        #Check for collisions and explode the helicopter if there is one
        if len(pygame.sprite.groupcollide(copter, top_wall_sprites, 0, 0)) != 0 or \
           len(pygame.sprite.groupcollide(copter, bottom_wall_sprites, 0, 0)) != 0 or \
           len(pygame.sprite.groupcollide(copter, obstacle_sprites, 0, 0)) != 0:
           global scrollspeed
           scrollspeed = 0
           text = get_game_over_surface(controller.get_score())
           textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/2)
           screen.blit(text, textpos)
           #print "game over, man, game over!"
        screen.blit(get_score_surface(controller.get_score()), (10, 10))
        pygame.display.flip()
           

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()