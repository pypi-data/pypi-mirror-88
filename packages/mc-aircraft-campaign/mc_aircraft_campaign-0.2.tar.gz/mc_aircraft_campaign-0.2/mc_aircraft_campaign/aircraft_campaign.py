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
e1_status = None

e2_act = None
e2_blood = None
e2_status = None
e2_fired = None

score = 0
game_status = 0


def draw():
    global game_status
    bg1.draw()
    bg2.draw()

    if game_status == 0:
        for i in range(10):
            if e1_status[i] < 2:
                if e1_status[i] == 1:
                    if e1_act[i].image != 'boom-7':
                        e1_act[i].image = 'boom-' + str(int(e1_act[i].image[5:]) + 1)
                    else:
                        e1_status[i] = 2
                e1_act[i].draw()

        for i in range(5):
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
        for i in range(10):
            e1_act[i].y += 2
            if e1_act[i].y > 800:
                e1_act[i].y = e1_act[i - 1].y - 300
                e1_act[i].image = 'e1'
                e1_blood[i] = 3
                e1_status[i] = 0

        for i in range(5):
            e2_act[i].y += 2
            if e2_act[i].y > 800:
                e2_act[i].y = e2_act[i - 1].y - 600
                e2_act[i].image = 'e2'
                e2_blood[i] = 6
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
            for i in range(10):
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
            for i in range(5):
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


def config():
    global bg1
    global bg2
    global player
    global bullets_lst
    global bullets2_lst
    global e1_act
    global e1_blood
    global e1_status
    global e2_act
    global e2_blood
    global e2_status
    global e2_fired

    bg_num = randint(1, 5)
    bg1 = Actor('bg' + str(bg_num), topleft=(0, 0))
    bg2 = Actor('bg' + str(bg_num), topleft=(0, -768))
    player = Actor('p1', center=(WIDTH // 2, 700))
    bullets_lst = []
    bullets2_lst = []

    e1_act = [Actor('e1', center=(randint(50, 460), -100 - i * 300)) for i in range(10)]
    e1_blood = [3] * 10
    e1_status = [0] * 10

    e2_act = [Actor('e2', center=(randint(50, 460), -600 - i * 600)) for i in range(5)]
    e2_blood = [6] * 5
    e2_status = [0] * 5
    e2_fired = [0] * 5


music.play('bgm')
