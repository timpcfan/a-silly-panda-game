import pygame
from pygame.locals import *
from pygame.math import Vector2
from sys import exit
from random import randint

SCREEN_SIZE = (400, 600)

counter = 0
bullet_num = 5
heart_group = pygame.sprite.Group()
badball_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
bulletpacket_group = pygame.sprite.Group()
spawn_speed = 3  # entites per second
time_to_spawn = 0

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
clock = pygame.time.Clock()
screen_rect = screen.get_rect()
font_small = pygame.font.Font("Monaco.ttf", 32)
font_big = pygame.font.Font("Monaco.ttf", 40)

pic_heart = pygame.image.load('pic/heart.png').convert_alpha()
pic_panda = pygame.image.load('pic/xm.png').convert_alpha()
pic_panda2 = pygame.image.load('pic/xm2.png').convert_alpha()
pic_panda3 = pygame.image.load('pic/xm3.png').convert_alpha()
pic_badball = pygame.image.load('pic/hqq.png').convert_alpha()
pic_fireball = pygame.image.load('pic/fireball.png').convert_alpha()
pic_bullet = pygame.image.load('pic/bullet.png').convert_alpha()


def spawn_entry():
    r = randint(1, 100)
    if r >= 98:
        spawn_bullet()
    elif r >= 80:
        spawn_badball()
    else:
        spawn_hearts()


def spawn_badball():
    global counter
    init_x = randint(0, 300)
    if init_x < 200:
        speed_x = randint(0, 100)
    else:
        speed_x = randint(-100, 0)
    speed_y = randint(200, 400)
    Badball((init_x, 0), (speed_x, speed_y), counter).add(badball_group)
    counter += 1


def spawn_hearts():
    global counter
    init_x = randint(0, 364)
    if init_x < 200:
        speed_x = randint(0, 50)
    else:
        speed_x = randint(-50, 0)
    speed_y = randint(100, 400)
    Heart((init_x, 0), (speed_x, speed_y), counter).add(heart_group)
    counter += 1


def spawn_bullet():
    global counter
    init_x = randint(0, 368)
    if init_x < 200:
        speed_x = randint(0, 100)
    else:
        speed_x = randint(-100, 0)
    speed_y = randint(300, 500)
    BulletPacket((init_x, 0), (speed_x, speed_y)).add(bulletpacket_group)
    counter += 1


class Heart(pygame.sprite.Sprite):
    def __init__(self, position, speed, id):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'heart'
        self.image = pic_heart
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.speed = Vector2(speed)
        self.pos = Vector2(position)
        self.id = id
        self.radius = 15

    def update(self, time_passed):
        self.pos += self.speed * time_passed
        self.rect.topleft = self.pos
        if self.rect.y > SCREEN_SIZE[1]:
            self.remove(heart_group)


class Panda(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pic_panda
        self.image_id = 1
        self.rect = self.image.get_rect()
        self.rect.midbottom = position
        self.image_last_time = 300  # ms
        self.radius = 30

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.midbottom = (x, SCREEN_SIZE[1])
        if self.image_id != 1 and pygame.time.get_ticks() - self.image_changed_time > self.image_last_time:
            self.image = pic_panda
            self.image_id = 1

    def get_heart(self):
        self.image = pic_panda2
        self.image_changed_time = pygame.time.get_ticks()
        self.image_id = 2

    def get_strike(self):
        self.image = pic_panda3
        self.image_changed_time = pygame.time.get_ticks()
        self.image_id = 3

    def shoot(self):
        global counter
        Fireball(self.rect.midtop, counter).add(fireball_group)
        counter += 1



class Badball(pygame.sprite.Sprite):
    def __init__(self, position, speed, id):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'badball'
        self.image = pic_badball
        self.rect = self.image.get_rect()
        self.id = id
        self.speed = Vector2(speed)
        self.pos = Vector2(position)
        self.radius = 45

    def update(self, time_passed):
        self.pos += self.speed * time_passed
        self.rect.topleft = self.pos
        if self.rect.y > SCREEN_SIZE[1]:
            self.remove(badball_group)



class Fireball(pygame.sprite.Sprite):
    def __init__(self, position, id):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'fire'
        self.image = pic_fireball
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.id = id
        self.speed = Vector2((0, -300))
        self.pos = position
        self.radius = 6

    def update(self, time_passed):
        self.pos += self.speed * time_passed
        self.rect.topleft = self.pos
        if self.rect.y < 0:
            self.remove(fireball_group)


class BulletPacket(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'bulletpacket'
        self.image = pic_bullet
        self.rect = self.image.get_rect()
        self.rect.topleft = Vector2(position)
        self.speed = Vector2(speed)
        self.pos = Vector2(position)

    def update(self, time_passed):
        self.pos += self.speed * time_passed
        self.rect.topleft = self.pos
        if self.rect.y > SCREEN_SIZE[1]:
            self.remove(bulletpacket_group)




# the player
panda_sprite = Panda((SCREEN_SIZE[0] / 2, SCREEN_SIZE[1]))

# collide checker
collide_circle = pygame.sprite.collide_circle_ratio(0.9)

while True:
    life = 3
    scores = 0
    counter = 0
    bullet_num = 10
    heart_group.empty()
    badball_group.empty()
    spawn_speed = 3  # entites per second
    time_to_spawn = .0
    while life > 0:

        event = pygame.event.poll()
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if bullet_num > 0:
                    panda_sprite.shoot()
                    bullet_num -= 1

        time_passed = clock.tick() / 1000

        time_to_spawn += time_passed
        if time_to_spawn > 1.0 / spawn_speed:
            spawn_entry()
            time_to_spawn = 0

        heart_group.update(time_passed)
        get_hearts_list = pygame.sprite.spritecollide(panda_sprite, heart_group, True, collided=collide_circle)
        hearts_num = len(get_hearts_list)
        if hearts_num > 0:
            scores += hearts_num * 100
            spawn_speed += hearts_num * 0.05
            panda_sprite.get_heart()

        badball_group.update(time_passed)
        get_badballs_list = pygame.sprite.spritecollide(panda_sprite, badball_group, True, collided=collide_circle)
        if len(get_badballs_list) > 0:
            life -= 1
            panda_sprite.get_strike()

        fireball_group.update(time_passed)
        kill_ball_dict = pygame.sprite.groupcollide(fireball_group, badball_group, True, True, collide_circle)
        scores += len(kill_ball_dict) * 500


        bulletpacket_group.update(time_passed)
        get_bullet_list = pygame.sprite.spritecollide(panda_sprite, bulletpacket_group, True, collide_circle)
        bullet_num += len(get_bullet_list) * 5
        if bullet_num > 10:
            bullet_num = 10

        panda_sprite.update()
        score_text = font_big.render(str(scores), True, (20, 20, 20))
        life_text = font_big.render(str(life), True, (219, 77, 109))
        bullet_num_text = font_big.render('{:02}/10'.format(bullet_num), True, (255, 201, 14))

        # display update
        screen.fill((255, 255, 255))
        screen.blit(panda_sprite.image, panda_sprite.rect)
        # blit group
        heart_group.draw(screen)
        badball_group.draw(screen)
        fireball_group.draw(screen)
        bulletpacket_group.draw(screen)
        # blit text
        screen.blit(score_text, (10, 10))
        screen.blit(life_text, (SCREEN_SIZE[0] - life_text.get_width() - 10, 10))
        screen.blit(bullet_num_text, (10, 15 + score_text.get_height()))
        pygame.display.update()

    screen.fill((255, 255, 255))
    SCORE_text = font_big.render('SCORE', True, (20, 20, 20))
    scores_text = font_small.render(str(scores), True, (20, 20, 20))
    tryagain_text = font_big.render('AGAIN', True, (251, 150, 110))
    r = tryagain_text.get_rect()
    r.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
    pygame.draw.rect(screen, (219, 77, 109), r)
    screen.blit(SCORE_text, (SCREEN_SIZE[0] / 2 - SCORE_text.get_width() / 2, 100))
    screen.blit(scores_text, (SCREEN_SIZE[0] / 2 - scores_text.get_width() / 2, 100 + SCORE_text.get_height()))
    screen.blit(tryagain_text, r)
    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == QUIT:
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and r.collidepoint(event.pos):
                break

