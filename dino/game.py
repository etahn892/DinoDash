import pygame as pg
from pygame import *
import random
import pickle
from os import path
import time
pg.init()
screenspace = 60
height = 800 + screenspace
width = 800
doublejumpbought = False
screen = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption('Capstone Game')
clock = pg.time.Clock()


EasyHealth = 150
EasyLives = 5
MediumHealth = 100
MediumLives = 4 
HardHealth = 10
HardLives = 1 
SelectedHealth = 0 

#game variables
tile_size = 40
fps = 60
health = 10
lives = EasyLives
StartMenu = 1
max_level = 2
bone_count = 0
total_bone_count  = 0
current_time = 0
start_point = 0
loadingscreen = False
loadingscreentimer = 2000

# custom user events
hit_cooldown = pg.USEREVENT + 1
doublejump = pg.USEREVENT + 2
candoublejump = False

# load basic images
SUN = pg.transform.scale(pg.image.load('img/sun.png'), (200,200))
BG = pg.transform.scale(pg.image.load('img/BG.jpg'), (width, height-screenspace))
shopBG = pg.transform.scale(pg.image.load('img/shopbackground2.png'), (width, height))
deaddino = pg.image.load('dino/dead.png')
restart_IMG = pg.image.load('img/restart_btn2.png')
HowToPlay_IMG = pg.transform.scale(pg.image.load('img/howtoplay.png'), (433,100))
levelselect_IMG = pg.transform.scale(pg.image.load('img/levelselect.png'), (433,100))
settings_IMG = pg.transform.scale(pg.image.load('img/settings_btn.png'), (75,75))
begin_IMG = pg.transform.scale(pg.image.load('img/begin_btn.png'), (200,100))
menu_IMG = pg.transform.scale(pg.image.load('img/menu_btn.png'), (100,50))
arrows = pg.transform.scale(pg.image.load('img/arroe.png'), (240,200))
downarrow = pg.image.load('img/downarrow.png')
keys = pg.transform.scale(pg.image.load('img/keys.png'), (240,200))
start_IMG = pg.transform.scale(pg.image.load('img/start_btn.png'), (200,100))
exit_IMG = pg.transform.scale(pg.image.load('img/exit_btn.png'), (200,100))
exit2_IMG = pg.transform.scale(pg.image.load('img/exit_btn.png'), (76,40))
exitgame = pg.transform.scale(pg.image.load('img/exitgame.png'), (400,400))
next_IMG = pg.transform.scale(pg.image.load('img/nextlevel.png'), (125,66))
smallnext_IMG = pg.transform.scale(pg.image.load('img/nextlevel.png'), (100,50))
load_img = pg.transform.scale(pg.image.load('img/load_btn.png'), (100,50))
extralife_IMG1 = pg.transform.scale(pg.image.load('img/nopluslife.png'), (300,200))
extralife_IMG2 = pg.transform.scale(pg.image.load('img/maxpluslife.png'), (300,200))
extralife_IMG = pg.transform.scale(pg.image.load('img/pluslife.png'), (300,200))
doublejump_IMG1 = pg.transform.scale(pg.image.load('img/nodoublejump.png'), (300,200))
doublejump_IMG2 = pg.transform.scale(pg.image.load('img/doublejumpbought.png'), (300,200))
doublejump_IMG = pg.transform.scale(pg.image.load('img/doublejump.png'), (300,200))
bone_IMG= pg.transform.scale(pg.image.load('dino/bone.png'), ((tile_size // 2)+10, (tile_size // 2)+10))
loadingIMGS = []
for i in range(1,8):
    img = pg.image.load(f'loading/Fotor_AI({i}).png')
    img = pg.transform.scale(img, (width, height))
    img = loadingIMGS.append(img)

rightBoost_IMG = pg.trasform.rotate(pg.transform.scale(pg.image.load('img/jumpboost.png'), ((tile_size // 2)+10, (tile_size // 2)+10)), 90)

# font settings
WHITE = (255,255,255)
RED = (255,0,0)
MINTGREEN = (96,96,96)
notactivegreen =  (206,194,255)
activegreen = (173,153,255)
DEEPPURPLE = (25,22,39)
MINTBLUE = (216,226,220)
GOLD = (216,226,220)
store_color = (127,112,195)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
font = pg.font.SysFont('Courier Regular', 93)
gameoverfont = pg.font.SysFont('Bauhaus 93', 100)
boughtfont = pg.font.SysFont('Lucida Sans Typewr', 60)
scorefont = pg.font.SysFont('Courier Regular', 40)

#loading bar
loadingBar_width = 200
loadingBar_height = 20
loadingBar_x = ((screen.get_width() - loadingBar_width) // 2) - 150
loadingBar_y = ((screen.get_height() - loadingBar_height) // 2) + 400
loadingBar_color = RED
progress = 0
max_progress = 100

#health bar
healthBar_width = 200
healthBar_height = 20
healthBar_x = ((screen.get_width() - healthBar_width) // 2) - 290
healthBar_y = ((screen.get_height() - healthBar_height) // 2) + 400
healthBar_color = RED

def print_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def reset_level(level):
    player.reset(100, height - 130)
    spider_group.empty()
    lava_group.empty()
    PortalDoor_group.empty()
    deeplava_group.empty()
    JumpBoost_group.empty()
    RightBoost_group.empty()

    Trampoline_group.empty()
    bone_group.empty()
    if path.exists(f'levels/level{level}_data'):
        pickles = open(f'levels/level{level}_data', 'rb')
        world_data = pickle.load(pickles)
    else:
        level += 1
        pickles = open(f'levels/level{level}_data', 'rb')
        world_data = pickle.load(pickles)
    world = World(world_data)
    
    return world

def grid():
    for line in range(0, 20):
        pg.draw.line(screen, (220, 240, 239), (0, line * tile_size), (width, line * tile_size))
        pg.draw.line(screen, (220, 240, 239), (line * tile_size, 0), (line * tile_size, height))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        reset_game = False

        #get mouse position
        pos = pg.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                reset_game = True
                self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        screen.blit(self.image, self.rect)

        return reset_game

class Player():
    def __init__(self, x, y):
        self.reset(x,y)
        
    def update(self, health):
        dx = 0
        dy = 0
        cooldown = 6
        

        # player controls
        randomlist=[]
        for i in range(0,200):
            n = random.uniform(3,6)
            randomlist.append(n)
        num1 = random.choice(randomlist)
        if not health < -1:
            key = pg.key.get_pressed()
            if (key[pg.K_SPACE] and self.jumped==True and self.in_air == True and self.doublejump == False) and self.candoublejump:
                self.vel_y = -12
                self.doublejump = True


            if (key[pg.K_UP] and self.jumped == False and self.in_air == False) or (key[pg.K_w] and self.jumped == False and self.in_air == False):
                jumpheight = round(random.uniform(-8, -14.5), 3)
                self.vel_y = jumpheight
                self.jumped = True
            
            if key[pg.K_LEFT] or key[pg.K_a]:
                dx -= num1
                self.counter += 1
                self.direction = -1

            if key[pg.K_RIGHT] or key[pg.K_d]:
                dx += num1
                self.counter += 1
                self.direction = 1

            if (key[pg.K_LEFT] == False and key[pg.K_RIGHT] == False) and (key[pg.K_a] == False and key[pg.K_d] == False):    
                self.counter = 0
                self.index = 0 
                if self.direction == 1:
                    self.image = self.img_right[self.index]
                if self.direction == -1:
                    self.image = self.img_left[self.index]

            #dont pass screen borders    
            if self.rect.x < -5:
                self.rect.x = 1
            if self.rect.x > 775:
                self.rect.x= 770
            if self.rect.y > height:
                health -= 1
            
            
            #characters animation
            
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.img_right):
                    self.index=0
                if self.direction == 1:
                    self.image = self.img_right[self.index]
                if self.direction == -1:
                    self.image = self.img_left[self.index]
            
            # gravity
            self.vel_y += 1

            # sets a terminal velocity
            if self.vel_y > 20:
                self.vel_y = 20
            dy += self.vel_y
            
            #collision check for movement
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if self.vel_y == 20:
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        pg.time.set_timer(hit_cooldown, 350)
                        self.cooldown = True
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.doublejump = False
                        health -= 1
                        self.in_air = False
                        self.jumped = False
                

                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if jumping / player hitting head on tile
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if falling / player is touching ground
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.doublejump = False

                        self.in_air = False
                        self.jumped = False

            #player collisions with objects
            if pg.sprite.spritecollide(self, spider_group, False) and self.cooldown == False:
                    health -= 1
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)
                    
            if pg.sprite.spritecollide(self, lava_group, False) and self.cooldown == False:
                    health -= 1
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)
                    
            if pg.sprite.spritecollide(self, deeplava_group, False) and self.cooldown == False:
                    health -= 2
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)

            if pg.sprite.spritecollide(self, PortalDoor_group, False):
                    health = -10


            if pg.sprite.spritecollide(self, JumpBoost_group, False):
                    self.vel_y -= random.uniform(1,3)
            if pg.sprite.spritecollide(self, RightBoost_group, False):
                    dx += num1
                    self.direction = 1                    
            if pg.sprite.spritecollide(self, Trampoline_group, False) and self.jumped == False:
                    self.vel_y = round(random.uniform(-10,-12), 4)
                    dy += .25
            if pg.sprite.spritecollide(self, Trampoline_group, False) and self.jumped == True:
                    self.vel_y -= 4.9
                 #   dy = 0
                  #  pass  
                    

            if self.cooldown == True:
                if self.direction == 1:
                    self.image = self.damage[0]
                    
                if self.direction == -1:
                    self.image = self.damage[1]

            self.rect.x += dx
            self.rect.y += dy

        screen.blit(self.image, self.rect)      

        return health
                

    def reset(self, x, y):
        self.img_right = []
        self.img_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,10):
            right_IMG = pg.image.load(f'dino/0{num}_DinoSprites - doux.png')
            right_IMG = pg.transform.scale(right_IMG, (30,40))
            left_IMG = pg.transform.flip(right_IMG, True, False)
            self.img_right.append(right_IMG)
            self.img_left.append(left_IMG)
        damage_image = pg.image.load('dino/damage.png')
        dead_image = pg.image.load('dino/ghost.png')
        right_damage_IMG = pg.transform.scale(damage_image, (30,40))
        left_damage_IMG = pg.transform.flip(damage_image, True, False)
        left_damage_IMG = pg.transform.scale(damage_image, (30,40))
        self.damage = [right_damage_IMG, left_damage_IMG]
        self.dead_image = pg.transform.scale(dead_image, (60,60))
        self.image = self.img_right[self.index]
        f = open('levels/highscore.txt', 'r')
        self.highscore = f.readline()

        self.cooldown = False
        self.deathnum = random.randint(0,len(DeathQuotes)-2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.doublejump = False
        self.candoublejump = candoublejump
        self.jumped = False
        self.direction = 0  
        self.in_air = True

class Spider(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        IMG = pg.image.load(f'spider/tile001.png')
        IMG = pg.transform.scale(IMG, (40,29))
        self.image = IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 4
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_direction = 1
        self.counter = 0
        self.randomlist = []
        for i in range(0,20):
            n = round(random.uniform(10,30), 2)
            self.randomlist.append(n)

    def update(self):
        self.rect.x += self.move_direction
        self.counter += 1
        num1 = random.choice(self.randomlist)
        num1 = 3000
        if abs(self.counter) > num1:
            self.move_direction *= -1
            self.counter *= -1
            

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.move_direction *= -1
                             
      
        #pg.draw.rect(screen, (255,255,255), self.rect,2)

class Lava(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/lava.png')
        img2 = pg.image.load('img/lava.png')
        self.image = pg.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class DeepLava(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/deeplava.png')
        self.image = pg.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BoostUp(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/jumpboost.png')
        self.image = pg.transform.scale(img, ((tile_size // 2)+10, (tile_size // 2)+10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Trampoline(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/trampoline.png')
        self.image = pg.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BoostRight(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/rightboost.png')
        self.image = pg.transform.scale(img, ((tile_size // 2)+10, (tile_size // 2)+10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Hearts():
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.imglist = []
        for i in range(1,7):
            IMG = pg.image.load(f'hearts/heart{i}.png')
            #IMG = IMG.inflate(100,100)
            IMG = pg.transform.scale(IMG, (IMG.get_width()*4,IMG.get_height()*4))
            
            self.imglist.append(IMG)

class Bone(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('dino/bone.png')
        self.image = pg.transform.scale(img, ((tile_size // 2)+10, (tile_size // 2)+10))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
class PortalDoor(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/portal.png')
        self.image = pg.transform.scale(img, (tile_size, int(tile_size*1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class World():
    def __init__(self, data):
        self.tile_list = []
        #load images
        dirt = pg.image.load('img/dirt.png')
        grass = pg.image.load('img/grass.png')
        specgrass = pg.image.load('img/specgrass.png')
        stone = pg.image.load('img/stone.png')

        # reads level data and loads into world tiles
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # for each number in level data, add tile to world
                if tile == 1:
                    img = pg.transform.scale(dirt, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pg.transform.scale(grass, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3: 
                    spider = Spider(col_count * tile_size, row_count * tile_size + 15)
                    spider_group.add(spider)
                if tile == 4:
                    lava = Lava(col_count * tile_size, row_count * tile_size+15)
                    lava_group.add(lava)
                if tile == 5:
                    bone = Bone(col_count * tile_size +(tile_size//2), row_count * tile_size + (tile_size//2))
                    bone_group.add(bone)
                if tile == 6:
                    exit = PortalDoor(col_count * tile_size, row_count *tile_size - (tile_size // 2))
                    PortalDoor_group.add(exit)
                if tile == 7:
                    img = pg.transform.scale(specgrass, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 8:
                    img = pg.transform.scale(stone, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 9:
                    deeplava = DeepLava(col_count * tile_size, row_count * tile_size)
                    deeplava_group.add(deeplava)
                if tile == 10:
                    # boost image
                    jump = BoostUp(col_count * tile_size, row_count * tile_size)
                    JumpBoost_group.add(jump)
                if tile == 11:
                    # trampoline image
                    trampoline = Trampoline(col_count * tile_size, row_count * tile_size)
                    Trampoline_group.add(trampoline)
                if tile == 12:
                    # boost image
                    right = BoostRight(col_count * tile_size, row_count * tile_size)
                    JumpBoost_group.add(right)

                col_count += 1
            row_count += 1


    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pg.draw.rect(screen, (255,255,255), tile[1], 2)

# etc
DeathQuotes = ["You just had a close encounter of the dead kind.",
    "Your platforming skills need a little work. Like, a lot of work.",
    "You're not good at jumping, but you're really good at falling.",
    "Looks like you're taking a nap.",
    "You have now joined the ranks of the fallen platformers.",
    "Another one bites the dust. Or, in your case, another one bites the pixelated platforms.",
    "You fell for it. Literally.",
    "Your lack of jumping ability is impressive. In a bad way.",
    "Oops, you fell for the oldest trick in the platforming book.",
    "Looks like you're going to need a lot more lives to beat this game.",
    "Gravity always wins, my friend.",
    "Better luck next respawn!",
    "If at first you don't succeed, respawn and try again.",
    "Looks like you need to work on your landing strategy.",
    "Ready to give it another go, champ? Death didn't keep you down for long!",
    "Get back in the game and show those obstacles who's boss!",
    "Back in the saddle again! Let's hope death learned its lesson this time.",
    "Death may have taken you down, but it can't keep a good player down!",
    "They say what doesn't kill you makes you stronger. Let's hope that's true for you!",
    "The respawn button is your friend. Don't be afraid to use it!",
    "Time to brush off the dirt and get back in the game. You got this!",
    "Death may have gotten the best of you before, but this time you're coming back stronger than ever!",
    "It's not how many times you fall, it's how many times you get back up. You're a fighter!",
    "The game isn't over until you say it is. So let's get back to it!",
    "You've got the jumping skills of a potato.",
    "You're really good at dying.",
    "Don't worry, death is just a minor setback.", 
    "Not going right? Go left."
    "You're back in the game. Let's hope you're ready for round two!"]

LoadingScreenTips = ['Trampolines negate fall damage!', "Don't forget to breathe.", "Never underestimate the power of a well-timed double jump.", "Don't worry if you fall down. The important thing is getting back up.", "Always be on the lookout for hidden secrets.", "If you're feeling stuck, try changing up your strategy.", "Don't be afraid to get a little creative.", "Sometimes the best way to beat a level is to think outside the box.", "Don't be afraid to take a break. Stretch your legs, get some fresh air."]

#entites

lava_group = pg.sprite.Group()
deeplava_group = pg.sprite.Group()
spider_group = pg.sprite.Group()
bone_group = pg.sprite.Group()
PortalDoor_group = pg.sprite.Group()
JumpBoost_group = pg.sprite.Group()
Trampoline_group = pg.sprite.Group()
player = Player(190, height - 130)

RightBoost_group = pg.sprite.Group()
level = 0
# load first level
if path.exists(f'levels/level{level}_data'):
	level_data = open(f'levels/level{level}_data', 'rb')
	world_data = pickle.load(level_data)
world = World(world_data)
heart = Hearts()

# Buttons
restart = Button(width //2 - 150, height //2+100, restart_IMG)
start = Button(width //2 - 100, height //2 -200, start_IMG)
controls = Button(width //2 - 200, height //2 +100, HowToPlay_IMG)
levelselect = Button(width //2 - 200, height //2 -50, levelselect_IMG)
begin = Button(width //2 - 100, height //2 , begin_IMG)
settings = Button(width-75,0, settings_IMG)
menu = Button(width //2 - 375, height //2 +350, menu_IMG)
next2 = Button(width //2 + 275, height //2 +350, smallnext_IMG)
load = Button(width //2 -50, height // 2+160, load_img)
exit = Button(width //2 - 100, height //2 +250, exit_IMG)
exit2 = Button(width //2 + 50, height //2+100, exit2_IMG)
next_level = Button(width //2 -50, height //2+325, next_IMG)
doublejump_btn = Button(width //2 -325, height //2-200, doublejump_IMG1)
extralife_btn = Button(width //2 + 50, height //2-200, extralife_IMG1)
closegame = Button(width //2  - 150, height //2, exitgame)

userfont = pg.font.SysFont('Courier Regular', 93)
username =''
code = ''
difficulty_text = 'Difficulty: Easy'
difficulty_text = font.render(difficulty_text, True, WHITE)

active = False
NameInput_rect = pg.Rect(width//2-200, height //2 - 100 , 500, 80)
CodeInput_rect = pg.Rect(width//2-200, height //2 , 500, 80)

difficulty_options = ['Difficulty: Easy', 'Difficulty: Medium', 'Difficulty: Hard']
selected_difficulty = 0
music_toggle = False
sound_toggle = False



def InvalidCode():
    running = True
    i = 0
    while running:
    
        if i <= 5000:
            i += 1
            print_text("Invalid Code ", font, MINTBLUE, (width//2)-250,(height//2)-250)
            pg.display.flip()
        if i == 5000:    
            running = False

def test():
    running = True
    i = 0
    while running:
    
        if i <= 10000:
            i += 1
            pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
            print_text("To double jump, press space while in the air", font, MINTBLUE, (width//2)-350,(height//2)-250)
        if i == 10000:    
            running = False

doublejumpscreen = False
# start game loop
running = True
while running:
    #set FPS and display background/sun
    screen.fill((224, 176, 255))
    clock.tick(fps)
    screen.blit(BG, (0,0))
    screen.blit(SUN, (25,50))
    #show start menu when starting 
    if StartMenu == 1:
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        print_text("Welcome To Dino Dash!", font, MINTBLUE, (width//2)-350,(height//2)-300)
        
        #if buttons are pressed
        if start.draw():
            StartMenu = 1.1
            time.sleep(0.1)
        if exit.draw():
            running = False
        if settings.draw():
            StartMenu = 4 
            time.sleep(0.1)

        if controls.draw():
            StartMenu = 3
            time.sleep(0.1)
        if  levelselect.draw():
            StartMenu = 5
            time.sleep(0.1)

    elif StartMenu == 1.1:
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        print_text("Enter Your Name:", font, MINTBLUE, (width//2)-240,(height//2)-200)
        if active:
            color = activegreen
        else:
            color = notactivegreen

        #if buttons are pressed

        pg.draw.rect(screen, color, NameInput_rect)
        text = userfont.render(username, True, GOLD)
        screen.blit(text, (NameInput_rect.x+5, NameInput_rect.y+10))
        NameInput_rect.w = max(450, 10)

        if begin.draw():
            StartMenu = 0
            if username == '':
                username = 'You'
            start_point = pg.time.get_ticks()         
            loadingscreen = True
            num = random.randint(0,6)
            loadingIMG = loadingIMGS[num]
            tip = random.choice(LoadingScreenTips)

        if menu.draw():
            StartMenu = 1
            time.sleep(0.1)

        pg.display.flip()

    elif StartMenu == 3:
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        print_text("The Basics", font, MINTBLUE, (width//2)-180,15)
        print_text("Use WAD or the arrow keys to move your character!", scorefont,GOLD, (width//2)-350,(height//2)-300)
        print_text("OR", font, BLACK, (width//2)-50,(height//2)+50)
        screen.blit(arrows, (500, 400))
        screen.blit(keys, (53, 400))
        if menu.draw():
            StartMenu = 1
            time.sleep(0.1) 
        if next2.draw():
            StartMenu = 3.1
            time.sleep(0.1)
            
    elif StartMenu == 3.1:
        i = 1
        healthBar_length = int(10 / 10 * healthBar_width)
        healtharrow = pg.transform.rotate(downarrow, 215)
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        pg.draw.rect(screen, (224, 176, 245),pg.Rect(0, 625, width, screenspace + 10))
        print_text("The Basics", font, MINTBLUE, (width//2)-180,15)
        print_text("Use WAD or the arrow keys to move your character!", scorefont, MINTBLUE, (width//2)-350,(height//2)-300)
        print_text("OR", font, BLACK, (width//2)-50,(height//2)+50)
        print_text("Your health resets each time you die,", scorefont, GOLD, (width//2)-240,160)
        print_text("avoid enemies, hazards, and fall damage!", scorefont, GOLD, (width//2)-270,185)
        pg.draw.rect(screen, BLACK, (healthBar_x-2, 643, healthBar_length+4, healthBar_height+4))
        pg.draw.rect(screen, GREEN, (healthBar_x, 645, healthBar_length, healthBar_height))
        screen.blit(healtharrow, (205, 665))
        screen.blit(arrows, (500, 400))
        screen.blit(keys, (53, 400))
        if menu.draw():
            StartMenu = 1
            time.sleep(0.1)
        if next2.draw():
            StartMenu = 3.2
            time.sleep(0.1)
       
    elif StartMenu == 3.2: 
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        pg.draw.rect(screen, (224, 176, 255),pg.Rect(0, 625, width, screenspace + 10))
        livesarrow = pg.transform.rotate(downarrow, 180)

        print_text("The Basics", font, MINTBLUE, (width//2)-180,15)
        print_text("Use WAD or the arrow keys to move your character!", scorefont, MINTBLUE, (width//2)-350,(height//2)-300)        
        print_text("OR", font, BLACK, (width//2)-50,(height//2)+50)
        print_text("Your health resets each time you die,", scorefont, MINTBLUE, (width//2)-240,160)
        print_text("avoid enemies, hazards, and fall damage!", scorefont, MINTBLUE, (width//2)-270,185)
        print_text("Hearts display your remaining lives.", scorefont, GOLD, (width//2)-250,220)
        print_text("Once they're gone, it's game over!", scorefont, GOLD, (width//2)-240,250)
        pg.draw.rect(screen, BLACK, (healthBar_x-2, 643, healthBar_length+4, healthBar_height+4))
        pg.draw.rect(screen, GREEN, (healthBar_x, 645, healthBar_length, healthBar_height))
    
        screen.blit(livesarrow, (383, 700))
        screen.blit(arrows, (500, 400))
        screen.blit(keys, (53, 400))
        screen.blit(heart.imglist[4], (width//2-heart.imglist[4].get_width()//2,640))
        if menu.draw():
            StartMenu = 1
            time.sleep(0.1)
        if next2.draw():
            StartMenu = 3.3
            time.sleep(0.1) 

    elif StartMenu == 3.3:
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        pg.draw.rect(screen, (224, 176, 255),pg.Rect(0, 625, width, screenspace + 10))
        bonearrow = pg.transform.rotate(downarrow, 135)

        print_text("The Basics", font, MINTBLUE, (width//2)-180,15)
        print_text("Use WAD or the arrow keys to move your character!", scorefont, MINTBLUE, (width//2)-350,(height//2)-300)
        print_text("OR", font, BLACK, (width//2)-50,(height//2)+50)
        print_text("Your health resets each time you die,", scorefont, MINTBLUE, (width//2)-240,160)
        print_text("avoid enemies, hazards, and fall damage!", scorefont, MINTBLUE, (width//2)-270,185)
        print_text("Hearts display your remaining lives.", scorefont, MINTBLUE, (width//2)-250,220)
        print_text("Once they're gone, it's game over!", scorefont, MINTBLUE, (width//2)-240,250)
        print_text("Collect Bones to purchase lives and upgrades!", scorefont, GOLD, (width//2)-300,280)
        pg.draw.rect(screen, BLACK, (healthBar_x-2, 643, healthBar_length+4, healthBar_height+4))
        pg.draw.rect(screen, GREEN, (healthBar_x, 645, healthBar_length, healthBar_height))
        print_text('10 X', scorefont, BLACK, 670,645)
        screen.blit(bonearrow, (620, 665))
        screen.blit(bone_IMG, (730,640))
        screen.blit(arrows, (500, 400))
        screen.blit(keys, (53, 400))
        screen.blit(heart.imglist[4], (width//2-heart.imglist[4].get_width()//2,640))
        if menu.draw():
            StartMenu = 1
            time.sleep(0.1) 
        if next2.draw():
            StartMenu = 3.4
            time.sleep(0.1)

    elif StartMenu == 3.4:
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        print_text("Item Shop", font, MINTBLUE, (width//2)-150,15)
        print_text("Here is where you can purchase ", scorefont, MINTBLUE, (width//2)-240,(height//2)-300)
        print_text("character upgrades and abilites! ", scorefont, MINTBLUE, (width//2)-240,(height//2)-260)
        if menu.draw():
            StartMenu = 1
        if next2.draw():
            StartMenu = 3.5

    elif StartMenu == 4:
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        print_text("Game Settings", font, MINTBLUE, (width//2)-240,15)
        

        #difficulty level selction
        difficulty = userfont.render(difficulty_options[selected_difficulty], True, MINTBLUE)
        difficulty_rect = difficulty.get_rect()
        difficulty_rect.topleft = (150,200)
        screen.blit(difficulty, (150,200))
        pg.draw.rect(screen, (255,255,255), difficulty_rect, 1)
        if selected_difficulty == 0:
            health = EasyHealth
            lives = EasyLives
            SelectedHealth = EasyHealth
        if selected_difficulty == 1:
            health = MediumHealth
            lives = MediumLives
            SelectedHealth = MediumHealth
        if selected_difficulty == 2:
            health = HardHealth
            lives = HardLives
            SelectedHealth = HardHealth
        
        
        if menu.draw():
            StartMenu = 1  
        pg.display.flip()

    elif StartMenu == 5:
        pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
        print_text("Level Selection", font, MINTBLUE, (width//2)-240,15)
        if active:
            color = activegreen
        else:
            color = notactivegreen

        # code input box
        pg.draw.rect(screen, color, CodeInput_rect)
        text = userfont.render(code, True, GOLD)
        screen.blit(text, (CodeInput_rect.x+5, CodeInput_rect.y+10))
        CodeInput_rect.w = max(450, 10)
        if menu.draw():
            StartMenu = 1  
        if load.draw():
            if path.exists(f'levels/level{code}_data'):
                world = reset_level(code)
                level_data = open(f'levels/level{code}_data', 'rb')
                world_data = pickle.load(level_data)
                StartMenu = 0
                start_point = pg.time.get_ticks()         
                loadingscreen = True
                level = int(code)
                num = random.randint(0,6)
                loadingIMG = loadingIMGS[num]
                tip = random.choice(LoadingScreenTips)

            else:
                InvalidCode()

        
        pg.display.flip()

    elif StartMenu == 0 and loadingscreen == False: 
        world.draw()

        healthBar_length = int(health / 10 * healthBar_width)
                
        if health > 0:
            spider_group.update()
            
            if lives == 1:

                screen.blit(heart.imglist[0], (width//2-heart.imglist[0].get_width()//2,810))
            elif lives == 2:
                screen.blit(heart.imglist[1], (width//2-heart.imglist[1].get_width()//2,810))
            elif lives == 3:
                screen.blit(heart.imglist[2], (width//2-heart.imglist[2].get_width()//2,810))
            elif lives == 4:
                screen.blit(heart.imglist[3], (width//2-heart.imglist[3].get_width()//2,810))
            elif lives == 5:
                screen.blit(heart.imglist[4], (width//2-heart.imglist[4].get_width()//2,810))
            elif lives == 6:               
                screen.blit(heart.imglist[5], (width//2-heart.imglist[5].get_width()//2,810))

            pg.draw.rect(screen, BLACK, (healthBar_x-4, healthBar_y-4, healthBar_width+8, healthBar_height+8))
            pg.draw.rect(screen, WHITE, (healthBar_x-2, healthBar_y-2, healthBar_length+4, healthBar_height+4))


            #display health counter
            if health > 7:
                    pg.draw.rect(screen, GREEN, (healthBar_x, healthBar_y, healthBar_length, healthBar_height))
            elif health > 3:
                pg.draw.rect(screen, YELLOW, (healthBar_x, healthBar_y, healthBar_length, healthBar_height))
            else:
                pg.draw.rect(screen, RED, ((healthBar_x, healthBar_y, healthBar_length, healthBar_height)))

            #print_text(f"Health: {health}", scorefont, BLACK, (width//2)+270,810)

            if pg.sprite.spritecollide(player, bone_group, True):
                bone_count += 1
                total_bone_count += 1
            # display bone counter
            print_text(f"{bone_count} X", scorefont, BLACK, 695, 815)
            screen.blit(bone_IMG, (750,810))

        #draw position of all sprites and update player health
        
        spider_group.draw(screen)
        lava_group.draw(screen)
        deeplava_group.draw(screen)
        JumpBoost_group.draw(screen)
        Trampoline_group.draw(screen)
        PortalDoor_group.draw(screen)
        bone_group.draw(screen)
        health = player.update(health)

        # if player dies
        if health <= 0 and health != -10:

            pg.draw.rect(screen, (112, 41, 99),pg.Rect(0, 0, width, height))
            screen.blit(deaddino, ((width//2)-150,(height//2)+150))
            
            #display death quotes and buttons
            print_text(f"{username} Died.", font, RED, (width//2)-150,(height//2))
            quote = DeathQuotes[player.deathnum]
            font1 = pg.font.Font(None, 30)
            text = font1.render(quote, True, YELLOW)
            text_rect = text.get_rect(center=(width//2, height//2-50))

            screen.blit(text, text_rect)
            
            if restart.draw():
                level -= 1
                world = reset_level(level)
                if SelectedHealth == 0:
                    health = 10
                if bone_count >= 2:
                    bone_count -= 2
                lives -= 1
                start_point = pg.time.get_ticks()         
                loadingscreen = True
                num = random.randint(0,6)
                loadingIMG = loadingIMGS[num]
            if exit2.draw():
                running = False

        # if player completes level
        if health == -10:
            tip = random.choice(LoadingScreenTips)

            if level == 0:
                screen.blit(shopBG, (0,0))
                print_text("Welcome to the ", font, store_color, (width//2)-230,10)
                print_text("Item Shop!", font, store_color, (width//2)-150,60)
                print_text("Click To Purchase", font, store_color, (width//2)-275,(height-160))
                print_text("Character Upgrades!", font, store_color, (width//2)-320,(height-100))
                print_text(f"You have {bone_count} bones.", scorefont, WHITE, (width//2)-120,(height-190))
                if bone_count >= 5 and doublejumpbought == False:
                    doublejump_btn.image = doublejump_IMG
                    if doublejump_btn.draw():
                        candoublejump = True
                        doublejump_btn.image = doublejump_IMG2
                        if doublejumpbought == False:
                             bone_count -= 5
                             doublejumpbought = True
                             doublejumpscreen = True
                elif doublejumpbought == True:
                    doublejump_btn.image =  doublejump_IMG2
                    doublejump_btn.draw()
                else:
                    doublejump_btn.image = doublejump_IMG1
                    if doublejump_btn.draw():
                        pass

                if bone_count >= 15 and lives < 6:
                    extralife_btn.image = extralife_IMG
                    if extralife_btn.draw():
                        extralife_btn.image = extralife_IMG2
                        if lives < 6:
                             bone_count -= 15
                             lives += 1
                elif lives == 6:
                    extralife_btn.image =  extralife_IMG2
                    extralife_btn.draw()
                else:
                    extralife_btn.image = extralife_IMG1
                    if extralife_btn.draw():
                        pass

                if next_level.draw():
                    if doublejumpscreen == True:
                        pass

                    # reset game and go to next level
                    level += 1
                    if level <= max_level:
                        # reset level
                        world_data = []
                        world = reset_level(level)
                        if SelectedHealth == 0:
                            health = 10
                        else:
                            health = SelectedHealth
                        start_point = pg.time.get_ticks()         
                        loadingscreen = True
                        num = random.randint(0,6)
                        loadingIMG = loadingIMGS[num]

            if level != max_level:
                screen.blit(shopBG, (0,0))
                print_text(f"Welcome Back", font, WHITE, (width//2)-225,13)
                print_text(f"{username}", font, WHITE, (width//2)-155,63)
                print_text(f"You have {bone_count} bones.", scorefont, WHITE, (width//2)-123,(height-188))

                print_text(f"Welcome Back", font, store_color, (width//2)-220,10)
                print_text(f"{username}", font, store_color, (width//2)-150,60)
                print_text(f"You have {bone_count} bones.", scorefont, store_color, (width//2)-120,(height-190))

                if bone_count >= 5 and doublejumpbought == False:
                    doublejump_btn.image = doublejump_IMG
                    if doublejump_btn.draw():
                        candoublejump = True
                        doublejump_btn.image = doublejump_IMG2
                        if doublejumpbought == False:
                                bone_count -= 5
                                doublejumpbought = True
                                doublejumpscreen = True

                elif doublejumpbought == True:
                    doublejump_btn.image =  doublejump_IMG2
                    doublejump_btn.draw()
                else:
                    doublejump_btn.image = doublejump_IMG1
                    if doublejump_btn.draw():
                        pass

                if bone_count >= 15 and lives < 6:
                    extralife_btn.image = extralife_IMG
                    if extralife_btn.draw():
                        extralife_btn.image = extralife_IMG2
                        if lives < 6:
                             bone_count -= 15
                             lives += 1
                elif lives == 6:
                    extralife_btn.image =  extralife_IMG2
                    extralife_btn.draw()
                else:
                    extralife_btn.image = extralife_IMG1
                    if extralife_btn.draw():
                        pass

                if next_level.draw() and doublejumpscreen == False:
                    if doublejumpscreen == True:
                        pass
                    # reset game and go to next level
                    level += 1
                    if level <= max_level:
                        # reset level
                        world_data = []
                        world = reset_level(level)
                        if SelectedHealth == 0:
                            health = 10
                        else:
                            health = SelectedHealth
                        start_point = pg.time.get_ticks()         
                        loadingscreen = True
                        num = random.randint(0,6)
                        loadingIMG = loadingIMGS[num]

            


            if level == max_level:
                pg.draw.rect(screen, MINTGREEN,pg.Rect(0, 0, width, height))
                print_text("Wait.. you won?", font, MINTBLUE, (width//2)-210,(height//2)-100)
                print_text("What Want A Cookie?", font, MINTBLUE, (width//2)-320,(height//2))
                print_text(f" You earned {total_bone_count} bones!", gameoverfont, RED, (width//2)-400,(height//2)-200)
                if restart.draw():
                    StartMenu = 1
                    time.sleep(0.5)
                if exit2.draw():
                    running = False


                        
        if lives <= 0:
            #display game over
            pg.draw.rect(screen, (112, 41, 99),pg.Rect(0, 0, width, height))
            screen.blit(deaddino, ((width//2)-150,(height//2)+150))

            #display death quotes and buttons
            print_text("Game over, man. Game over.", gameoverfont, RED, (width//2)-250,(height//2)-350)
            print_text(f"{username}", gameoverfont, RED, (width//2)-270,(height//2)-270)
            print_text(f" You earned {total_bone_count} bones!", gameoverfont, RED, (width//2)-400,(height//2)-200)
            if closegame.draw():
                running = False
                

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        #user event that allows for player damage cooldown
        if event.type == hit_cooldown:
            player.cooldown = False

        if event.type == pg.MOUSEBUTTONDOWN and StartMenu == 2:
            if NameInput_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pg.MOUSEBUTTONDOWN and StartMenu == 5:
            if CodeInput_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pg.MOUSEBUTTONDOWN and StartMenu == 4:
            if difficulty_rect.collidepoint(event.pos):
                selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
            else:
                pass
        if event.type == pg.KEYDOWN and len(code) < 14:
            # Check for backspace
            if event.key == pg.K_BACKSPACE and StartMenu == 5:
  
                code = code[:-1]

            elif active == True and len(code) < 13 and StartMenu == 5 and event.key != pg.K_RETURN:
                code += event.unicode

        if event.type == pg.KEYDOWN and len(username) < 14:
            # Check for backspace
            if event.key == pg.K_BACKSPACE and StartMenu == 2:
  
                username = username[:-1]

            elif active == True and len(username) < 13 and StartMenu == 2 and event.key != pg.K_RETURN:
                username += event.unicode


    current_time = pg.time.get_ticks()         
    if current_time - start_point < loadingscreentimer and loadingscreen == True and level != max_level:
        screen.blit(loadingIMG,(0,0))
        font1 = pg.font.Font(None, 30)
        text = font1.render(tip, True, YELLOW)
        text_rect = text.get_rect(center=(width//2, height//2-50))

        screen.blit(text, text_rect)
        progress += 1
        if num == 1:
            print_text(f"Level {level}", gameoverfont, RED, (width//2)-250,(height//2)-350)
        else:
            print_text(f"Level {level}", gameoverfont, RED, (width//2)-250,(height//2)-350)
            

        progress_width = progress / max_progress * loadingBar_width
        pg.draw.rect(screen, BLACK, (loadingBar_x, loadingBar_y, 500, loadingBar_height))
        pg.draw.rect(screen, loadingBar_color, (loadingBar_x, loadingBar_y, progress_width, loadingBar_height))
        
    if current_time - start_point > loadingscreentimer:
        loadingscreen = False
        progress = 0
#    print(current_time)

    if current_time > 50000:
        running = False
    pg.draw.line(screen, (220, 240, 239), (width/2, 0), (width/2, height), 2)

    pg.display.update()
    
pg.quit()
