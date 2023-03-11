import sys
import pygame
from sys import exit
from random import randint, uniform

def laser_update(laser_list,speed = 300):
    for rect in laser_list:
        rect.y -= speed *dt
        if rect.bottom < 0:
            laser_list.remove(rect)



def metor_update(metor_list,speed = 300):
    for metor_tuple in metor_list:
        direction = metor_tuple[1]
        metor_rect = metor_tuple[0]
        metor_rect.center += direction * speed *dt
        if metor_rect.top > WINDOW_HEIGHT:
            metor_list.remove(metor_tuple)




def display_score():
    score_text = f'score:{pygame.time.get_ticks()//1000}'
    text_surf = font.render( score_text,True, (255, 255, 255))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width=10, border_radius=5)


def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True

    return(can_shoot)

#surface game
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Astro Shooter')
clock = pygame.time.Clock()

#imported images
ship_surf = pygame.image.load('.\graphics\ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
bg_surf = pygame.image.load('.\graphics\groundback.png').convert()
laser_surf = pygame.image.load('.\graphics\laser.png').convert_alpha()


#metor image
metor_surf = pygame.image.load('.\graphics\meteor.png').convert_alpha()

laser_list = []
metor_list = []

can_shoot = True
shoot_time = None





#impot fonts for text in game
font = pygame.font.Font('.\graphics\subatomic.ttf', 50)







#metor timer
metor_timer = pygame.event.custom_type()
pygame.time.set_timer(metor_timer, 500)


laser_sound = pygame.mixer.Sound('.\sounds\laser.ogg')
explosion_sound = pygame.mixer.Sound('.\sounds\explosion.wav')
background_music = pygame.mixer.Sound('.\sounds\music.wav')
background_music.play(loops= -1)

# 1. input -> events (mouse click, mouse movement, press of a button, controller or touchscreen)
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            #Laser
            laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)
            can_shoot=False
            shoot_time = pygame.time.get_ticks()

            # laser sound
            laser_sound.play()

        if event.type == metor_timer:
            x_pos = randint (-100, WINDOW_WIDTH + 100)
            y_pos = randint(-100, -50)
            metor_rect = metor_surf.get_rect(center = (x_pos,y_pos))
            direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
            metor_list.append((metor_rect, direction))



        dt= clock.tick(120) /1000


#mouse input
        ship_rect.center = pygame.mouse.get_pos()

#laser move
        laser_update(laser_list)
        metor_update(metor_list)
        can_shoot = laser_timer(can_shoot, 500)


#metor ship collisions
        for metor_tuple in metor_list:
            metor_rect = metor_tuple[0]
            if ship_rect.colliderect(metor_rect):
                pygame.quit()
                sys.exit()


# laser metor collision
        for laser_rect in laser_list:
            for metor_tuple in metor_list:
                if laser_rect.colliderect(metor_tuple[0]):
                    metor_list.remove(metor_tuple)
                    laser_list.remove(laser_rect)
                    explosion_sound.play()


   # 2. update dates
    display_surface.fill((0, 0, 0))
    display_surface.blit(bg_surf,(0,0))

#display metors




    display_score()




    for rect in laser_list:
        display_surface.blit(laser_surf,rect)
        display_surface.blit(ship_surf, ship_rect)

    for metor_tuple in metor_list:
        display_surface.blit(metor_surf,metor_tuple[0])





# 3. show the frame to the player / update the display surface
    pygame.display.update()
