import pygame
from pygame.locals import *
from pygame.math import Vector2
from sys import exit
from random import randint

# screen size
SCREEN_SIZE = (400, 600)

# setup
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
font_small = pygame.font.Font("font/Monaco.ttf", 32)
font_big = pygame.font.Font("font/Monaco.ttf", 40)
font_huge = pygame.font.Font("font/Monaco.ttf", 64)

# load images
pic_heart = pygame.image.load('pic/heart.png').convert_alpha()
pic_panda = pygame.image.load('pic/xm.png').convert_alpha()
pic_panda2 = pygame.image.load('pic/xm2.png').convert_alpha()
pic_panda3 = pygame.image.load('pic/xm3.png').convert_alpha()
pic_badball = pygame.image.load('pic/hqq.png').convert_alpha()
pic_fireball = pygame.image.load('pic/fireball.png').convert_alpha()
pic_bulletpacket = pygame.image.load('pic/bulletpacket.png').convert_alpha()
pic_freestyle = pygame.image.load('pic/freestyle_small.png').convert_alpha()
pic_freestyle_l = pygame.image.load('pic/freestyle_large.png').convert_alpha()

# load sounds
sound_fire = pygame.mixer.Sound('sound/fire.ogg')
sound_heart = pygame.mixer.Sound('sound/heart.ogg')
sound_freestyle = pygame.mixer.Sound('sound/freestyle.ogg')
sound_bulletpacket = pygame.mixer.Sound('sound/bulletpacket.ogg')
sound_hurt = pygame.mixer.Sound('sound/hurt.ogg')
sound_boom = pygame.mixer.Sound('sound/boom.ogg')
sound_nobullet = pygame.mixer.Sound('sound/nobullet.ogg')

# init groups
heart_group = pygame.sprite.Group()
badball_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
bulletpacket_group = pygame.sprite.Group()
freestyle_group = pygame.sprite.Group()


class GameItem(pygame.sprite.Sprite):
    def __init__(self, type, image, position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = Vector2(position)
        self.rect.topleft = self.pos
        self.speed = Vector2(speed)
        self.add(globals()[self.type.lower() + '_group'])

    def update(self, time_passed):
        self.pos += self.speed * time_passed
        self.rect.topleft = self.pos
        if self.rect.y > SCREEN_SIZE[1] or self.rect.midbottom[1] < 0:
            self.kill()


class Heart(GameItem):
    def __init__(self, position, speed):
        super(Heart, self).__init__('Heart', pic_heart, position, speed)
        self.radius = 15


class Badball(GameItem):
    def __init__(self, position, speed):
        super(Badball, self).__init__('Badball', pic_badball, position, speed)
        self.radius = 45

    def play_sound_die(self):
        sound_boom.play()


class Fireball(GameItem):
    def __init__(self, position):
        super(Fireball, self).__init__('Fireball', pic_fireball, position, (0, -300))
        self.radius = 6


class BulletPacket(GameItem):
    def __init__(self, position, speed):
        super(BulletPacket, self).__init__('BulletPacket', pic_bulletpacket, position, speed)


class FreeStyle(GameItem):
    def __init__(self, position, speed):
        super(FreeStyle, self).__init__('FreeStyle', pic_freestyle, position, speed)


class Panda(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pic_panda
        self.image_id = 1
        self.rect = self.image.get_rect()
        self.rect.midbottom = position
        self.image_last_time = 300  # ms
        self.freestyle_last_time = 6000  # ms
        self.radius = 30
        self.is_freestyle_mode = False
        self.bullet_num = 10

    def update(self):
        x, y = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        if self.image_id != 1 and current_time - self.image_changed_since > self.image_last_time:
            self.image = pic_panda
            self.image_id = 1
        if self.is_freestyle_mode and current_time - self.freestyle_since > self.freestyle_last_time:
            self.is_freestyle_mode = False
        self.rect.center = (x, self.is_freestyle_mode and y or SCREEN_SIZE[1] - self.image.get_height() / 2)

    def get_heart(self):
        self.image = pic_panda2
        self.image_changed_since = pygame.time.get_ticks()
        self.image_id = 2

    def get_badball(self):
        self.image = pic_panda3
        self.image_changed_since = pygame.time.get_ticks()
        self.image_id = 3

    def get_freestyle(self):
        r = pic_freestyle_l.get_rect()
        r.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
        screen.blit(pic_freestyle_l, r)
        pygame.display.update()
        pygame.time.delay(1000)
        clock.tick()
        self.is_freestyle_mode = True
        self.freestyle_since = pygame.time.get_ticks()

    def shoot(self):
        if self.bullet_num > 0:
            Fireball(self.rect.midtop)
            self.bullet_num -= 1
            self.play_sound('fire')
        else:
            self.play_sound('nobullet')

    def play_sound(self, type):
        globals()['sound_' + type].play()


# init the player
panda_sprite = Panda((SCREEN_SIZE[0] / 2, SCREEN_SIZE[1]))

# collide checker
collide_circle = pygame.sprite.collide_circle_ratio(0.9)


def random_spawn():
    r = randint(1, 100)
    if r >= 100:
        spawn_gameitem('FreeStyle', 450, 550)
    elif r >= 98:
        spawn_gameitem('BulletPacket', 300, 500)
    elif r >= 80:
        spawn_gameitem('Badball', 200, 400)
    else:
        spawn_gameitem('Heart', 100, 400)


def spawn_gameitem(type, speed_y_min=100, speed_y_max=400):
    ItemClass = globals()[type]
    item_width = globals()['pic_' + type.lower()].get_width()
    init_x = randint(0, SCREEN_SIZE[0] - item_width)
    if init_x < (SCREEN_SIZE[0] - item_width) / 2:
        speed_x = randint(0, 60)
    else:
        speed_x = randint(-60, 0)
    speed_y = randint(speed_y_min, speed_y_max)
    ItemClass((init_x, 0), (speed_x, speed_y))


def status_init():
    status = {
        'life':3,
        'scores':0,
        'spawn_speed':3.0,  # entites per second
    }
    heart_group.empty()
    badball_group.empty()
    fireball_group.empty()
    panda_sprite.bullet_num = 10
    return status


def item_update(status, time_passed):
    # update hearts
    heart_group.update(time_passed)
    get_hearts_list = pygame.sprite.spritecollide(panda_sprite, heart_group, True, collided=collide_circle)
    hearts_num = len(get_hearts_list)
    if hearts_num > 0:
        status['scores'] += hearts_num * 100
        status['spawn_speed'] += hearts_num * 0.05
        panda_sprite.get_heart()
        panda_sprite.play_sound('heart')
    # update badballs
    badball_group.update(time_passed)
    get_badballs_list = pygame.sprite.spritecollide(panda_sprite, badball_group, True, collided=collide_circle)
    if len(get_badballs_list) > 0:
        status['life'] -= 1
        panda_sprite.get_badball()
        panda_sprite.play_sound('hurt')
    # update fireballs
    fireball_group.update(time_passed)
    kill_ball_dict = pygame.sprite.groupcollide(fireball_group, badball_group, True, True, collide_circle)
    status['scores'] += len(kill_ball_dict) * 500
    if kill_ball_dict: sound_boom.play()
    # update bulletpackets
    bulletpacket_group.update(time_passed)
    get_bullet_list = pygame.sprite.spritecollide(panda_sprite, bulletpacket_group, True, collide_circle)
    panda_sprite.bullet_num = min(10, panda_sprite.bullet_num + len(get_bullet_list) * 5)
    if get_bullet_list: panda_sprite.play_sound('bulletpacket')
    # update freestyles
    freestyle_group.update(time_passed)
    get_freestyle_list = pygame.sprite.spritecollide(panda_sprite, freestyle_group, True, collide_circle)
    if get_freestyle_list:
        panda_sprite.play_sound('freestyle')
        panda_sprite.get_freestyle()
    # update player
    panda_sprite.update()


def display_update(status):
    screen.fill((255, 255, 255))  # background
    screen.blit(panda_sprite.image, panda_sprite.rect)  # player
    heart_group.draw(screen)  # hearts
    badball_group.draw(screen)  # badballs
    fireball_group.draw(screen)  # fireballs
    bulletpacket_group.draw(screen)  # bulletpackets
    freestyle_group.draw(screen)  # freestyles
    # text update
    score_text = font_big.render(str(status['scores']), True, (20, 20, 20))
    life_text = font_big.render(str(status['life']), True, (219, 77, 109))
    bullet_num_text = font_big.render('{:02}/10'.format(panda_sprite.bullet_num), True, (255, 201, 14))
    # freestyle big timer
    if panda_sprite.is_freestyle_mode:
        ftime_text = font_huge.render(
            '%.3f' % (
                (panda_sprite.freestyle_last_time - pygame.time.get_ticks() + panda_sprite.freestyle_since) / 1000),
            True, (203, 27, 69))
        screen.blit(ftime_text, (SCREEN_SIZE[0] / 2 - ftime_text.get_width() / 2,
                                 SCREEN_SIZE[1] / 2 - ftime_text.get_height() / 2))
    # text display
    screen.blit(score_text, (10, 10))
    screen.blit(life_text, (SCREEN_SIZE[0] - life_text.get_width() - 10, 10))
    screen.blit(bullet_num_text, (10, 15 + score_text.get_height()))
    # final display
    pygame.display.update()


def gameover(status):
    screen.fill((255, 255, 255))
    SCORE_text = font_big.render('SCORE', True, (20, 20, 20))
    scores_text = font_small.render(str(status['scores']), True, (20, 20, 20))
    tryagain_text = font_big.render('AGAIN', True, (251, 150, 110))
    r = tryagain_text.get_rect()
    r.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
    pygame.draw.rect(screen, (219, 77, 109), r)
    screen.blit(SCORE_text, (SCREEN_SIZE[0] / 2 - SCORE_text.get_width() / 2, 100))
    screen.blit(scores_text, (SCREEN_SIZE[0] / 2 - scores_text.get_width() / 2, 100 + SCORE_text.get_height()))
    screen.blit(tryagain_text, r)
    pygame.display.update()

    # wait for try again
    while True:
        event = pygame.event.poll()
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and r.collidepoint(event.pos):
                break


# main
while True:
    status = status_init()
    timer_for_spawn_item = 0.0
    # game loop
    while status['life'] > 0:

        event = pygame.event.poll()
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                panda_sprite.shoot()

        # get the time last frame cost in seconds
        time_passed = clock.tick() / 1000

        # spawn items
        timer_for_spawn_item += time_passed
        if timer_for_spawn_item > 1.0 / status['spawn_speed']:
            random_spawn()
            timer_for_spawn_item = 0

        # updates
        item_update(status, time_passed)
        display_update(status)

    gameover(status)
