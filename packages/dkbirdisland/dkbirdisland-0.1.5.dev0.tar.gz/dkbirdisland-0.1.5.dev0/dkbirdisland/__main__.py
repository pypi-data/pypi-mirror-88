import pygame
from .src import menus

screen = pygame.display.set_mode((800, 350))


def main():
    menus.menu(screen)


if __name__ == '__main__':
    main()
