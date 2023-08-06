import os
import sys

from random import *

from pgzero import music
from pgzero.actor import Actor
from pgzero.runner import prepare_mod, set_my_root, run_mod

WIDTH = 512
HEIGHT = 768
TITLE = '飞机大战'
# PATH = "./"
# os.path.abspath(os.path.join("./", ".."))

mod = sys.modules['mc_aircraft_campaign.aircraft_campaign']

if not getattr(sys, '_pgzrun', None):
	if not getattr(mod, '__file__', None):
		raise ImportError(
			"You are running from an interactive interpreter.\n"
			"'import pgzrun' only works when you are running a Python file."
		)
	prepare_mod(mod)


def go():
	"""Run the __main__ module as a Pygame Zero script."""
	mymod = sys.modules['mc_aircraft_campaign.aircraft_campaign']
	set_my_root(getattr(mymod, 'PATH', ''))
	print(getattr(mymod, 'PATH', ''))

	if getattr(sys, '_pgzrun', None):
		return
	run_mod(mod)

bg1 = None
bg2 = None
player = None
bullets_lst = []
bullets2_lst = []

e1_act = None
e1_blood = None
e1_blood_size = 3
e1_status = None
e1_size = 10

e2_act = None
e2_blood = None
e2_blood_size = 6
e2_status = None
e2_fired = None
e2_size = 5
# launch = key.F

player_x = WIDTH//2
player_y = 700
score = 0
game_status = 0


def draw():
    global game_status
    bg1.draw()
    bg2.draw()

    if game_status == 0:
        for i in range(e1_size):
            if e1_status[i] < 2:
                if e1_status[i] == 1:
                    if e1_act[i].image != 'boom-7':
                        e1_act[i].image = 'boom-' + str(int(e1_act[i].image[5:]) + 1)
                    else:
                        e1_status[i] = 2
                e1_act[i].draw()

        for i in range(e2_size):
            if e2_status[i] < 2:
                if e2_status[i] == 1:
                    if e2_act[i].image != 'boom-7':
                        e2_act[i].image = 'boom-' + str(int(e2_act[i].image[5:]) + 1)
                    else:
                        e2_status[i] = 2
                e2_act[i].draw()

        for b in bullets_lst:
            b.draw()

        for b in bullets2_lst:
            b.draw()

    if game_status < 2:
        if game_status == 1:
            if player.image != 'boom-7':
                player.image = 'boom-' + str(int(player.image[5:]) + 1)
            else:
                game_status = 2
        player.draw()

    screen.draw.text('%08d' % score, topright=(500, 10), color=(255, 255, 255), fontsize=30)


def update():
    global score, game_status
    bg1.y += 1
    bg2.y += 1

    if bg1.topleft[1] > 768:
        bg1.y = bg2.y - 768
    if bg2.topleft[1] > 768:
        bg2.y = bg1.y - 768

    if game_status == 0:
        for i in range(e1_size):
            e1_act[i].y += 2
            if e1_act[i].y > 800:
                e1_act[i].y = e1_act[i - 1].y - 300
                e1_act[i].image = 'e1'
                e1_blood[i] = e1_blood_size
                e1_status[i] = 0

        for i in range(e2_size):
            e2_act[i].y += 2
            if e2_act[i].y > 800:
                e2_act[i].y = e2_act[i - 1].y - 600
                e2_act[i].image = 'e2'
                e2_blood[i] = e2_blood_size
                e2_status[i] = 0
                e2_fired[i] = 0
            elif e2_act[i].y > 200 and e2_fired[i] == 0:
                bullets2_lst.append(Actor('bullet-2', center=(e2_act[i].x, e2_act[i].y + 30)))
                e2_fired[i] = 1

        for b in bullets_lst:
            b.y -= 10
            if b.y < -100:
                bullets_lst.remove(b)
                continue
            for i in range(e1_size):
                if e1_act[i].colliderect(b) and e1_status[i] == 0 and b.y > 0:
                    if e1_blood[i] > 1:
                        e1_act[i].y -= 3
                        e1_blood[i] -= 1
                    else:
                        sounds.boom.play()
                        e1_act[i].image = 'boom-1'
                        e1_status[i] = 1
                        score += 100
                    bullets_lst.remove(b)
                    continue
            for i in range(e2_size):
                if e2_act[i].colliderect(b) and e2_status[i] == 0 and b.y > 0:
                    if e2_blood[i] > 1:
                        e2_act[i].y -= 3
                        e2_blood[i] -= 1
                    else:
                        sounds.boom.play()
                        e2_act[i].image = 'boom-1'
                        e2_status[i] = 1
                        score += 200
                    bullets_lst.remove(b)
                    continue

        for b in bullets2_lst:
            b.y += 5
            if b.y > 800:
                bullets2_lst.remove(b)
                continue
            if b.colliderect(player):
                sounds.boom.play()
                player.image = 'boom-1'
                game_status = 1

        if keyboard.left and player.x > player.width // 2:
            player.x -= 5
        if keyboard.right and player.x < WIDTH - player.width // 2:
            player.x += 5
        if keyboard.up and player.y > player.height // 2:
            player.y -= 5
        if keyboard.down and player.y < HEIGHT - player.height // 2:
            player.y += 5


def on_key_down(key):
    if key == key.F and game_status == 0:
        bullets_lst.append(Actor('bullet-1', center=(player.x, player.y - 30)))

def setLaunch(key):
    global launch
    if key is not None:
        launch = key

def setPlayerCoordinate(x, y):
    global player_x, player_y
    if isinstance(x,int):
        player_x = x
    if isinstance(y,int):
        player_y = y

def config(blood_size1, blood_size2, bg_num):
    global bg1
    global bg2
    global player
    global bullets_lst
    global bullets2_lst
    global e1_act
    global e1_blood
    global e1_blood_size
    global e1_status
    global e2_act
    global e2_blood
    global e2_blood_size
    global e2_status
    global e2_fired

    if blood_size1 is not None:
        e1_blood_size = blood_size1
    if blood_size2 is not None:
        e2_blood_size = blood_size2

    if bg_num is None:
        bg_num = randint(1, 5)
    else:
        bg_num = bg_num % 5

    bg1 = Actor('bg' + str(bg_num), topleft=(0, 0))
    bg2 = Actor('bg' + str(bg_num), topleft=(0, -768))
    player = Actor('p1', center=(player_x, player_y))
    bullets_lst = []
    bullets2_lst = []

    e1_act = [Actor('e1', center=(randint(50, 460), -100 - i * 300)) for i in range(e1_size)]
    e1_blood = [e1_blood_size] * e1_size
    e1_status = [0] * e1_size

    e2_act = [Actor('e2', center=(randint(50, 460), -600 - i * 600)) for i in range(e2_size)]
    e2_blood = [e2_blood_size] * e2_size
    e2_status = [0] * e2_size
    e2_fired = [0] * e2_size


music.play('bgm')
