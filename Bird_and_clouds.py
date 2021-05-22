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

    #  ---------------------------------- end_game + win ----------------------------------->

    def end_game():
        pygame.mixer.music.load('data/game_over.mp3')
        pygame.mixer.music.play(0, 0.5)
        pygame.time.wait(2700)
        print(5/0)

    def win():
        pygame.display.flip()
        pygame.mixer.music.load('data/win.mp3')
        pygame.mixer.music.play(0)
        pygame.time.wait(6300)
        print(5/0)

    # ------------------------------------ Heart + show_hearts ----------------------------->

    class Heart(pygame.sprite.Sprite):
        def __init__(self, group, x, y):
            super().__init__(group)

            self.image = pygame.transform.scale(load_image('heart.png', -1), (pr(50), pr(48)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def delete(self):
            self.rect.x = width
            self.rect.y = height

    def show_hearts(count):
        hearts.draw(screen)
        if count == 1:
            heart1.delete()
        if count == 2:
            heart2.delete()
        if count >= 3:
            heart3.delete()
