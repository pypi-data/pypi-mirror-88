import pygame
from random import randrange
from . import tools


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, xpos, SCREEN_HEIGHT, GROUND_HEIGHT, GAME_SPEED):
        pygame.sprite.Sprite.__init__(self)

        self.red_bird = [tools.load_img('animations/RedBird (1).png').convert_alpha(),
                         tools.load_img('animations/RedBird (2).png').convert_alpha(),
                         tools.load_img('animations/RedBird (3).png').convert_alpha(),
                         tools.load_img('animations/RedBird (4).png').convert_alpha()]

        self.vulture = [tools.load_img('animations/Vulture (1).png').convert_alpha(),
                        tools.load_img('animations/Vulture (2).png').convert_alpha(),
                        tools.load_img('animations/Vulture (3).png').convert_alpha(),
                        tools.load_img('animations/Vulture (4).png').convert_alpha()]

        self.green_bird = [tools.load_img('animations/GreenBird (1).png').convert_alpha(),
                           tools.load_img('animations/GreenBird (2).png').convert_alpha(),
                           tools.load_img('animations/GreenBird (3).png').convert_alpha(),
                           tools.load_img('animations/GreenBird (4).png').convert_alpha()]

        self.images = [tools.load_img('snake1.png').convert_alpha(),
                       tools.load_img('barris.png').convert_alpha(),
                       tools.load_img('mouse.png').convert_alpha()]

        self.images[0] = pygame.transform.scale(self.images[0], (40, 70))
        self.images[1] = pygame.transform.scale(self.images[1], (73, 70))

        if GAME_SPEED > 30:
            self.images.append(self.vulture)
        if GAME_SPEED > 40:
            self.images.append(self.green_bird)
        if GAME_SPEED > 50:
            self.images.append(self.red_bird)

        self.range = randrange(0, len(self.images))
        self.current_image = 0
        self.image = self.images[self.range]

        if self.range > 2:
            self.current_list = self.images[self.range]
            self.rect = self.current_list[0].get_rect()
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT - (self.rect[3] * 1.5)

        else:
            self.rect = self.image.get_rect()
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect[3]

        self.rect[0] = xpos

    def update(self, GAME_SPEED):
        if self.range > 2:
            self.current_image = (self.current_image + 1) % len(self.current_list)
            self.image = self.current_list[self.current_image]

        self.rect[0] -= GAME_SPEED
