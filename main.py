import sys

import pygame, random

pygame.init()

Screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

bg_img = pygame.image.load('background.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (800, 600))

ship = pygame.image.load('ship.png').convert_alpha()
# Rotate
# ship = pygame.transform.rotate(ship, 180)
ship_rect = ship.get_rect(midbottom=(400, 500))

laser = pygame.image.load('laser.png').convert_alpha()
laser_list = []


text = pygame.font.Font('subatomic.ttf', 50)


test_rect = pygame.Rect(100, 100, 300, 400)


can_shoot = True

def display_score():
    text_surf = text.render(f'Score:{pygame.time.get_ticks() // 1000}', True, 'white')
    text_rect = text_surf.get_rect(midbottom=(400, 300))
    Screen.blit(text_surf, text_rect)
    # Search for the inflate method
    pygame.draw.rect(Screen, 'white', text_rect.inflate(30, 30), width=10, border_radius=10)

def shooting_time(can_shoot):
    if can_shoot == False:
        current_time = pygame.time.get_ticks()
        if current_time - start_time > 500:
            can_shoot = True
    return can_shoot




meteor_img = pygame.image.load('meteor.png').convert_alpha()
meteor_list = []


meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 1000)


# Sounds

laser_sound = pygame.mixer.Sound('laser.ogg')
explosion_sound = pygame.mixer.Sound('explosion.wav')
bg_music = pygame.mixer.Sound('music.wav')
bg_music.play(loops=-1)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event. type == meteor_timer:
            x_pos = random.randint(-100, 900)
            y_pos = random.randint(-100, -50)
            meteor_rect = meteor_img.get_rect(center=(x_pos, y_pos))
            direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
            meteor_list.append((meteor_rect, direction))

        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser.get_rect(midbottom=(ship_rect.midtop))
            laser_list.append(laser_rect)
            laser_sound.play()

            can_shoot = False
            start_time = pygame.time.get_ticks()


    dt = clock.tick(120) / 1000

    Screen.blit(bg_img, (0, 0))

    for laser_rect in laser_list:
        Screen.blit(laser, laser_rect)
        laser_rect.top -= round(300 * dt)
        if laser_rect.bottom < 0:
            laser_list.remove(laser_rect)

    for tuple in meteor_list:
        Screen.blit(meteor_img, tuple[0])
        direction = tuple[1]
        meteor_rect = tuple[0]
        meteor_rect.center += direction * 200 * dt
        if meteor_rect.y > 600:
            meteor_list.remove(tuple)

    display_score()
    Screen.blit(ship, ship_rect)

    # Checking ship collisions
    for tuple in meteor_list:
        meteor_rect = tuple[0]
        if ship_rect.colliderect(meteor_rect):
           pygame.quit()
           sys.exit()

        for laser_rect in laser_list:
            if laser_rect.colliderect(meteor_rect):
                meteor_list.remove(tuple)
                laser_list.remove(laser_rect)
                explosion_sound.play()

    can_shoot = shooting_time(can_shoot)

    ship_rect.center = pygame.mouse.get_pos()

    pygame.display.update()
