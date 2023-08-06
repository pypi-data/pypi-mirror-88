import pygame
from . import tools


class Donkey(pygame.sprite.Sprite):
    def __init__(self, MIN_HEIGHT, SPEED_JUMP):
        pygame.sprite.Sprite.__init__(self)

        self.images_walk = [tools.load_img('animations/Walk (1).png').convert_alpha(),
                            tools.load_img('animations/Walk (2).png').convert_alpha(),
                            tools.load_img('animations/Walk (3).png').convert_alpha(),
                            tools.load_img('animations/Walk (4).png').convert_alpha(),
                            tools.load_img('animations/Walk (5).png').convert_alpha(),
                            tools.load_img('animations/Walk (6).png').convert_alpha()]

        self.images_jump = [tools.load_img('animations/Jump (1).png').convert_alpha(),
                            tools.load_img('animations/Jump (2).png').convert_alpha(),
                            tools.load_img('animations/Jump (3).png').convert_alpha(),
                            tools.load_img('animations/Jump (4).png').convert_alpha(),
                            tools.load_img('animations/Jump (5).png').convert_alpha()]

        self.images_not = [tools.load_img('animations/Not (1).png').convert_alpha(),
                           tools.load_img('animations/Not (2).png').convert_alpha(),
                           tools.load_img('animations/Not (3).png').convert_alpha(),
                           tools.load_img('animations/Not (4).png').convert_alpha(),
                           tools.load_img('animations/Not (5).png').convert_alpha()]

        self.images_happy = [tools.load_img('animations/Happy (1).png').convert_alpha(),
                           tools.load_img('animations/Happy (2).png').convert_alpha(),
                           tools.load_img('animations/Happy (3).png').convert_alpha(),
                           tools.load_img('animations/Happy (4).png').convert_alpha(),
                           tools.load_img('animations/Happy (5).png').convert_alpha(),
                           tools.load_img('animations/Happy (6).png').convert_alpha(),
                           tools.load_img('animations/Happy (7).png').convert_alpha(),
                           tools.load_img('animations/Happy (8).png').convert_alpha()]

        self.jump_sound = tools.load_sound('jump_sound.wav', 0.3)
        self.speed = SPEED_JUMP
        self.isJumping = False
        self.isHappy = False
        self.isSad = False
        self.n = -1
        self.IMAGE_INTERVAL = 110
        self.last_update = 0
        self.current_image = 0
        self.current_list = self.images_walk
        self.image = tools.load_img('original.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[0] = 20
        self.rect[1] = MIN_HEIGHT

    def update(self, GRAVITY, MIN_HEIGHT):
        if self.isJumping:
            self.current_list = self.images_jump
        elif self.isSad:
            self.current_list = self.images_not
        elif self.isHappy:
            self.current_list = self.images_happy
        else:
            self.current_list = self.images_walk

        if self.current_list == self.images_jump:
            if pygame.time.get_ticks() - self.last_update > self.IMAGE_INTERVAL:
                self.current_image = (self.current_image + 1) % len(self.current_list)
                self.image = self.current_list[self.current_image]
                self.last_update = pygame.time.get_ticks()
        elif self.current_list == self.images_walk or self.current_list == self.images_happy:
            self.current_image = (self.current_image + 1) % len(self.current_list)
            self.image = self.current_list[self.current_image]
        else:
            if self.current_image == 4 or self.current_image == 0:
                self.n *= -1
            self.current_image = (self.current_image + self.n)
            self.image = self.current_list[self.current_image]

        self.speed += GRAVITY
        self.rect[1] += self.speed

        if self.rect[1] > MIN_HEIGHT:
            if self.isSad:
                self.rect[1] = 267
            elif self.isHappy:
                self.rect[1] = 235
            else:
                self.rect[1] = MIN_HEIGHT
                self.speed = 0
                self.isJumping = False

    def jump(self, SPEED_JUMP, MIN_HEIGHT):
        if self.rect[1] == MIN_HEIGHT:
            self.jump_sound.play()
            self.speed -= SPEED_JUMP
            self.current_image = 0
            self.isJumping = True

    def down(self, SPEED_JUMP, MIN_HEIGHT, GRAVITY):
        if self.rect[1] < MIN_HEIGHT:
            self.speed += SPEED_JUMP + GRAVITY

    def sad(self, NEW_HI):
        self.rect[0] = 370

        if NEW_HI:
            self.isHappy = True
        else:
            self.isSad = True
