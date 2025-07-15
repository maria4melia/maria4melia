import pygame
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *
from PPlay.gameimage import *
from PPlay.collision import *
from config import *

from entities import *


def update_tiros(player):
    
    tempo = display.time_elapsed()
    if Keyboard().key_pressed("SPACE") and (tempo - player.tempo_ultimo >= player.recarga):
        player.tiros.append(PlayerAtirar(player))
        player.tempo_ultimo = display.time_elapsed()

    tiros_a_remover = set()

    for tiro in player.tiros:
        tiro.tiro_update() 

        if (tiro.tiro.x < -tiro.tiro.width or tiro.tiro.x > display.width or tiro.tiro.y < -tiro.tiro.height or tiro.tiro.y > display.height):
            tiros_a_remover.add(tiro)

        for mob in lista_mobs[0]:
            if tiro.tiro.collided(mob.slime):
                lista_remove[0].append(mob)
                tiros_a_remover.add(tiro)
                Slime.dano(mob)
        for mob in lista_mobs[1]:
            if tiro.tiro.collided(mob.wolf):
                tiros_a_remover.add(tiro)
                Wolf.dano(mob)
        for mob in lista_mobs[2]:
            if tiro.tiro.collided(mob.boss):
                tiros_a_remover.add(tiro)
                Boss.dano(mob)



    if tiros_a_remover:
        player.tiros = [tiro for tiro in player.tiros if tiro not in tiros_a_remover]

def update_mobs():
    global wave, portal
    if wave != 0:
        if not any(lista_mobs):
            if portal == True:
                sprite_portal.draw()
                
            elif wave % 5 == 0:
                for i in range(wave//5):
                    Boss.criarBoss()
                    for i in range(wave*2):
                        Slime.criarSlime()
                portal = True
                wave += 1
            elif wave <= 2:
                for i in range(wave*2):
                    Slime.criarSlime()
                wave += 1
            elif wave > 2:
                for i in range(wave*2):
                    Slime.criarSlime()
                for i in range(wave*1):
                    Wolf.criarWolf()
                wave += 1
               
            

    for slime in lista_mobs[0]:
        slime.slime.update()
        Slime.main(slime)
        slime.slime.draw()
    
    
    for wolf in lista_mobs[1]:
        wolf.wolf.update()
        Wolf.main(wolf)
        wolf.wolf.draw()
     
    for boss in lista_mobs[2]:
        boss.boss.update()
        Boss.main(boss)
        boss.boss.draw()

def npc():
    global portal, estado
    fundoNPC.draw()
    witch.update()
    witch.draw()
    sprite_portal.draw()

    if player.sprite.collided(witch):
        upg_vida.draw()
        upg_dano.draw()
        upg_vel.draw()
        
        if checar_click(upg_vida) and player.exp >= 200 and player.maxVida <= 1200:
            player.maxVida += 10
            player.vida = player.maxVida
            player.exp -= 200
            
        if checar_click(upg_vel) and player.exp >= 200:
            player.speed += 10
            player.exp -= 200
            
        if checar_click(upg_dano) and player.exp >= 200:
            player.dano += 5
            player.exp -= 200
            

    if player.sprite.collided(sprite_portal):
        portal = False
        estado = "play"
        sprite_portal.set_position(81,83)

    player.main()
    update_tiros(player)

    HUD.hp()
    display.draw_text(f"exp: {player.exp}", display.width - 100, 10, 20, (255, 255, 255))
    display.update()

def checar_click(button):
    if mouse.is_button_pressed(1) and mouse.is_over_area((button.x,button.y),(button.x + button.width,button.y + button.height)):
        return True


while True:
    
    while estado == "menu":
        player.morre = 0
        fundoMenu.draw()
        play_button.draw()

        if checar_click(play_button):
            player.reset()
            for mob_list in lista_mobs:
                mob_list.clear()
            wave = 1
            portal = False
            estado = "play"

        display.update()

    while estado == "npc":
        npc()

    while estado == "play":
        fundo.draw()
        if player.sprite.collided(sprite_portal) and portal == True and any(lista_mobs) == False:
            estado = "npc"
            sprite_portal.set_position(81, 666)
            portal = False
            player.vida = player.maxVida
            
        player.main()
        update_mobs()
        player.status_update()
        update_tiros(player)


        HUD.hp()
        display.draw_text(f"exp: {player.exp}", display.width - 100, 10, 20, (255, 255, 255))
        display.update()
        if player.morre == 1:
            player.reset()
            estado = "menu"


