import pygame
import os
import random


def game():
    # ------------------------------------- Start + pr ------------------------------------->

    pygame.mixer.music.load('data/main.mp3')
    pygame.mixer.music.play(-1)

    pygame.init()

    birds = pygame.sprite.Group()
    grounds = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    hearts = pygame.sprite.Group()

    w = 1500  # МОЖНО ИЗМЕНЯТЬ
    win_level = 5000  # МОЖНО ИЗМЕНЯТЬ

    size = width, height = w, int(w/1.875)
    screen = pygame.display.set_mode(size)

    def pr(n):
        return int(n/(1500/width))

    bird_speed = pr(200)

    # ------------------------------------- load_image ------------------------------------->

    def load_image(name, color_key=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname).convert()
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image

