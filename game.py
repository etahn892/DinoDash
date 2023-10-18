import pygame as pg
from pygame import *
import random
import pickle
import os
from os import path
from dotenv import load_dotenv
import time
import smtplib
import ssl
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox, filedialog
from zipfile import ZipFile
import win32gui
import win32con
import math
import pyautogui
pyautogui.FAILSAFE = False

joysticks = []
deadzone = 0.2
MAX_FILE_SIZE = 5 * 1024 * 1024

pg.init()
pg.mixer.init()
screenspace = 60
height = 800 + screenspace
width = 800
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Dino Dash')
pg.display.set_icon(pg.image.load('img/icon.ico'))
clock = pg.time.Clock()

#get encrpyed password

load_dotenv('passwords.env')
password = os.environ.get('PASSWORD')
hwnd = pg.display.get_wm_info()["window"]
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

#game variables
tile_size = 40
fps = 60
health = 10

StartMenu = 1
max_level = 5
bone_count = 0
total_bone_count  = 0
inshop = False
died = False
current_time = 0
invincibiltyStart = 0
StopTimeStart = 0
DBStart = 0
start_point = 0
loadingscreen = False
loadingscreentimer = 1000
notshown = True
candoublejump = False
candinodash = False
doublejumpbought = False
dinodash = False
active = False
doublejumpscreen = False
paused = False
timeStop = False
gameover = False
gamewon = False
levelskip_count = 100
soundplaying = False

EasyDamage = 15
MediumDamage = 17
HardDamage = 5
SelectedDamage = 0 
damage = EasyDamage

EasyHealth = 150
EasyLives = 5
MediumHealth = 100
MediumLives = 4 
HardHealth = 10
HardLives = 1 
SelectedHealth = 0 
lives = EasyLives

# custom user events
hit_cooldown = pg.USEREVENT + 1

# load basic images
SUN = pg.transform.scale(pg.image.load('img/sun.png'), (200,200))
BG = pg.transform.scale(pg.image.load('img/BG.jpg'), (width, height-screenspace))
shopBG = pg.transform.scale(pg.image.load('img/shopbackground.png'), (width, height))
deaddino = pg.image.load('dino/dead.png')
restart_IMG = pg.image.load('img/restart_btn2.png')
HowToPlay_IMG = pg.transform.scale(pg.image.load('img/howtoplay.png'), (433,100))
levelselect_IMG = pg.transform.scale(pg.image.load('img/levelselect.png'), (433,100))
settings_IMG = pg.transform.scale(pg.image.load('img/settings_btn.png'), (75,75))
begin_IMG = pg.transform.scale(pg.image.load('img/begin_btn.png'), (200,100))
menu_IMG = pg.transform.scale(pg.image.load('img/menu_btn.png'), (100,50))
arrows = pg.transform.scale(pg.image.load('img/arrow.png'), (240,200))
downarrow = pg.image.load('img/downarrow.png')

keyboard = pg.transform.scale(pg.image.load('img/keyboard.png'), (600,226))
controller = pg.transform.scale(pg.image.load('img/controls.png'), (600,250))
start_IMG = pg.transform.scale(pg.image.load('img/start_btn.png'), (200,100))
exit_IMG = pg.transform.scale(pg.image.load('img/exit_btn.png'), (200,100))
exit2_IMG = pg.transform.scale(pg.image.load('img/exit_btn.png'), (76,40))
exitgame = pg.transform.scale(pg.image.load('img/exitgame.png'), (150,150))
next_IMG = pg.transform.scale(pg.image.load('img/nextlevel.png'), (125,66))
smallnext_IMG = pg.transform.scale(pg.image.load('img/nextlevel.png'), (100,50))
load_img = pg.transform.scale(pg.image.load('img/load_btn.png'), (100,50))
extralife_IMG1 = pg.transform.scale(pg.image.load('img/nopluslife.png'), (300,200))
extralife_IMG2 = pg.transform.scale(pg.image.load('img/maxpluslife.png'), (300,200))
extralife_IMG = pg.transform.scale(pg.image.load('img/pluslife.png'), (300,200))
doublejump_IMG1 = pg.transform.scale(pg.image.load('img/nodoublejump.png'), (300,200))
doublejump_IMG2 = pg.transform.scale(pg.image.load('img/doublejumpbought.png'), (300,200))
doublejump_IMG = pg.transform.scale(pg.image.load('img/doublejump.png'), (300,200))
levelskip_IMG = pg.transform.scale(pg.image.load('img/levelskip.png'), (300,200))
levelskip_IMG1 = pg.transform.scale(pg.image.load('img/nolevelskip.png'), (300,200))
skip_IMG = pg.transform.scale(pg.image.load('img/skip.png'), (60,60))
dinodash_IMG = pg.transform.scale(pg.image.load('img/dinodash.png'), (300,200))
dinodash_IMG1 = pg.transform.scale(pg.image.load('img/nodinodash.png'), (300,200))
dinodash_IMG2 = pg.transform.scale(pg.image.load('img/boughtdinodash.png'), (300,200))
bone_IMG= pg.transform.scale(pg.image.load('dino/bone.png'), ((tile_size // 2)+10, (tile_size // 2)+10))
back_IMG = pg.transform.scale(pg.image.load('img/back_btn.png'), (100,50))
feedback_IMG = pg.transform.scale(pg.image.load('img/feedback.png'), (300,70))
iceFilter = pg.transform.scale(pg.image.load('img/freeze.jpg'), (width, height-screenspace))
iceFilter.set_alpha(100)
doublebone_IMG = pg.transform.scale(pg.image.load('img/doublebones.png'), ((tile_size // 2)+15, (tile_size // 2)+15))

loadingIMGS = []
for i in range(1,8):
    img = pg.image.load(f'loading/loadingscreen{i}.png')
    img = pg.transform.scale(img, (width, height))
    img = loadingIMGS.append(img)

highscorefile = open('levels/highscore.txt', 'r')
highscore = float(highscorefile.readline())
score = 0
totalscore = 0
sender = 'dinodashewilson@gmail.com'
receiver = 'ethan8902@gmail.com'
subject = ''
body = ''
username =''
feedback = ''

# font settings
WHITE = (255,255,255)
RED = (255,0,0)
GRAY = (96,96,96)
notactivepurple =  (206,194,255)
activepurple = (180,51,255)
DEEPPURPLE = (25,22,39)
SILVER = (216,226,220)
GOLD = (216,226,220)
store_color = (127,112,195)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
font = pg.font.SysFont('Courier Regular', 93)
gameoverfont = pg.font.SysFont('Bauhaus 93', 70)
userfont = pg.font.SysFont('Courier Regular', 93)
feedbackfont = pg.font.SysFont('Courier Regular', 27)
boughtfont = pg.font.SysFont('Courier Regular', 30)
scorefont = pg.font.SysFont('Courier Regular', 40)

difficulty_text = 'Difficulty: Easy'
difficulty_text = font.render(difficulty_text, True, WHITE)
difficulty_options = ['Difficulty: Effortless', 'Difficulty: Moderate', 'Difficulty: Ruthless']
selected_difficulty = 0

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

# Input Boxes
NameInput_rect = pg.Rect(width//2-225, height //2 -100, 500, 80)
CodeInput_rect = pg.Rect(width//2-225, height //2 -100, 500, 80)
Feedback_rect = pg.Rect(width//2-200, height //2 -100, 500, 350)
Subject_rect = pg.Rect(width//2-200, height //2 -200, 500, 80)


# etc
DeathQuotes = ["You just had a encounter of the dead kind.", "Your platforming skills need a little work. Like, a lot of work.", "You're not good at jumping, but you're really good at falling.", "Looks like you're taking a nap.", "You have now joined the ranks of the fallen platformers.", "Another one bites the dust.", "You fell for it. Literally.", "Your lack of jumping ability is impressive. In a bad way.", "Oops, you fell for the oldest trick in the platforming book.", "Looks like you're going to need a lot more lives to beat this game.", "Gravity always wins, my friend.", "Better luck next respawn!", "If at first you don't succeed, respawn and try again.", "Looks like you need to work on your landing strategy.", "Ready to give it another go, champ? Death didn't keep you down for long!", "Get back in the game and show those obstacles who's boss!", "Back in the saddle again! Let's hope death learned its lesson this time.", "Death may have taken you down, but it can't keep a good player down!", "They say what doesn't kill you makes you stronger. Cept you just died.", "The restart button is your friend. Don't be afraid to use it!", "Time to brush off the dirt and get back in the game. You got this!", "Death got the best of you, unacceptable.", "The game isn't over until you say it is. So let's get back to it!", "You've got the jumping skills of a potato.", "You're really good at dying.", "Don't worry, death is just a minor setback.",  "Not going right? Go left.", "You're back in the game. Let's hope you're ready for round two!"]
LoadingScreenTips = ['Trampolines negate fall damage!', "Don't forget to breathe.", "Never underestimate the power of a well-timed double jump.", "Don't worry if you fall down. The important thing is getting back up.", "Always be on the lookout for hidden secrets.", "If you're feeling stuck, try changing up your strategy.", "Don't be afraid to get a little creative.", "Sometimes the best way to beat a level is to think outside the box.", "Don't be afraid to take a break. Stretch your legs, get some fresh air."]
RAINBOW = [(255, 0, 0), (255, 69, 0), (255, 140, 0), (255, 215, 0), (255, 255, 0), (173, 255, 47),            (0, 255, 0), (0, 250, 154), (0, 255, 255), (0, 191, 255), (0, 0, 255), (138, 43, 226),            (148, 0, 211), (255, 0, 255), (255, 20, 147), (255, 69, 0), (255, 140, 0), (255, 215, 0),            (255, 255, 0), (255, 0, 0), (128, 0, 128), (0, 128, 128), (128, 128, 0), (255, 165, 0),           (255, 99, 71), (218, 112, 214), (255, 182, 193), (188, 143, 143), (139, 69, 19), (0, 0, 128),           (0, 128, 0), (128, 0, 0), (0, 255, 127), (255, 215, 180), (176, 224, 230), (255, 192, 203)]

# sounds 
trampBounce_sound = pg.mixer.Sound("sound/jews_harp_boing-7111.mp3")
tramp_sound = pg.mixer.Sound("sound/trampoline.mp3")
jump_sound = pg.mixer.Sound("sound/jump.wav")
bone_sound = pg.mixer.Sound("sound/bone.wav")
hurt_sound = pg.mixer.Sound("sound/villager.mp3")
boost_sound = pg.mixer.Sound("sound/BoostLoop.mp3")
purchase_sound = pg.mixer.Sound("sound/lostbone.mp3")
boost_sound.set_volume(0.25)
background_music = pg.mixer.Sound("sound/background_music.mp3")
ate_sound = pg.mixer.Sound("sound/ate.mp3")
toggle_snd = pg.mixer.Sound("sound/toggle.wav")
warped_sound = pg.mixer.Sound("sound/warp.mp3")
tick_sound = pg.mixer.Sound("sound/tick.mp3")
invinc_sound = pg.mixer.Sound('sound/invincibilty.mp3')
doublebones_sound = pg.mixer.Sound('sound/doublebones.mp3')
timestop_sound = pg.mixer.Sound('sound/timefreeze.mp3')
dash_sound = pg.mixer.Sound('sound/dash.mp3')


sound_volume = 0.5
music_volume = 0.5
music_toggle = False
sound_toggle = False
pg.mixer.music.set_volume(music_volume)
sound_mode = "Sound: On"
music_mode = "Music: On"

# Read from previous attempt
with open('levels/futurelevelcodes.txt') as f:
    LevelCodes = {}
    for i, code in enumerate(f):
        code = code.strip()
        LevelCodes[code] = i

# Create random codes and its value as a level number
with open('levels/futurelevelcodes.txt', 'w') as f:
    codes = []
    FutureLevelCodes = {}
    for i in range(7):
        code = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=8))
        codes.append(code)
        FutureLevelCodes[code] = i
        f.write(f"{code}\n")
    code = ''

def toggle_sound():
    global sound_volume, sound_mode
    if sound_volume == 0:
        sound_volume = 0.5
        sound_mode = "Sound: On"
    else:
        sound_volume = 0
        sound_mode = "Sound: Off"
    
    jump_sound.set_volume(sound_volume)
    bone_sound.set_volume(sound_volume)
    hurt_sound.set_volume(sound_volume)
    tramp_sound.set_volume(sound_volume)
    trampBounce_sound.set_volume(sound_volume)
    boost_sound.set_volume(sound_volume)
    purchase_sound.set_volume(sound_volume)
    ate_sound.set_volume(sound_volume)
    toggle_snd.set_volume(sound_volume)
    warped_sound.set_volume(sound_volume)
    tick_sound.set_volume(sound_volume)
    invinc_sound.set_volume(sound_volume)
    doublebones_sound.set_volume(sound_volume)
    timestop_sound.set_volume(sound_volume)
    dash_sound.set_volume(sound_volume)


def toggle_music():
    global music_volume, music_mode
    if music_volume == 0:
        music_volume = 0.5
        music_mode = "Music: On"
    else:
        music_volume = 0
        music_mode = "Music: Off"
    pg.mixer.music.set_volume(music_volume)
    
def SendEmail(subject, body, attachment=None):

    # Set the subject and body of the email
    subject = str(subject)
    body = str(body)
    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.set_content(body)
    context = ssl.create_default_context()

    if attachment:
        if os.path.getsize(attachment) > MAX_FILE_SIZE:
            with ZipFile('compressed.zip', 'w') as zip_file:
                zip_file.write(attachment, os.path.basename(attachment))
            attachment = 'compressed.zip'
        with open(attachment, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment)
        message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
    except Exception as e:
        # Show an error message if the email fails to send
        messagebox.showerror('Error', f'Failed to send email: {e}')
    else:
        # Show a success message if the email is sent successfully
        messagebox.showinfo('Success', 'Email sent successfully!\nThanks for your feedback!')

def getFile(attachment_input):

    # Open a file dialog and get the selected file
    file_path = filedialog.askopenfilename()

    # Clear the attachment input field and set its value to the selected file
    attachment_input.delete(0, tk.END)
    attachment_input.insert(0, file_path)

def open_window():
    # create the window
    PURPLE = "#b433ff"
    GRAY = "#666666"
    TextColor = "#d8e2dc"
    window = tk.Tk()
    window.geometry("600x700")
    window.title("Feedback Submission")
    window.iconbitmap("img/icon.ico")
    window.configure(bg=GRAY)
    window.wm_attributes("-topmost", True)

    # change the background color
    subject_label = tk.Label(window, text="Subject:", font=("Courier Regular", 15), bg=GRAY, fg=TextColor)
    subject_label.pack(padx=40, pady=(40, 0))
    subject_input = tk.Entry(window, font=("Courier Regular", 15), bg=PURPLE, fg=TextColor, insertbackground=TextColor)
    subject_input.pack(fill=tk.X, expand=True, padx=40, pady=(5, 20))

    # create the body label and input field
    body_label = tk.Label(window, text="Message:", font=("Courier Regular", 15), bg=GRAY, fg=TextColor)
    body_label.pack(padx=40, pady=(20, 0))
    body_input_frame = tk.Frame(window)
    body_input_frame.pack(fill=tk.X, expand=True, padx=40, pady=(5, 10))
    body_input = tk.Text(body_input_frame, font=("Courier Regular", 15), height=10, width=30, wrap=tk.WORD, bg=PURPLE, fg=TextColor, insertbackground=TextColor)
    body_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # add a scrollbar to the body input field
    body_scrollbar = tk.Scrollbar(body_input_frame, troughcolor=PURPLE, bg=PURPLE, width=0)
    body_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    body_input.config(yscrollcommand=body_scrollbar.set)
    body_scrollbar.config(command=body_input.yview, highlightthickness=0)

    attachment_label = tk.Label(window, text="Attachment:", font=("Courier Regular", 15), bg=GRAY, fg=TextColor)
    attachment_label.pack(padx=40, pady=(10, 0))
    attachment_frame = tk.Frame(window, bg=GRAY, padx=40)
    attachment_frame.pack(fill=tk.X, expand=True, pady=(0, 20))
    attachment_input = tk.Entry(attachment_frame, font=("Courier Regular", 15), bg=PURPLE, fg=TextColor, insertbackground=TextColor)
    attachment_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
    attachment_button = tk.Button(attachment_frame, height=1,text="Browse", font=("Courier Regular", 15), bg=PURPLE, fg=TextColor, command=lambda: getFile(attachment_input))
    attachment_button.pack(side=tk.LEFT, padx=10)

    # create the submit button
    def submit():
        if not subject_input.get() or not body_input.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to send the message?")

        if confirm:
            # get the text from the subject and body fields
            subject = subject_input.get()
            body = body_input.get("1.0", tk.END)
            attachment = attachment_input.get()
            try:
                if attachment:
                    SendEmail(subject, body, attachment)
                else:
                    SendEmail(subject, body)
            except FileNotFoundError:
                # if the file is not found, show an error message to the user
                messagebox.showerror("Error", "File not found")
                return
            

            subject_input.delete(0, tk.END)
            body_input.delete("1.0", tk.END)
            attachment_input.delete(0, tk.END)

    submit_button = tk.Button(window, text="Submit", font=("Courier Regular", 15), command=submit, bg=PURPLE, fg=TextColor)
    submit_button.pack()

    spacer = tk.Label(window, height=1, bg=GRAY)
    spacer.pack(pady=20)

    # center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # start the window
    window.mainloop()

def InvalidCode():
    running = True
    i = 0
    while running:
    
        if i <= 5000:
            i += 1
            print_text("Invalid Code ", font, RED, (width//2)-200,(height//2)-200)
            pg.display.flip()
        if i == 5000:
            running = False

def HowToDoubleJump():
    floor = pg.transform.scale(pg.image.load('img/doublejumpscreen.png'), (width,280))
    spacebar = pg.transform.scale(pg.image.load('img/spacebar.png'), (200,50))
    pressedspace = pg.transform.scale(pg.image.load('img/pressedspace.png'), (200,50))
    ybutton = pg.transform.scale(pg.image.load('img/ybutton.png'), (60,60))
    pressedybutton = pg.transform.scale(pg.image.load('img/ybuttonpressed.png'), (60,60))
    BG = pg.transform.scale(pg.image.load('img/BG.jpg'), (width, height-screenspace))
    running = True
    i = 0
    y_loc = 580-player.height
    cnt = 0
    spacebarimg = spacebar
    y_img = ybutton
    while running:
        if i == 300:    
            i = 0
            y_loc = 580-player.height
            cnt += 1

        if cnt == 3:
            running = False

        if i <= 300:
            i += 1
            if i > 40 and i < 90:
                y_loc -= 2
            if i > 90 and i < 120:
                y_loc -= 1
            if i >130 and i < 150:
                y_loc += 1
                spacebarimg = pressedspace
                y_img = pressedybutton
                time.sleep(0.01)
            if i > 150 and i < 190:
                spacebarimg = spacebar
                y_img = ybutton
                y_loc -= 3

            if i > 190:
                if y_loc +player.height > 580:
                    y_loc = 580 - player.height
                else:
                    y_loc += 3
            
            screen.blit(BG, (0,0))
            screen.blit(spacebarimg, (300,300))
            screen.blit(y_img, (550,290))
            screen.blit(player.img_right[0], (150, y_loc))
            screen.blit(floor, (0,580))
            print_text("To double jump, press space or Y while in the air!", boughtfont, BLACK, (width//2)-200,(height//2)-178)
            print_text("To double jump, press space or Y while in the air!", boughtfont, WHITE, (width//2)-200,(height//2)-180)
            
            pg.display.flip()


def print_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def reset_level(level):
    player.reset(100, height - 150)
    spider_group.empty()
    lava_group.empty()
    PortalDoor_group.empty()
    deeplava_group.empty()
    BoostUp_group.empty()
    BoostRight_group.empty()
    BoostLeft_group.empty()
    Cake_group.empty()
    Trampoline_group.empty()
    bone_group.empty()
    Platform_group.empty()
    Ghost_group.empty()
    Invinc_group.empty()
    DB_group.empty()
    timeStop_group.empty()
    Cactus_group.empty()
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
            try:
                if (pg.mouse.get_pressed()[0] == 1 and self.clicked is False) or  joystick.get_button(1):
                    reset_game = True
                    self.clicked = True

            except:
                pass

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
        for i in range(0,50):
            n = random.uniform(3,6)
            randomlist.append(n)
        player_movement = random.choice(randomlist)
        if not health < -1:
            key = pg.key.get_pressed()
            joystick_moved = False
            if (key[pg.K_SPACE] and self.jumped==True and self.in_air is True and self.doublejump is False) and self.candoublejump:
                self.vel_y = -12
                self.doublejump = True

            if (key[pg.K_UP] and self.jumped is False) or (key[pg.K_w] and self.jumped is False):
                jumpheight = round(random.uniform(-8, -14.5), 3)
                self.vel_y = jumpheight
                self.jumped = True
                jump_sound.play()

            for joystick in joysticks:
                # check for joystick button inputs

                if (joystick.get_button(3) and self.jumped==True and self.in_air is True and self.doublejump is False) and self.candoublejump:
                    self.vel_y = -12
                    self.doublejump = True


                horizonal = joystick.get_axis(0)
                if not key[pg.K_LEFT] and not key[pg.K_a] and not key[pg.K_RIGHT] and not key[pg.K_d]:
                    dx = horizonal * player_movement

                if horizonal < 0 -deadzone or horizonal > 0 +deadzone:
                    self.counter += 1
                    self.index += 1
                    if self.index >= len(self.img_right):
                        self.index = 0
                if horizonal < 0 -deadzone:
                    self.direction =-1
                if horizonal > 0 +deadzone:
                    self.direction = 1
                if joystick.get_button(0) and self.jumped is False:
                    jumpheight = round(random.uniform(-8, -14.5), 3)
                    self.vel_y = jumpheight
                    self.jumped = True
                    jump_sound.play()

                if joystick.get_button(1) and self.can_dash and self.candinodash :
                    dash_distance = 150
                    dash_sound.play()
                    dx += self.direction * dash_distance
                    self.can_dash = False
                    self.dash_cooldown_timer = self.dash_cooldown

                
                if abs(horizonal) > deadzone:
                    self.counter += 1
                    if self.counter<6:
                        self.counter += 1


            if key[pg.K_LEFT] or key[pg.K_a]:
                dx -= player_movement
                self.counter += 1
                self.direction = -1

            if key[pg.K_f] and self.can_dash and self.candinodash :
                    dash_distance = 150
                    dash_sound.play()
                    dx += self.direction * dash_distance
                    self.can_dash = False
                    self.dash_cooldown_timer = self.dash_cooldown

            

            if key[pg.K_RIGHT] or key[pg.K_d]:
                dx += player_movement
                self.counter += 1
                self.direction = 1

            if (key[pg.K_LEFT] is False and key[pg.K_RIGHT] is False) and (key[pg.K_a] is False and key[pg.K_d] is False):    
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
                health -= SelectedDamage
                
            
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
                    dx =  0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) and self.on_platform is False :
                    
                    if self.vel_y == 20 and not self.invincibilty and not timeStop:
                        pg.time.set_timer(hit_cooldown, 350)
                        self.cooldown = True
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.doublejump = False
                        hurt_sound.play()
                        health -= SelectedDamage
                        self.in_air = False
                        self.jumped = False
                

                #check for collision in y direction
                if tile[1].colliderect(self.rect.x+5, self.rect.y + dy, self.width-5, self.height) and self.on_platform is False:
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
            if pg.sprite.spritecollide(self, spider_group, False) and self.cooldown is False and not self.invincibilty and not timeStop:
                    health -= SelectedDamage
                    hurt_sound.play()
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)
                    
            if pg.sprite.spritecollide(self, lava_group, False) and self.cooldown is False and not self.invincibilty and not timeStop:
                    hurt_sound.play()
                    health -= SelectedDamage
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)
                    
            if pg.sprite.spritecollide(self, deeplava_group, False) and self.cooldown is False and not self.invincibilty and not timeStop:
                    hurt_sound.play()
                    health -= SelectedDamage + 1
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)

            if pg.sprite.spritecollide(self, PortalDoor_group, False):
                    warped_sound.play()
                    time.sleep(0.2)
                    health = -10


            if pg.sprite.spritecollide(self, BoostRight_group, False):
                if not self.boost_sound_playing:
                    boost_sound.play()
                dx += random.uniform(5,10)          
                self.direction = 1
                dy += .25

            if pg.sprite.spritecollide(self, BoostLeft_group, False):
                if not self.boost_sound_playing:
                    boost_sound.play()
                dx -= random.uniform(5,10)          
                self.direction = -1

            if pg.sprite.spritecollide(self, BoostUp_group, False):
                if not self.boost_sound_playing:
                    channel = pg.mixer.find_channel()
                    if channel:
                        channel.play(boost_sound)
                        self.boost_sound_playing = True
                    self.boost_sound_playing = False
                        
                self.vel_y -= random.uniform(1,3)

            if pg.sprite.spritecollide(self, Ghost_group, False) and self.cooldown is False and not self.invincibilty and not timeStop:
                    hurt_sound.play()
                    health -= SelectedDamage * 0.15
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)
            

            if pg.sprite.spritecollide(self, Trampoline_group, False) and self.jumped is False:
                    self.vel_y = round(random.uniform(-10,-12), 4)
                    dy += .25
                    if not self.tramp_sound_playing:
                        channel = pg.mixer.find_channel()
                    if channel:
                        channel.play(tramp_sound)
                        self.tramp_sound_playing = True
                    self.tramp_sound_playing = False

            if pg.sprite.spritecollide(self, Trampoline_group, False) and self.jumped is True:
                    self.vel_y -= 4.9
                    if not self.tramp_sound_playing:
                        channel = pg.mixer.find_channel()
                    if channel:
                        channel.play(tramp_sound)
                        self.tramp_sound_playing = True
                    self.tramp_sound_playing = False
            
            if pg.sprite.spritecollide(self, Cactus_group, False) and self.cooldown is False and not self.invincibilty and not timeStop:
                    hurt_sound.play()
                    health -= SelectedDamage - 1
                    self.cooldown = True
                    pg.time.set_timer(hit_cooldown, 350)
            
            for each in Platform_group:
                if each.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if each.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.on_platform = True
                    #check if below platform
                    if abs((self.rect.top + dy) - each.rect.bottom) < 20:
                        self.vel_y = 0
                        dy = each.rect.bottom - self.rect.top
                    #check if above platform
                    
                    elif abs((self.rect.bottom + dy) - each.rect.top) < 20:
                    
                        for tile in world.tile_list:
                            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) and not self.invincibilty:
                                #check if jumping / player hitting head on tile
                                if each.move_x == 1:
                                    if each.move_direction == 1:
                                        if each.move_counter > 10:
                                            self.rect.right = tile[1].x - 3
                                            i = 1
                                    elif each.move_direction == -1:
                                        if each.move_counter > 10:
                                            self.rect.left = tile[1].x + tile_size + 3
                                            i = 1
                                elif i == 1:
                                    break
                                else:
                                    self.rect.top = each.rect.bottom
                                    self.doublejump = False
                                    self.in_air = False
                                    self.jumped = False
                                    i = 1
                                    if not self.invincibilty  and not timeStop:
                                        health -= SelectedDamage
                                        self.cooldown = True
                                        pg.time.set_timer(hit_cooldown, 350)
                                        hurt_sound.play()
                        if i == 1:
                            break
                        else:
                            self.rect.bottom = each.rect.top - 1
                            self.in_air = False
                            dy = 0
                            self.vel_y = 0
                            if (key[pg.K_UP]) or (key[pg.K_w]):
                                jumpheight = round(random.uniform(-8, -14.5), 3)
                                self.vel_y = jumpheight
                                self.jumped = True
                                jump_sound.play()           

                    #move sideways with the platform
                    if each.move_x != 0:
                        self.rect.x += each.move_direction
                        self.vel_y = 1
                        if (key[pg.K_UP]) or (key[pg.K_w]):
                            jumpheight = round(random.uniform(-8, -14.5), 3)
                            self.vel_y = jumpheight
                            self.jumped = True
                            jump_sound.play()

            if self.in_air:
                self.on_platform = False

            if self.cooldown is True:
                if self.direction == 1:
                    self.image = self.damage[0]
                    
                if self.direction == -1:
                    self.image = self.damage[1]

            self.rect.x += dx
            self.rect.y += dy

            if self.boost_sound_playing is True:
                self.boost_sound_playing = False
            if self.tramp_sound_playing is True:
                self.tramp_sound_playing = False
            if self.trampBounce_sound_playing is True:
                self.trampBounce_sound_playing = False

        if not self.can_dash:
            self.dash_cooldown_timer -= 1
            if self.dash_cooldown_timer <= 0:
                self.can_dash = True
        screen.blit(self.image, self.rect)      
        return health
                
    def reset(self, x, y):
        self.img_right = []
        self.img_left = []
        self.index = 0
        self.counter = 0
        self.joystick = None
        self.deadzone = 0.2
        pg.joystick.init()
        if pg.joystick.get_count() > 0:
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()
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
        self.boost_sound_playing = False
        self.tramp_sound_playing = False
        self.trampBounce_sound_playing = False
        self.on_platform = False
        self.invincibilty = False
        self.doubleBones = False
        self.candinodash = candinodash
        self.dash_cooldown = 60 # in frames, 60 frames = 1 second at 60 FPS
        self.dash_cooldown_timer = 0
        self.can_dash = True

class Spider(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        IMG = pg.image.load(f'enemy/tile001.png')
        self.IMGLEFT = pg.transform.scale(IMG, (40,29))
        self.IMGRIGHT = pg.transform.flip(self.IMGLEFT, True,False)

        self.image = self.IMGLEFT
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 4
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_direction = 1
        self.counter = 0
        self.direction = 1
        self.randomlist = []
        for i in range(0,20):
            n = round(random.uniform(10,30), 2)
            self.randomlist.append(n)
        self.vel_y = 0
        self.in_air = False

    def update(self):
        dy = 0
        self.rect.x += self.move_direction
        self.counter += 1
        player_movement = random.choice(self.randomlist)
        player_movement = 3000

        self.vel_y += 0.15
        if abs(self.counter) > player_movement:
            self.move_direction *= -1
            self.counter *= -1
            self.direction *= -1
        
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.move_direction *= -1
                self.direction *= -1

                #check for collision in y direction
            if tile[1].colliderect(self.rect.x+3, self.rect.y + dy, self.width-5, self.height) and self.in_air is False:
                dy = tile[1].top - self.rect.bottom
                self.vel_y = 0
                

        if self.direction == -1:
            self.image = self.IMGLEFT
        if self.direction == 1:
            self.image = self.IMGRIGHT

        dy += self.vel_y
        self.rect.y += dy
        self.rect.y -= 2

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

class Trampoline(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/trampoline.png')
        self.image = pg.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

class Cake(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/cake.png')
        self.image = pg.transform.scale(img, ((tile_size // 2)+10, (tile_size // 2)+10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BoostRight(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.transform.rotate(pg.image.load('img/jumpboost.png'), 270)
        self.image = pg.transform.scale(img, ((tile_size // 2)+10, (tile_size // 2)+10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    

class BoostLeft(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.transform.rotate(pg.image.load('img/jumpboost.png'), 90)
        self.image = pg.transform.scale(img, ((tile_size // 2)+10, (tile_size // 2)+10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('img/platform.png')
        self.move_x = move_x
        self.move_y = move_y
        if move_x == 1:    
            self.image = pg.transform.scale(img, (tile_size + 10, tile_size // 2))
        else:
            self.image = pg.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        x = random.randint(0,100)
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        
        if abs(self.move_counter) > 999:
            self.move_direction *= -1
            self.move_counter *= -1

        
        for tile in world.tile_list:

            if self.move_x ==1:
                if tile[1].colliderect(self.rect.x-10, self.rect.y, self.width+20, self.height):
                    self.move_direction *= -1
                    self.move_counter *= -1
            else:
                if tile[1].colliderect(self.rect.x, self.rect.y-player.height, self.width, self.height+player.height//2):
                    self.move_direction *= -1
                    self.move_counter *= -1

        if x == 500:
            self.move_direction *= -1
            self.move_counter *= -1

class Ghost(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        IMG = pg.image.load(f'enemy/ghost.png')
        self.IMGLEFT = pg.transform.scale(IMG, (70,68))
        self.IMGRIGHT = pg.transform.flip(self.IMGLEFT, True,False)

        self.image = self.IMGLEFT
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 4
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Initialize movement variables
        self.home_x = x
        self.home_y = y - 4
        self.move_direction = 0
        self.direction = 1
        self.swooping = False
        self.returning = False
        self.start_y = 0
        self.start_x = 0
        self.end_y = 0
        self.timer = 0

        # Initialize duration and probability variables
        self.duration = 0
        self.max_duration = 50  # 2 seconds at 60 FPS
        self.swoop_prob = 0.001  # 20% probability of swooping

    def update(self, player):
        player_distance = abs(player.rect.x - self.rect.x)
        if not self.swooping and not self.move_direction and player_distance <= 5000 and random.random() < self.swoop_prob:
            self.timer = 0
            if player.rect.x < self.rect.x:
                self.move_direction = -1  # move left towards player
            else:
                self.move_direction = 1  # move right towards player
            self.swooping = True
            self.start_y = self.rect.y
            self.start_x = self.rect.x
            self.end_y = player.rect.y
            self.returning = False
            self.duration = 0  # reset duration

        # Move the ghost during swoop
        elif self.swooping and not self.returning:
            self.rect.x += self.move_direction * 2
            delta_y = (self.end_y - self.rect.y) // 10
            self.rect.y += delta_y
            self.duration += 1
            if abs(self.rect.y - self.end_y) <= 10 or self.duration >= self.max_duration:
                self.returning = True

            # Rotate the image to face the player
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y
            angle = math.atan2(dy, dx) * 180 / math.pi
            self.image = pg.transform.rotate(self.IMGLEFT, angle)

        elif not self.swooping and not self.returning:
            idle_x = random.randint(-1, 1)
            idle_y = random.randint(-1, 1)
            self.rect.x += idle_x
            self.rect.y += idle_y

        # Return to original position after swoop
        elif self.returning:
            delta_y = (self.home_y - self.rect.y) // 10
            delta_x = (self.home_x - self.rect.x) // 10
            if abs(delta_x) <= 5 and abs(delta_y) <= 5:
                self.swooping = False
                self.move_direction = 0
                self.duration = 0  # reset duration
            else:
                self.rect.y += delta_y
                self.rect.x += delta_x

            if self.direction == -1:
                self.image = self.IMGLEFT
            elif self.direction == 1:
                self.image = self.IMGRIGHT






class Invincibilty(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.transform.scale(pg.image.load('img/rainbowstar.png'), ((tile_size // 2)+10, (tile_size // 2)+10))
        self.image = pg.transform.scale(img, (tile_size, (tile_size)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class DoubleBones(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.transform.scale(pg.image.load('img/doublebones.png'), ((tile_size // 2)+10, (tile_size // 2)+10))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class StopTime(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.transform.scale(pg.image.load('img/timestop.png'), ((tile_size // 2)+10, (tile_size // 2)+10))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cactus(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.transform.scale(pg.image.load('enemy/cactus.png'), ((tile_size // 2)+15, (tile_size // 2)+20))
        self.image = img
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
                    BoostUp_group.add(jump)
                if tile == 11:
                    # trampoline image
                    trampoline = Trampoline(col_count * tile_size, row_count * tile_size)
                    Trampoline_group.add(trampoline)
                if tile == 12:
                    # boost sprite
                    right = BoostRight(col_count * tile_size, row_count * tile_size)
                    BoostRight_group.add(right)
                if tile == 13:
                    # boost sprite
                    left = BoostLeft(col_count * tile_size, row_count * tile_size)
                    BoostLeft_group.add(left)
                if tile == 14:
                    # boost sprite
                    cake = Cake(col_count * tile_size, row_count * tile_size)
                    Cake_group.add(cake)
                if tile == 15:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1,0)
                    Platform_group.add(platform)
                if tile == 16:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0,1)
                    Platform_group.add(platform)
                if tile == 17: 
                    ghost = Ghost(col_count * tile_size, row_count * tile_size + 15)
                    Ghost_group.add(ghost)
                if tile == 18: 
                    star = Invincibilty(col_count * tile_size, row_count * tile_size+5)
                    Invinc_group.add(star)
                if tile == 19: 
                    db = DoubleBones(col_count * tile_size, row_count * tile_size + 15)
                    DB_group.add(db)
                if tile == 20: 
                    stop = StopTime(col_count * tile_size, row_count * tile_size + 15)
                    timeStop_group.add(stop)
                if tile == 21: 
                    cactus = Cactus(col_count * tile_size, row_count * tile_size)
                    Cactus_group.add(cactus)
                
                col_count += 1
            row_count += 1


    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pg.draw.rect(screen, (255,255,255), tile[1], 2)


#Create Sprite Groups
lava_group = pg.sprite.Group()
deeplava_group = pg.sprite.Group()
spider_group = pg.sprite.Group()
bone_group = pg.sprite.Group()
PortalDoor_group = pg.sprite.Group()
BoostUp_group = pg.sprite.Group()
Trampoline_group = pg.sprite.Group()
player = Player(190, height - 130)
BoostRight_group = pg.sprite.Group()
BoostLeft_group = pg.sprite.Group()
heart = Hearts()
Cake_group = pg.sprite.Group()
Platform_group = pg.sprite.Group()
Ghost_group = pg.sprite.Group()
Invinc_group = pg.sprite.Group()
DB_group = pg.sprite.Group()
timeStop_group = pg.sprite.Group()
Cactus_group = pg.sprite.Group()


# Buttons
restart = Button(width //2 - 150, height //2+100, restart_IMG)
start = Button(width //2 - 100, height //2 -200, start_IMG)
controls = Button(width //2 - 200, height //2 +100, HowToPlay_IMG)
levelselect = Button(width //2 - 200, height //2 -50, levelselect_IMG)
begin = Button(width //2 - 100, height //2, begin_IMG)
begin2 = Button(width //2 + 275, height //2 +350, pg.transform.scale(begin_IMG, (100,50)))
settings = Button(width-75,0, settings_IMG)
menu = Button(width //2 - 375, height //2 +350, menu_IMG)
next2 = Button(width //2 + 275, height //2 +350, smallnext_IMG)
load = Button(width //2 -50, height // 2+10, load_img)
exit = Button(width //2 - 100, height //2 +250, exit_IMG)
exit2 = Button(width //2 + 50, height //2+100, exit2_IMG)
next_level = Button(width //2 -50, height //2+325, next_IMG)
doublejump_btn = Button(width //2 -325, height //2-250, doublejump_IMG1)
extralife_btn = Button(width //2 + 50, height //2-250, extralife_IMG1)
levelskip_btn = Button(width //2 -325, height //2, levelskip_IMG)
skip_btn = Button(width //2 + 200, height - 60, skip_IMG)
dinodash_btn = Button(width //2 +50 , height //2, dinodash_IMG)
closegame = Button(width //2  - exitgame.get_width()//2, height //2, exitgame)
back = Button(width //2 - 375, height //2 +350, back_IMG)
Feedback_btn = Button(width //2 - feedback_IMG.get_width()//2, height //2 +150, feedback_IMG)
Feedback_btn2 = Button(width //2 - feedback_IMG.get_width()//2, height //2 -250, feedback_IMG)


level = 8
# load first level
if path.exists(f'levels/level{level}_data'):
    level_data = open(f'levels/level{level}_data', 'rb')
    world_data = pickle.load(level_data)
world = World(world_data)

cursor_img = pg.transform.scale(pg.image.load('img/cursor.png'), (25,25))
cursor_pos = [width - 200, height - 200]

# Get the first connected joystick
if pg.joystick.get_count() > 0:
    joystick = pg.joystick.Joystick(0)
    joystick.init()

# start game loop
running = True
while running:
    #set FPS and display background/sun
    screen.fill((224, 176, 255))
    clock.tick(fps)
    screen.blit(BG, (0,0))
    screen.blit(SUN, (25,50))
    current_time = pg.time.get_ticks()


    if level > 10 and level <15:
        print('v')
    #show start menu when starting 
    if StartMenu == 1:
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        print_text("Welcome To Dino Dash!", font, SILVER, (width//2)-350,(height//2)-300)
        
        #if buttons are pressed
        if start.draw(): 
            tick_sound.play()
            StartMenu = 1.1
            time.sleep(0.1)
        if exit.draw():
            running = False
        if settings.draw():
            tick_sound.play()
            StartMenu = 4 
            time.sleep(0.1)

        if controls.draw():
            tick_sound.play()
            StartMenu = 3
            time.sleep(0.1)
        if  levelselect.draw():
            tick_sound.play()
            StartMenu = 5
            time.sleep(0.1)

        

    elif StartMenu == 1.1:
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        print_text("Enter Your Name:", font, SILVER, (width//2)-240,(height//2)-200)
        if active:
            color = activepurple
        else:
            color = notactivepurple

        #if buttons are pressed

        pg.draw.rect(screen, color, NameInput_rect)
        text = userfont.render(username, True, GOLD)
        screen.blit(text, ((width//2)-text.get_width()//2, NameInput_rect.y+10))
        NameInput_rect.w = max(450, 10)

        if begin.draw():
            soundplaying = False
            tick_sound.play()
            level = 1
            StartMenu = 0
            if username == '':
                username = 'You'
            start_point = pg.time.get_ticks()         
            loadingscreen = True
            num = random.randint(0,6)
            loadingIMG = loadingIMGS[num]
            tip = random.choice(LoadingScreenTips)
            if SelectedHealth == 0:
                SelectedHealth = MediumHealth
                max_health = SelectedHealth
                health = max_health
                SelectedDamage = MediumDamage
            else:
                max_health = SelectedHealth

            levelStart = pg.time.get_ticks()
            paused = False

            

        if menu.draw():
            tick_sound.play()
            StartMenu = 1
            time.sleep(0.1)

        pg.display.flip()

    elif StartMenu == 2:
            pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))

            settingsText = "Game Settings"
            settingsText = userfont.render(settingsText, True, SILVER)
            screen.blit(settingsText, ((width//2)-settingsText.get_width()//2,35))

            sound = userfont.render(sound_mode, True, SILVER)
            sound_rect = sound.get_rect()
            sound_rect.topleft = ((width//2)-sound.get_width()//2,470)
            screen.blit(sound, ((width//2)-sound.get_width()//2,470))
            music = userfont.render(music_mode, True, SILVER)
            music_rect = music.get_rect()
            music_rect.topleft = ((width//2)-music.get_width()//2,340)
            screen.blit(music, ((width//2)-music.get_width()//2,340))
            
            
            if back.draw():
                tick_sound.play()
                StartMenu = 0 


            pg.display.flip()

    elif StartMenu == 4:
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        print_text("Game Settings", font, SILVER, (width//2)-240,35) 

        #difficulty level selction
        difficulty = userfont.render(difficulty_options[selected_difficulty], True, SILVER)
        difficulty_rect = difficulty.get_rect()
        difficulty_rect.topleft = ((width//2)-difficulty.get_width()//2,200)
        screen.blit(difficulty, ((width//2)-difficulty.get_width()//2,200))

        sound = userfont.render(sound_mode, True, SILVER)
        sound_rect = sound.get_rect()
        sound_rect.topleft = ((width//2)-sound.get_width()//2,470)
        screen.blit(sound, ((width//2)-sound.get_width()//2,470))

        music = userfont.render(music_mode, True, SILVER)
        music_rect = music.get_rect()
        music_rect.topleft = ((width//2)-music.get_width()//2,340)
        screen.blit(music, ((width//2)-music.get_width()//2,340))

        if selected_difficulty == 0:
            health = EasyHealth
            lives = EasyLives
            SelectedHealth = EasyHealth
            SelectedDamage = EasyDamage
        if selected_difficulty == 1:
            health = MediumHealth
            lives = MediumLives
            SelectedHealth = MediumHealth
            SelectedDamage = MediumDamage
        if selected_difficulty == 2:
            health = HardHealth
            lives = HardLives
            SelectedHealth = HardHealth
            SelectedDamage = HardDamage

        
        if menu.draw():
            tick_sound.play()
            StartMenu = 1  

        if Feedback_btn.draw():
            tick_sound.play()
            open_window()
            time.sleep(0.1)

        pg.display.flip()


    elif StartMenu == 3:
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        print_text("The Basics", font, SILVER, (width//2)-180,15)
        print_text("Use the keyboard or a controller to move your character!", scorefont,GOLD, (width//2)-390,(height//2)-300)
        print_text("OR", font, BLACK, (width//2)-50,(height//2))
        screen.blit(controller, (110, 500))
        screen.blit(keyboard, (100, 200))
        if menu.draw():
            tick_sound.play()
            StartMenu = 1
            time.sleep(0.1) 
        if next2.draw():
            tick_sound.play()
            StartMenu = 3.1
            time.sleep(0.1)
            
    elif StartMenu == 3.1:
        i = 1
        healthBar_length = int(10 / 10 * healthBar_width)
        healtharrow = pg.transform.rotate(downarrow, 215)
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        pg.draw.rect(screen, (224, 176, 245),pg.Rect(0, 625, width, screenspace + 10))
        print_text("The Basics", font, SILVER, (width//2)-180,15)
        print_text("Use the keyboard or a controller to move your character!", scorefont,GOLD, (width//2)-390,(height//2)-300)
        
        print_text("Your health resets each time you die,", scorefont, GOLD, (width//2)-240,160)
        print_text("avoid enemies, hazards, and fall damage!", scorefont, GOLD, (width//2)-270,185)
        pg.draw.rect(screen, BLACK, (healthBar_x-2, 643, healthBar_length+4, healthBar_height+4))
        pg.draw.rect(screen, GREEN, (healthBar_x, 645, healthBar_length, healthBar_height))
        screen.blit(healtharrow, (205, 665))
        if menu.draw():
            tick_sound.play()
            StartMenu = 1
            time.sleep(0.1)
        if next2.draw():
            tick_sound.play()
            StartMenu = 3.2
            time.sleep(0.1)
       
    elif StartMenu == 3.2: 
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        pg.draw.rect(screen, (224, 176, 255),pg.Rect(0, 625, width, screenspace + 10))
        livesarrow = pg.transform.rotate(downarrow, 180)

        print_text("The Basics", font, SILVER, (width//2)-180,15)
        print_text("Use the keyboard or a controller to move your character!", scorefont,GOLD, (width//2)-390,(height//2)-300)        
        
        print_text("Your health resets each time you die,", scorefont, SILVER, (width//2)-240,160)
        print_text("avoid enemies, hazards, and fall damage!", scorefont, SILVER, (width//2)-270,185)
        print_text("Hearts display your remaining lives.", scorefont, GOLD, (width//2)-250,220)
        print_text("Once they're gone, it's game over!", scorefont, GOLD, (width//2)-240,250)
        pg.draw.rect(screen, BLACK, (healthBar_x-2, 643, healthBar_length+4, healthBar_height+4))
        pg.draw.rect(screen, GREEN, (healthBar_x, 645, healthBar_length, healthBar_height))
    
        screen.blit(livesarrow, (383, 700))

        screen.blit(heart.imglist[4], (width//2-heart.imglist[4].get_width()//2,640))
        if menu.draw():
            tick_sound.play()
            StartMenu = 1
            time.sleep(0.1)
        if next2.draw():
            tick_sound.play()
            StartMenu = 3.3
            time.sleep(0.1) 

    elif StartMenu == 3.3:
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        pg.draw.rect(screen, (224, 176, 255),pg.Rect(0, 625, width, screenspace + 10))
        bonearrow = pg.transform.rotate(downarrow, 135)

        print_text("The Basics", font, SILVER, (width//2)-180,15)
        print_text("Use the keyboard or a controller to move your character!", scorefont,GOLD, (width//2)-390,(height//2)-300)
        
        print_text("Your health resets each time you die,", scorefont, SILVER, (width//2)-240,160)
        print_text("avoid enemies, hazards, and fall damage!", scorefont, SILVER, (width//2)-270,185)
        print_text("Hearts display your remaining lives.", scorefont, SILVER, (width//2)-250,220)
        print_text("Once they're gone, it's game over!", scorefont, SILVER, (width//2)-240,250)
        print_text("Collect Bones to purchase lives and upgrades!", scorefont, GOLD, (width//2)-300,280)
        pg.draw.rect(screen, BLACK, (healthBar_x-2, 643, healthBar_length+4, healthBar_height+4))
        pg.draw.rect(screen, GREEN, (healthBar_x, 645, healthBar_length, healthBar_height))
        print_text('10 X', scorefont, BLACK, 670,645)
        screen.blit(bonearrow, (620, 665))
        screen.blit(bone_IMG, (730,640))

        screen.blit(heart.imglist[4], (width//2-heart.imglist[4].get_width()//2,640))
        if menu.draw():
            tick_sound.play()
            StartMenu = 1
            time.sleep(0.1) 
        if next2.draw():
            tick_sound.play()
            StartMenu = 3.4
            time.sleep(0.1)

    elif StartMenu == 3.4:
        screen.blit(shopBG, (0,0))
        print_text("Item Shop", font, BLACK, (width//2)-150,15)
        print_text("Here is where you can purchase ", scorefont, BLACK, (width//2)-220,(height//2)-340)
        print_text("character upgrades and abilites! ", scorefont, BLACK, (width//2)-220,(height//2)-300)
        extralife_btn.image = extralife_IMG
        doublejump_btn.image = doublejump_IMG
        if extralife_btn.draw():
            pass
        if doublejump_btn.draw():
            pass
        if levelskip_btn.draw():
            pass
        if dinodash_btn.draw():
            pass

        if menu.draw():
            tick_sound.play()
            StartMenu = 1
        if begin2.draw():
            tick_sound.play()
            StartMenu = 1.1

    
    elif StartMenu == 5:
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        print_text("Level Selection", font, SILVER, (width//2)-240,25)
        print_text("Enter A Code From The Previous Playthough!", boughtfont, SILVER, (width//2)-220,(height//2)-130)
        if active:
            color = activepurple
        else:
            color = notactivepurple

        # code input box
        pg.draw.rect(screen, color, CodeInput_rect)
        text = userfont.render(code, True, GOLD)
        screen.blit(text, ((width//2)-text.get_width()//2, CodeInput_rect.y+10))
        CodeInput_rect.w = max(450, 10)
        if menu.draw():
            tick_sound.play()
            StartMenu = 1  
        if load.draw():
            tick_sound.play()
            if code in LevelCodes:
                level = LevelCodes[code]
                if path.exists(f'levels/level{level}_data'):
                    world = reset_level(level)
                    level_data = open(f'levels/level{level}_data', 'rb')
                    world_data = pickle.load(level_data)
                    StartMenu = 0
                    start_point = pg.time.get_ticks()         
                    loadingscreen = True
                    num = random.randint(0,6)
                    loadingIMG = loadingIMGS[num]
                    tip = random.choice(LoadingScreenTips)
                
            else:
                InvalidCode()
                code = ''

        
        pg.display.flip()

    elif StartMenu == 6:
        pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
        print_text("Level Selection", font, SILVER, (width//2)-240,25)
        print_text("Enter A Code From The Previous Playthough!", boughtfont, SILVER, (width//2)-220,(height//2)-130)
        if active:
            color = activepurple
        else:
            color = notactivepurple

        # code input box
        pg.draw.rect(screen, color, CodeInput_rect)
        text = userfont.render(code, True, GOLD)
        screen.blit(text, ((width//2)-text.get_width()//2, CodeInput_rect.y+10))
        CodeInput_rect.w = max(450, 10)
        if back.draw():
            tick_sound.play()
            time.sleep(0.1)
            StartMenu = 0
        if load.draw():
            tick_sound.play()
            time.sleep(0.1)
            if code in LevelCodes:
                level = LevelCodes[code]
                if path.exists(f'levels/level{level}_data'):
                    world = reset_level(level)
                    level_data = open(f'levels/level{level}_data', 'rb')
                    world_data = pickle.load(level_data)
                    StartMenu = 0
                    start_point = pg.time.get_ticks()         
                    loadingscreen = True
                    num = random.randint(0,6)
                    loadingIMG = loadingIMGS[num]
                    tip = random.choice(LoadingScreenTips)
                    paused = False
                
            else:
                InvalidCode()
                code = ''

        
        pg.display.flip()


    elif StartMenu == 0 and loadingscreen is False: 
        world.draw()
        spider_group.draw(screen)
        lava_group.draw(screen)
        deeplava_group.draw(screen)
        BoostUp_group.draw(screen)
        Trampoline_group.draw(screen)
        PortalDoor_group.draw(screen)
        bone_group.draw(screen)
        BoostRight_group.draw(screen)
        BoostLeft_group.draw(screen)
        Cake_group.draw(screen)
        Platform_group.draw(screen)
        Ghost_group.draw(screen)
        Invinc_group.draw(screen)
        DB_group.draw(screen)
        timeStop_group.draw(screen)
        Cactus_group.draw(screen)
        

        if SelectedHealth != 0:
            healthBar_length = int(health / SelectedHealth * healthBar_width)
        
        pg.draw.rect(screen, BLACK, (healthBar_x-4, healthBar_y-4, healthBar_width+8, healthBar_height+8))
        pg.draw.rect(screen, WHITE, (healthBar_x-2, healthBar_y-2, healthBar_length+4, healthBar_height+4))
        if health != -10:
            timer = (current_time-levelStart)/600
            # Convert the time difference to a string
            time_string = "{:.1f}".format(timer)

            # Render the time string to a surface
            font1 = pg.font.Font(None, 36)
            text_surface = font1.render(time_string, True, WHITE)
            screen.blit(text_surface, (10, 11))
            text_surface = font1.render(time_string, True, BLACK)
            screen.blit(text_surface, (10, 10))
        
        if health > 0:
            if not paused:
                health = player.update(health)
                if levelskip_count > 0:
                    if skip_btn.draw():
                        health = -10
                        levelskip_count -= 1
                    print_text(f"{levelskip_count}", scorefont, BLACK, width //2 + 180, height - 40)

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

            # display bone counter
            print_text(f"{bone_count} X", scorefont, BLACK, 695, 815)
            for code, i in FutureLevelCodes.items():
                if i == level:
                    print_text(f'Passcode: {code}', boughtfont, WHITE, (width//2)+180,11)
                    print_text(f'Passcode: {code}', boughtfont, BLACK, (width//2)+180,10)

            if health > 7:
                pg.draw.rect(screen, GREEN, (healthBar_x, healthBar_y, healthBar_length, healthBar_height))
            elif health > 3:
                pg.draw.rect(screen, YELLOW, (healthBar_x, healthBar_y, healthBar_length, healthBar_height))
            else:
                pg.draw.rect(screen, RED, ((healthBar_x, healthBar_y, healthBar_length, healthBar_height)))

            if not timeStop:
                spider_group.update()
                Platform_group.update()
                for ghost in Ghost_group:
                    ghost.update(player)
            elif timeStop: 
                    screen.blit(iceFilter, (0,0))

            if player.invincibilty:
                for i in range(36):
                    # Define the rainbow color for the edge
                    rainbow_color = pg.Color(0, 0, 0)
                    rainbow_color.hsva = ((pg.time.get_ticks() / 10 + i * 45) % 360, 100, 100, 100)
                    
                    # Draw the rainbow border
                    border_size = 10
                    pg.draw.rect(screen, rainbow_color, pg.Rect(0, 0, width, border_size))
                    pg.draw.rect(screen, rainbow_color, pg.Rect(0, 0, border_size, height))
                    pg.draw.rect(screen, rainbow_color, pg.Rect(width-10, 0, border_size, height))
                    pg.draw.rect(screen, rainbow_color, pg.Rect(0, height-10, width, border_size)) 
            # display bone counter
            print_text(f"{bone_count} X", scorefont, BLACK, 695, 815)
            for code, i in FutureLevelCodes.items():
                    if i == level:
                        print_text(f'Passcode: {code}', boughtfont, WHITE, (width//2)+180,11)
                        print_text(f'Passcode: {code}', boughtfont, BLACK, (width//2)+180,10)

            if not player.doubleBones:
                screen.blit(bone_IMG, (750,810))
            else:
                screen.blit(doublebone_IMG, (750,810))

            if pg.sprite.spritecollide(player, bone_group, True):
                bone_sound.play()
                if player.doubleBones:
                    bone_count += 2
                    total_bone_count += 2
                else:    
                    bone_count += 1
                    total_bone_count += 1

            if pg.sprite.spritecollide(player, PortalDoor_group, False):
                score = round(math.exp(-0.08 * timer)* 100, 1)
                totalscore += score

            if pg.sprite.spritecollide(player, Cake_group, False):
                if health<max_health:
                    if pg.sprite.spritecollide(player, Cake_group, True):
                        ate_sound.play()
                        if SelectedHealth == 0:
                            if health >= 7:
                                health = 10
                            elif health < 7:
                                health += 3
                        elif SelectedHealth == 150:
                            if health >= 130:
                                health = 150
                            elif health < 130:
                                health += 20
                        elif SelectedHealth == 100:
                            if health >= 70:
                                health = 100
                            elif health < 70:
                                health += 30
                        elif SelectedHealth == 10:
                            if health >= 7:
                                health = 10
                            elif health < 7:
                                health += 3


            if pg.sprite.spritecollide(player, Invinc_group, False):
                if not player.invincibilty:
                    pg.sprite.spritecollide(player, Invinc_group, True)
                    invincibiltyStart = pg.time.get_ticks()
                    invinc_sound.play()
                    print(SelectedHealth)
                    if SelectedHealth == 0:
                            if health >= 7:
                                health = 10
                            elif health < 7:
                                health += 3
                    elif SelectedHealth == 150:
                        if health >= 130:
                            health = 150
                        elif health < 130:
                            health += 20
                    elif SelectedHealth == 100:
                        if health >= 70:
                            health = 100
                        elif health < 70:
                            health += 30
                    elif SelectedHealth == 10:
                        if health >= 7:
                            health = 10
                        elif health < 7:
                            health += 3

            if pg.sprite.spritecollide(player, DB_group, False):
                if not player.doubleBones:
                    pg.sprite.spritecollide(player, DB_group, True)
                    DBStart = pg.time.get_ticks()
                    doublebones_sound.play()

            if pg.sprite.spritecollide(player, timeStop_group, False):
                if not timeStop:
                    pg.sprite.spritecollide(player, timeStop_group, True)
                    StopTimeStart = pg.time.get_ticks()
                    timestop_sound.play()
                    

        if lives == 1 and health <= 0 and health != -10:

            if soundplaying and not gameover:
                soundplaying = False
                gameover = True
                if gameover and not soundplaying:
                    pg.mixer.music.stop()
                    pg.mixer.music.load('sound/evil_laugh.mp3')
                    pg.mixer.music.play(-1)

            #display game over
            pg.draw.rect(screen, (112, 41, 99),pg.Rect(0, 0, width, height))
            screen.blit(deaddino, ((width//2)-150,(height//2)+150))

            #display death quotes and buttons# Define the font and font size
            gameoverfont = pg.font.SysFont('Courier Regular', 50)

            # Define the text to be displayed
            gameover_text = "Game over, man. Game over."
            username_text = f"{username}"
            bone_count_text = f"You earned {total_bone_count} bones!"

            # Render the text
            gameover_render = gameoverfont.render(gameover_text, True, RED)
            username_render = gameoverfont.render(username_text, True, RED)
            bone_count_render = gameoverfont.render(bone_count_text, True, RED)

            # Get the dimensions of the text surfaces
            gameover_width, gameover_height = gameover_render.get_size()
            username_width, username_height = username_render.get_size()
            bone_count_width, bone_count_height = bone_count_render.get_size()

            # Calculate the positions of the text surfaces
            gameover_x = (width - gameover_width) // 2
            gameover_y = (height - gameover_height) // 2 - 350
            username_x = (width - username_width) // 2
            username_y = gameover_y + gameover_height + 80
            bone_count_x = (width - bone_count_width) // 2
            bone_count_y = username_y + username_height + 50

            # Blit the text surfaces onto the screen
            screen.blit(gameover_render, (gameover_x, gameover_y))
            screen.blit(username_render, (username_x, username_y))
            screen.blit(bone_count_render, (bone_count_x, bone_count_y))
            if closegame.draw():
                running = False

        # if player dies
        elif health <= 0 and health != -10:
            
            
            pg.draw.rect(screen, (112, 41, 99),pg.Rect(0, 0, width, height))
            screen.blit(deaddino, ((width//2)-150,(height//2)+150))
            
            #display death quotes and buttons
            print_text(f"You Died.", font, RED, (width//2)-150,(height//2-50))
            quote = DeathQuotes[player.deathnum]
            font1 = pg.font.Font(None, 30)
            text = font1.render(quote, True, YELLOW)
            text_rect = text.get_rect(center=(width//2, height//2+50))

            screen.blit(text, text_rect)
            
            if restart.draw():
                
                tick_sound.play()
                if level != 0:
                    print('no cap')
                    level -= 1
                else:
                    level = 1
                world = reset_level(level)
                if SelectedHealth == 0:
                    health = 10
                else:
                    health = SelectedHealth
                if bone_count >= 2:
                    bone_count -= 2
                lives -= 1
                start_point = pg.time.get_ticks()         
                loadingscreen = True
                num = random.randint(0,6)
                loadingIMG = loadingIMGS[num]
                levelStart = pg.time.get_ticks()
                died = False
            if exit2.draw():
                soundplaying = False
                pg.mixer.music.stop()
                pg.mixer.music.load('sound/menu_song.wav')
                pg.mixer.music.play(-1)
                tick_sound.play()
                time.sleep(0.1)
                level = 1
                player.reset(190, height - 130)
                if SelectedHealth == 0:
                    health = 10
                else:
                    health = SelectedHealth
                username = ''
                paused = False
                StartMenu = 1
                died = False

        

        # if player completes level
        elif health == -10:
            tip = random.choice(LoadingScreenTips)
            if level != max_level:
                inshop = True
                screen.blit(shopBG, (0,0))
                title = "Blorgs Quantum Market"
                title = userfont.render(title, True, WHITE)
                screen.blit(title, (((width//2)-title.get_width()//2),10))


                title = userfont.render(f"Score: {str(score)}", True, WHITE)
                screen.blit(title, (((width//2)-title.get_width()//2),71))
                title = userfont.render(f"Score: {str(score)}", True, store_color)
                screen.blit(title, (((width//2)-title.get_width()//2),73))


                print_text(f"You have {bone_count} bones.", scorefont, WHITE, (width//2)-120,(height-168))

                title = "Blorgs Quantum Market"
                title = userfont.render(title, True, store_color)

                screen.blit(title, (((width//2)-title.get_width()//2),13))
                print_text(f"You have {bone_count} bones.", scorefont, store_color, (width//2)-120,(height-170))
                
                # double jump
                if bone_count >= 5 and doublejumpbought is False:
                    doublejump_btn.image = doublejump_IMG
                    if doublejump_btn.draw():
                        candoublejump = True
                        doublejump_btn.image = doublejump_IMG2
                        if doublejumpbought is False:
                                bone_count -= 5
                                doublejumpbought = True
                                doublejumpscreen = True

                elif doublejumpbought is True:
                    doublejump_btn.image =  doublejump_IMG2
                    doublejump_btn.draw()
                else:
                    doublejump_btn.image = doublejump_IMG1
                    if doublejump_btn.draw():
                        pass

                # extra lives
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

                if bone_count >= 10 and dinodash is False:
                    dinodash_btn.image = dinodash_IMG
                    if dinodash_btn.draw():
                        candinodash = True
                        dinodash_btn.image = dinodash_IMG1
                        if dinodash is False:
                            bone_count -= 10
                            dinodash = True
                            candinodash = True
                            purchase_sound.play()


                elif dinodash is True:
                    dinodash_btn.image =  dinodash_IMG2
                    dinodash_btn.draw()
                else:
                    dinodash_btn.image = dinodash_IMG1
                    if dinodash_btn.draw():
                        pass

                # level skip
                if bone_count >= 30:
                    if levelskip_btn.draw():
                        bone_count -= 30
                        levelskip_count += 1
                        purchase_sound.play()
                else:
                    levelskip_btn.image = levelskip_IMG1
                    if levelskip_btn.draw():
                        pass




                if next_level.draw():  
                    # reset game and go to next level
                    level += 1
                    if level <= max_level:
                        if doublejumpscreen is True and notshown is True:
                            HowToDoubleJump()
                            notshown = False
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
                        levelStart = pg.time.get_ticks()
                        inshop = False

            if level == max_level:
                if soundplaying and not gamewon:
                    soundplaying = False
                    gamewon = True
                    if gamewon and not soundplaying:
                        pg.mixer.music.stop()
                        pg.mixer.music.load('sound/game_won.wav')
                        pg.mixer.music.play(-1)

                if totalscore > highscore:
                    highscore = totalscore
                    highscorefile = open("levels/highscore.txt", "w")
                    highscorefile.write(str(int(totalscore)))
                    highscorefile.close()
                pg.draw.rect(screen, GRAY,pg.Rect(0, 0, width, height))
                print_text("Wait.. you won?", font, WHITE, (width//2)-210,(height//2)-250)
                totalscore_str = f"Your Score: {round(totalscore, 1)}"
                totalscore_surf = userfont.render(totalscore_str, True, WHITE)
                screen.blit(totalscore_surf, (((width//2)-totalscore_surf.get_width()//2),(height//2)-90))
                highscore_str = f"Highscore: {highscore}"
                highscore_surf = userfont.render(highscore_str, True, WHITE)
                screen.blit(highscore_surf, (((width//2)-highscore_surf.get_width()//2),(height//2)-170))
                print_text(f"You earned {total_bone_count} bones!", font, WHITE,  (width//2)-320,(height//2))
                highscorefile.close()
                if restart.draw():
                    StartMenu = 1
                    username = ''
                    time.sleep(0.5)
                if exit2.draw():
                    running = False
                     
        

        if paused and loadingscreen is False:
            surface = pg.Surface((width,height))
            surface.fill(GRAY)
            screen.blit(surface, (0,0))
            title = 'Paused'
            title = userfont.render(title, True, SILVER)
            screen.blit(title, ((width//2)-title.get_width()//2,40))
            exit = Button(width //2 - 100, height //2 +150, exit_IMG)
            if settings.draw():
                tick_sound.play()
                StartMenu = 2
                time.sleep(0.1)

            if exit.draw():
                soundplaying = False
                tick_sound.play()
                time.sleep(0.1)
                StartMenu = 1
                username = ''
                code = ''
                if SelectedHealth == 0:
                    health = 10
                else:
                    health = SelectedHealth
                paused = False
                player.reset(100, height - 150)
                exit = Button(width //2 - 100, height //2 +250, exit_IMG)

            if  levelselect.draw():
                tick_sound.play()
                code = ''
                StartMenu = 6
                time.sleep(0.1)
           
            if Feedback_btn2.draw():
                subject = ''
                feedback = ''
                open_window()
                

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.JOYDEVICEADDED:
            joystick = pg.joystick.Joystick(event.device_index)
            joysticks.append(joystick)

        #user event that allows for player damage cooldown
        if event.type == hit_cooldown:
            player.cooldown = False

        if event.type == pg.MOUSEBUTTONDOWN and StartMenu == 1.1:
            if NameInput_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pg.MOUSEBUTTONDOWN and (StartMenu == 5 or StartMenu == 6 ):
            if CodeInput_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pg.MOUSEBUTTONDOWN and StartMenu == 4:
            if difficulty_rect.collidepoint(event.pos):
                selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                toggle_snd.play()
            else:
                pass

        if event.type == pg.MOUSEBUTTONDOWN and (StartMenu == 4 or StartMenu == 2):
            if music_rect.collidepoint(event.pos):
                toggle_music()
                toggle_snd.play()
            
        if event.type == pg.MOUSEBUTTONDOWN and (StartMenu == 4 or StartMenu == 2):
            if sound_rect.collidepoint(event.pos):
                toggle_sound()
                toggle_snd.play()

        if event.type == pg.KEYDOWN and len(code) < 9:
            # Check for backspace
            if event.key == pg.K_BACKSPACE and (StartMenu == 5 or StartMenu == 6):
  
                code = code[:-1]

            elif active is True and len(code) < 8 and (StartMenu == 5 or StartMenu == 6) and event.key != pg.K_RETURN:
                code += event.unicode

        if event.type == pg.KEYDOWN and len(username) < 14:
            # Check for backspace
            if event.key == pg.K_BACKSPACE and StartMenu == 1.1:
  
                username = username[:-1]

            elif active is True and len(username) < 12 and StartMenu == 1.1 and event.key != pg.K_RETURN:
                username += event.unicode

        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and loadingscreen is False and StartMenu == 0 and not died:
                paused = not paused

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                HowToDoubleJump()

        if event.type == pg.KEYDOWN and levelskip_count > 0 and loadingscreen is False and StartMenu == 0 and not paused and not inshop:
            keys = pg.key.get_pressed()
            if keys[pg.K_q]:
                health = -10
                levelskip_count -= 1
                
             
    if current_time - start_point < loadingscreentimer and loadingscreen is True and level <= max_level:
        screen.blit(loadingIMG,(0,0))
        font1 = pg.font.Font(None, 30)
        text = font1.render(tip, True, YELLOW)
        text_rect = text.get_rect(center=(width//2, 800))
        
        progress += 1

        progress_width = progress / max_progress * loadingBar_width
        pg.draw.rect(screen, BLACK, (loadingBar_x, loadingBar_y, 500, loadingBar_height),border_radius=5)
        pg.draw.rect(screen, loadingBar_color, (loadingBar_x, loadingBar_y, progress_width, loadingBar_height), border_radius=5)
        screen.blit(text, text_rect)
        lev = f'Level {level}'
        text = font1.render(lev, True, YELLOW)
        text_rect = text.get_rect(center=(width//2, 750))
        screen.blit(text, text_rect)
        
    if StartMenu == 0 and not soundplaying and not died and not gameover and not gamewon:
            pg.mixer.music.load('sound/gamesong.wav')
            pg.mixer.music.play(-1)
            soundplaying = True

    if StartMenu == 1 and not soundplaying:
        pg.mixer.music.stop()
        pg.mixer.music.load('sound/menu_song.wav')
        pg.mixer.music.play(-1)
        soundplaying = True
    
    if current_time-invincibiltyStart < 5000:
        player.invincibilty = True

    if current_time-invincibiltyStart > 5000:
        player.invincibilty = False

    if current_time-DBStart < 5000:
        player.doubleBones = True

    if current_time-DBStart > 5000:
        player.doubleBones = False

    if current_time- StopTimeStart < 5000:
        timeStop = True

    if current_time- StopTimeStart > 5000:
        timeStop = False
        
    if current_time - start_point > loadingscreentimer:
        loadingscreen = False
        progress = 0
        

    threshold = 0.1
    if pg.joystick.get_count() > 0 and joystick.get_button(2) and levelskip_count > 0 and loadingscreen is False and StartMenu == 0 and not paused and not inshop:
        levelskip_count -= 1
        health = -10

    if pg.joystick.get_count() > 0 and (StartMenu != 0 or inshop or died):
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)

        if abs(x_axis) > threshold or abs(y_axis) > threshold:
            cursor_pos = list(pg.mouse.get_pos())

            if x_axis > 0:
                cursor_pos[0] += int(x_axis * 10)
            else:
                cursor_pos[0] -= int(abs(x_axis) * 10)

            if y_axis > 0:
                cursor_pos[1] += int(y_axis * 10)
            else:
                cursor_pos[1] -= int(abs(y_axis) * 10)

    mouse_rel = pg.mouse.get_rel()
    if mouse_rel[0] != 0 or mouse_rel[1] != 0:
        cursor_pos = list(pg.mouse.get_pos())
        cursor_pos[0] += mouse_rel[0]
        cursor_pos[1] += mouse_rel[1]

    cursor_pos = list(cursor_pos)
    cursor_pos[0] = max(0, min(width-1, cursor_pos[0]))
    cursor_pos[1] = max(0, min(height-1, cursor_pos[1]))

    pg.mouse.set_pos(cursor_pos)
    if pg.joystick.get_count() > 0 and joystick.get_button(1) and  (StartMenu != 0 or inshop):
        prev_cursor_pos = cursor_pos  # Store the previous cursor position
        cursor_pos = pg.mouse.get_pos()
        window_handle = pg.display.get_wm_info()['window']
        window_rect = win32gui.GetWindowRect(window_handle)
        window_pos = (window_rect[0], window_rect[1])
        x = cursor_pos[0] + window_pos[0]
        y = cursor_pos[1] + window_pos[1]
        pyautogui.click(x=x, y=y, button='left')
        pg.mouse.set_pos(prev_cursor_pos)  # Set the position back to the previous cursor position

    pg.mouse.set_visible(False)
    screen.blit(cursor_img, cursor_pos)


    pg.display.update()
pg.quit()
