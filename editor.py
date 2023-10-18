import pygame as pg
import pickle
from os import path

pg.init()
clock = pg.time.Clock()

fps = 60

tile_size = 40
cols = 20
screenspace = 100
width = tile_size * cols
height = (tile_size * cols) + screenspace
screen = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption('Capstone Editor')

BG = pg.image.load('img/BG.jpg')
BG = pg.transform.scale(BG, (width, height - screenspace))

#loads images for tiles
dirt = pg.image.load('img/dirt.png')
grass = pg.image.load('img/grass.png')
spider = pg.image.load('enemy/tile001.png')
specgrass = pg.image.load('img/specgrass.png')
stone = pg.image.load('img/stone.png')
lavablock = pg.image.load('img/deeplava.png')
lava_img = pg.image.load('img/lava.png')
bone = pg.image.load('dino/bone.png')
exit_img = pg.image.load('img/portal.png')
save_img = pg.image.load('img/save_btn.png')
load_img = pg.image.load('img/load_btn.png')
boost_img = pg.image.load('img/jumpboost.png')
boostright_img = pg.transform.rotate(pg.image.load('img/jumpboost.png'), 270)
boostleft_img = pg.transform.rotate(pg.image.load('img/jumpboost.png'), 90)
cake_img = pg.image.load('img/cake.png')
trampoline = pg.image.load('img/trampoline.png')
platform_img = pg.image.load('img/platform.png')
flyingenemy_img = pg.image.load('enemy/ghost.png')
rainbow = pg.image.load('img/rainbowstar.png')
doubleBones = pg.image.load('img/doublebones.png')
timestop = pg.image.load('img/timestop.png')
cactus = pg.image.load('enemy/cactus.png')
clicked = False
level = 0
black=(0,0,0)
MINTBLUE = (0,128,255)
font = pg.font.SysFont('Courier Regular', 93)

# creates empty world to load into
world_data = []
for row in range(20):
    r = [0] * 20
    world_data.append(r)



class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        click = False

        #get mouse position
        mouse = pg.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(mouse):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                click = True
                self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return click

# print text function
def print_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

# draws grid on screen 
def draw_grid():
    for c in range(21):
        #vertical lines
        pg.draw.line(screen, black, (c * tile_size, 0), (c * tile_size, height - screenspace))
        #horizontal lines
        pg.draw.line(screen, black, (0, c * tile_size), (width, c * tile_size))

# changes each tile based on number of clicks
def draw_world():
    for row in range(20):
        for col in range(20):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    #dirt blocks
                    img = pg.transform.scale(dirt, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    #grass blocks
                    img = pg.transform.scale(grass, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    #enemy blocks
                    img = pg.transform.scale(spider, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 4:
                    #lava
                    img = pg.transform.scale(lava_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size ))
                if world_data[row][col] == 5:
                    #bone
                    img = pg.transform.scale(bone, (tile_size // 2, tile_size // 2))
                    screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
                if world_data[row][col] == 6:
                    #portal
                    img = pg.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
                    screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
                if world_data[row][col] == 7:
                    #grass blocks
                    img = pg.transform.scale(specgrass, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 8:
                    #stone blocks
                    img = pg.transform.scale(stone, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 9:
                    # deep lava blocks
                    img = pg.transform.scale(lavablock, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 10:
                    # boost image
                    img = pg.transform.scale(boost_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 11:
                    # boost image
                    img = pg.transform.scale(trampoline, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 12:
                    # boost sprite
                    img = pg.transform.scale(boostright_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 13:
                    # boost sprite
                    img = pg.transform.scale(boostleft_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 14:
                    # boost sprite
                    img = pg.transform.scale(cake_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size)) 
                if world_data[row][col] == 15:
                    # boost sprite
                    img = pg.transform.scale(platform_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size)) 
                if world_data[row][col] == 16:
                    # boost sprite
                    img = pg.transform.scale(platform_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size)) 
                if world_data[row][col] == 17:
                    #enemy blocks
                    img = pg.transform.scale(flyingenemy_img, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 18:
                    #enemy blocks
                    img = pg.transform.scale(rainbow, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 19:
                    #enemy blocks
                    img = pg.transform.scale(doubleBones, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 20:      
                    #enemy blocks
                    img = pg.transform.scale(timestop, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 21:      
                    #enemy blocks
                    img = pg.transform.scale(cactus, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))

#create load and save buttons
SaveBtn = Button(width // 2 - 50, height - 80, save_img)
LoadBtn = Button(width // 2 + 150, height - 80, load_img)

#main game loop
running = True
tile_change_speed = 100
tile_change_timer = 0

while running:

    clock.tick(fps)

    #draw background
    screen.fill(black)
    screen.blit(BG, (0, 0))

    #load and save level
    if SaveBtn.draw():
        #save level data to level Y
        write = open(f'levels/level{level}_data', 'wb')
        pickle.dump(world_data, write)
        write.close()
    if LoadBtn.draw():
        #load in level data from level Y
        if path.exists(f'levels/level{level}_data'):
            load = open(f'levels/level{level}_data', 'rb')
            world_data = pickle.load(load)

    draw_grid()
    draw_world()

    print_text(f'Level: {level}', font, MINTBLUE, tile_size, height - 80)

    if pg.mouse.get_pressed()[0] == 1 or pg.mouse.get_pressed()[2] == 1:
        if pg.time.get_ticks() - tile_change_timer >= tile_change_speed:
            pos = pg.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size

            #check to make sure cursor is on tile
            if x < 20 and y < 20:
                # change tile value ie the tile 
                if pg.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 21:
                        world_data[y][x] = 0
                elif pg.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 21
            tile_change_timer = pg.time.get_ticks()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            pos = pg.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size

            if event.key == pg.K_w:
                for i in range(20):
                    world_data[i][x] += 1
                    if world_data[i][x] > 21:
                        world_data[i][x] = 0
            elif event.key == pg.K_s:
                for i in range(20):
                    world_data[i][x] -= 1
                    if world_data[i][x] < 0:
                        world_data[i][x] = 21
            elif event.key == pg.K_a:
                for i in range(20):
                    world_data[y][i] -= 1
                    if world_data[y][i] < 0:
                        world_data[y][i] = 21
            elif event.key == pg.K_d:
                for i in range(20):
                    world_data[y][i] += 1
                    if world_data[y][i] > 21:
                        world_data[y][i] = 0

    pg.display.update()

pg.quit()
