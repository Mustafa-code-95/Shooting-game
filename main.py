from ursina import Audio
from ursina import camera
from ursina import time
from ursina import application
from ursina import Ursina
from ursina import Entity
from ursina import Text
from ursina import invoke
from ursina import Button
from ursina import color
from ursina import scene
from ursina import clamp
from ursina import destroy
from ursina import held_keys
from ursina import Sky
import random
import threading

app = Ursina()

Sky(texture='feld.png', transparent=False)

background = Entity(
    model='quad',
    texture='feld.png',
    scale=(20, 12),
    z=1
)

rid = 0
score_thread_started = False
game_win = False
d = 0.6
leben = 3
s = 59
y = random.randint(-7, 7)
x = random.randint(-4, 4)
r = 0
er = 0
min_x = -10
max_x = 10
min_y = -6
max_y = 6
name = None
direction = None
herzen = 10
ee = 0
t = ['e', 'm', 'c', 'd']
z = 0
e = ['dieb']
boxes = []
camera.orthographic = True
camera.fov = 5
camera.position = -9, 5
background.z = 10
music = Audio('sound.wav', loop=True, autoplay=True)


def random_name():
    global name
    ran = ['a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü']
    kon = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    name = f'{kon[random.randint(0, len(kon)-1)] + ran[random.randint(0, len(ran)-1)] + kon[random.randint(0, len(kon)-1)] + ran[random.randint(0, len(ran)-1)] + kon[random.randint(0, len(kon)-1)]}'


her = Text('', origin=(0,6), scale=1.2, color=color.white)
leben_text = Text('', origin=(0,2), scale=1.2, color=color.black)
game_over_text = Text('', origin=(0,-1), scale=2.8, color=color.gray)

ziel = Entity(model='cube', color=color.red, scale=0.3, position=(-8, 6), collider='box')
player = Entity(model='cube', color=color.white, scale=5, position=(-7, 4), collider='box', texture='zihl')


def update_score():
    global rid
    if not game_win:
        rid += 1
        invoke(update_score, delay=1)


def add_mob(position, name):
    boxes.append(
        Button(
            parent=scene,
            model='cube',
            origin=0.1,
            color=color.white,
            scale=0.7,
            position=position,
            texture='dieb.png',
            name=name
        )
    )


asa = random.randint(10, 20)

for _ in range(asa):
    y = random.randint(-7, 7)
    x = random.randint(-4, 4)
    random_name()
    add_mob(position=(y, x), name=name)


def update():
    global r, ziel, camera, player, direction, d, game_win, t, z, score_thread_started, rid, s, er, game_over_text, her, name, ee
    r = time.dt
    if not score_thread_started:
        threading.Thread(target=update_score, daemon=True).start()
        score_thread_started = True
    if game_win == True:
        er += 1
        if not rid == 60:
            game_over_text.text = f'The victory\nYou have all monsters killed in {rid}.sek\nClick (q) for quit'
        if held_keys['q']:
            application.quit()
    elif game_win == False:
        if held_keys['a']:
            player.x -= 5 * time.dt
        if held_keys['d']:
            player.x += 5 * time.dt
        if held_keys['s']:
            player.y -= 5 * time.dt
        if held_keys['w']:
            player.y += 5 * time.dt
        camera.position = (player.x, player.y, -20)
        ziel.position = (player.position.x, player.position.y - 0.1)
        if rid > s:
            game_win = True
        for mob in boxes:
            direction = (player.position - mob.position).normalized()
            mob.position -= direction * time.dt * d
            mob.x = clamp(mob.x, min_x + 0.5, max_x - 0.5)
            mob.y = clamp(mob.y, min_y + 0.5, max_y - 0.5)
            if ziel.intersects(mob).hit and ee != 1 and held_keys['space']:
                boxes.remove(mob)
                destroy(mob)
        if boxes == []:
            game_win = True
    player.x = clamp(player.x, min_x + 0.5, max_x - 0.5)
    player.y = clamp(player.y, min_y + 0.5, max_y - 0.5)


def input(key):
    global game_win, camera
    if not game_win:
        if key == 'scroll up':
            camera.fov -= 1
        if key == 'scroll down':
            if not camera.fov > 19:
                camera.fov += 1


app.run()
