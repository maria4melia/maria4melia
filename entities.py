import pygame
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.gameimage import *
from PPlay.collision import *
from config import *
import math
import random
from config import *

# HUD

class HUD:
    def __init__(self):
        pass
    def main(self):
        self.hp()
    def hp():
        pygame.draw.rect(display.screen, (255, 0, 0), (10, display.height - 30, player.vida * 2, 20))


# Player 

class Player:
    def __init__(self):
        self.sprite = Sprite("assets/player.png",17)
        self.sprite.set_sequence_time(0,1,100, True)
        self.sprite.set_position(display.width/2 - self.sprite.width/2,display.height/2-self.sprite.width/2)
        self.tempo_ultimo = 0
        self.recarga = 200
        self.vida = 100
        self.speed = 200
        self.tiros = []
        self.t_vel = 500
        self.direcao = 0
        self.invuneravelCD = 5000
        self.exp = 10000
        self.dano = 10
        self.maxVida = 100
        self.morre = 0

    def status_update(self):
        self.invuneravelCD -= 10
    
    def receberDano(self, dano):
        if self.invuneravelCD <= 0:
            self.vida -= dano
            self.invuneravelCD = 5000
        if self.vida <= 0: 
            self.morre = 1
        

    def reset(self):
        self.sprite.set_position(display.width/2 - self.sprite.width/2,display.height/2-self.sprite.width/2)
        self.exp = 0
        self.dano = 10
        self.maxVida = 100
        self.vida = 100
        self.speed = 200
        self.tiros = []
        self.invuneravelCD = 0

    def movimento(self):

        if Keyboard().key_pressed("W"):
            self.sprite.move_y(-self.speed * display.delta_time())
            if not self.direcao == 1:
                self.direcao = 1
                self.sprite.set_sequence_time(1,9,100, True)
        elif Keyboard().key_pressed("S"):
            self.sprite.move_y(self.speed * display.delta_time())
            if not self.direcao == 2:
                self.direcao = 2
                self.sprite.set_sequence_time(9,17,100, True)
        if Keyboard().key_pressed("D"):
            self.sprite.move_x(self.speed * display.delta_time())
            if not self.direcao == 3:
                self.direcao = 3
                self.sprite.set_sequence_time(1,9,100, True)
                
        elif Keyboard().key_pressed("A"):
            self.sprite.move_x(-self.speed * display.delta_time())
            if not self.direcao == 4:
                self.direcao = 4
                self.sprite.set_sequence_time(9,17,100, True)
                
        

    def colisao(self):
        if self.sprite.x >= display.width - self.sprite.width:
            self.sprite.x = display.width - self.sprite.width
        if self.sprite.x <= 0:
            self.sprite.x = 0
        if self.sprite.y >= display.height - self.sprite.height:
            self.sprite.y = display.height - self.sprite.height
        if self.sprite.y <= 0:
            self.sprite.y = 0
           


    def main(self):
        self.movimento()
        self.colisao()
        self.sprite.update()
        self.sprite.draw()
        self.status_update()

class Clone:

    def __init__(self):
        self.sprite = Sprite("assets/player.png",17)
        self.sprite.set_sequence_time(1,9,200, True)
        self.sprite.set_position(display.width/2 - self.sprite.width/2,display.height/2-self.sprite.width/2)
        self.tempo_ultimo = 0
        self.recarga = 200
        self.vida = 100
        # self.speed = 200
        self.tiros = []
        self.t_vel = 500
        # self.direcao = 0

    def main(self):
        self.sprite.update()
        self.sprite.draw()



player = Player()
player.sprite.set_sequence_time(1,9,100, True)


class PlayerAtirar:
    def __init__(self, player):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.player = player
        self.angle = math.atan2(player.sprite.y - mouse_y, player.sprite.x - mouse_x)
        self.t_vel = player.t_vel
        self.x_vel = math.cos(self.angle) * self.t_vel
        self.y_vel = math.sin(self.angle) * self.t_vel
        self.tiro = Sprite("assets/tiro.png",6)
        self.tiro.set_sequence_time(0,6,100, True)
        self.tiro.set_position(player.sprite.x,player.sprite.y)
    def tiro_update(self):
        self.tiro.x -= self.x_vel * display.delta_time()
        self.tiro.y -= self.y_vel * display.delta_time()
        self.tiro.update()
        self.tiro.draw()
        
class Slime:
    def __init__(self):
        self.vel = 120    
        self.slime = Sprite("assets/slime.png",4)
        self.slime.set_sequence_time(0,4,100, True)
        self.slime.set_position(random.randrange(0,display.width),random.randrange(0,display.height))
        self.reset_offset = 0
        self.offset_x = random.randrange(-500, 500)
        self.offset_y = random.randrange(-500, 500)
        self.dano = 10
        self.vida = 10

    def criarSlime():
        lista_mobs[0].append(Slime())

    def movimento(self):
        if self.reset_offset == 0:
            self.offset_x = random.randrange(-500, 500)
            self.offset_y = random.randrange(-500, 500)
            self.reset_offset = random.randrange(100, 150)
        else:
            self.reset_offset -= 1

        if player.sprite.x + self.offset_x > self.slime.x:
            self.slime.x += self.vel * display.delta_time()
        elif player.sprite.x + self.offset_x < self.slime.x:
            self.slime.x -= self.vel * display.delta_time()
        if player.sprite.y + self.offset_y > self.slime.y:
            self.slime.y += self.vel * display.delta_time()
        elif player.sprite.y + self.offset_y < self.slime.y:
            self.slime.y -= self.vel * display.delta_time()
        
    def main(self):
       
        self.movimento()
        if self.slime.collided(player.sprite):
            player.receberDano(self.dano)

    def dano(self):
        self.vida -= player.dano
        if self.vida <= 0:
            lista_mobs[0].remove(self)
            player.exp += 10


class Wolf:
    def __init__(self):
        self.vel = 120    
        self.wolf = Sprite("assets/wolf2.png",16)
        self.wolf.set_sequence_time(0,8,100, True)
        self.wolf.set_position(random.randrange(0,display.width),random.randrange(0,display.height))
        self.reset_offset = 0
        self.offset_x = random.randrange(-500, 500)
        self.offset_y = random.randrange(-500, 500)
        self.dano = 20
        self.vida = 30
        if player.sprite.x > self.wolf.x:
            self.direcao = 2
            self.wolf.set_sequence_time(0,8,100, True)
        else:
            self.direcao = 1
            self.wolf.set_sequence_time(8,16,100, True)

    def movement(self):
        if player.sprite.x > self.wolf.x:
            self.wolf.x += self.vel * display.delta_time()
            if not self.direcao == 2:
                self.direcao = 2
                self.wolf.set_sequence_time(0,8,100, True)

        elif player.sprite.x < self.wolf.x:
            self.wolf.x -= self.vel * display.delta_time()
            if not self.direcao == 1:
                self.direcao = 1
                self.wolf.set_sequence_time(8,16,100, True)
        if player.sprite.y > self.wolf.y:
            self.wolf.y += self.vel * display.delta_time()
        elif player.sprite.y < self.wolf.y:
            self.wolf.y -= self.vel * display.delta_time()
        

    def criarWolf():
        lista_mobs[1].append(Wolf())
    
    def dano(self):
        self.vida -= player.dano
        if self.vida <= 0:
            lista_mobs[1].remove(self)
            player.exp += 15
        


    def main(self):
        self.movement()
        if self.wolf.collided(player.sprite):
            player.receberDano(self.dano)

        pass

class Boss:
    def __init__(self):
        self.vel = 120    
        self.boss = Sprite("assets/boss.png",10)
        self.boss.set_sequence_time(0,5,100, True)
        self.boss.set_position(random.randrange(0,display.width),random.randrange(0,display.height))
        self.reset_offset = 0
        self.offset_x = random.randrange(-500, 500)
        self.offset_y = random.randrange(-500, 500)
        self.dano = 40
        self.vida = 100
        if player.sprite.x > self.boss.x:
            self.direcao = 1
            self.boss.set_sequence_time(5,10,100, True)
        else:
            self.direcao = 2
            self.boss.set_sequence_time(0,5,100, True)

    def criarBoss():
        lista_mobs[2].append(Boss())

    def dano(self):
        self.vida -= player.dano
        if self.vida <= 0:
            lista_mobs[2].remove(self)

    def movimento(self):
        if player.sprite.x - player.sprite.width/2 > self.boss.x + self.boss.width/2:
            self.boss.x += self.vel * display.delta_time()
            if not self.direcao == 1:
                self.direcao = 1
                self.boss.set_sequence_time(5,10,100, True)
        elif player.sprite.x - player.sprite.width/2 < self.boss.x + self.boss.width/2:
            self.boss.x -= self.vel * display.delta_time()
            if not self.direcao == 2:
                self.direcao = 2
                self.boss.set_sequence_time(0,5,100, True)
        if player.sprite.y > self.boss.y:
            self.boss.y += self.vel * display.delta_time()
        elif player.sprite.y < self.boss.y:
            self.boss.y -= self.vel * display.delta_time()


    def main(self):
        self.movimento()

        if self.boss.collided(player.sprite):
            player.receberDano(self.dano)
