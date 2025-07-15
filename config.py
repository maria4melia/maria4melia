import pygame
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.gameimage import *
from PPlay.collision import *
from config import *
from PPlay.sound import *
import math
import random

# Colors

black = (0,0,0)

# game
display = Window(1356, 775)
display.set_title("Jogo")
fundoNPC = GameImage("assets/mapNPC.png")
fundo = GameImage("assets/map.png")
fundoMenu = GameImage("assets/mapmenu.png")

play_button = GameImage("assets/play.png")
play_button.set_position(display.width/2 - play_button.width/2, display.height/3 - play_button.height/2)


estado = "menu"

witch = Sprite("assets/witch.png",6)
witch.set_position(display.width/2 - witch.width/2, display.height/3 - witch.height/2)
witch.set_sequence_time(0,6,200, True)


lista_upgrades = []
lista_mobs = []

for i in range(3):
    lista_mobs.append([])

lista_remove = []
for i in range(3):
    lista_remove.append([])

wave = 0

portal = False
sprite_portal = Sprite("assets/portal.png")
sprite_portal.set_position(81,83)

upg_vida = Sprite("assets/upg_vida.png")
upg_vida.set_position(display.width/2 + upg_vida.width * 3 - 240, display.height/2 - upg_vida.height/2)

upg_dano = Sprite("assets/upg_dano.png")
upg_dano.set_position(upg_vida.x + 80, upg_vida.y)

upg_vel = Sprite("assets/upg_vel.png")
upg_vel.set_position(upg_vida.x + 160, upg_vida.y)

mouse = Mouse()

sound = Sound("assets/music.ogg")
sound.play()