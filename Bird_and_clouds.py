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
            

    # ---------------------------------------- Bird ---------------------------------------->

    class Bird(pygame.sprite.Sprite):
        def __init__(self, group, sheet, columns, rows, fps):
            super().__init__(group)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (pr(75), pr(75)))
            self.rect = self.image.get_rect()
            self.fps = fps

            self.flag1 = False
            self.flag2 = True

            self.clouds = []

            self.mask = pygame.mask.from_surface(self.image)

            self.countTicks = 0

            self.countTicks1 = 0
            self.forgot_sec = 5

        def set_pos(self, x, y):
            self.rect.x = x
            self.rect.y = y

        def check_v(self, v, ticks):
            if self.rect.y >= pr(300):
                self.rect.y -= v * ticks/1000
                return False
            return True

        def check(self, cloud, sc1, sc2):
            self.mask = pygame.mask.from_surface(self.image)

            if pygame.sprite.collide_mask(self, cloud):
                sc1 -= 10000
                if cloud not in self.clouds:
                    sc2 += 1
                    self.clouds.append(cloud)

            return sc1, sc2

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for m in range(columns):
                    frame_location = (self.rect.w * m, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def update(self, ticks, h):

            self.countTicks += ticks

            if self.countTicks > 1000 / self.fps:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.cur_frame], (pr(75), pr(75)))
                self.countTicks = 0

            self.countTicks1 += ticks

            if self.countTicks1 / 1000 > self.forgot_sec:
                try:
                    self.clouds.pop()
                except IndexError:
                    pass
                self.countTicks1 = 0

            if h <= pr(height - height//4 + height//9.19):
                self.rect.y -= v_high * 0.5 * ticks/1000

            if self.rect.y >= height-pr(75):
                end_game()


    # ---------------------------------------- Ground ---------------------------------------->

    class Ground(pygame.sprite.Sprite):
        def __init__(self, group, image, y1, v, ret=False):
            super().__init__(group)
            self.y = height//4
            self.v = v
            self.image = pygame.transform.scale(load_image(image, -1), (pr(5100), pr(y1)))
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.down = height - pr(y1)
            self.rect.y = self.down
            self.pos_x = self.rect.x
            self.pos_y = self.rect.y
            self.ret = ret

        def update(self, ticks, v):
            self.pos_x -= self.v * bird_speed * ticks/1000
            if self.pos_x <= -pr(3550):
                self.pos_x = 0

            self.pos_y += v * self.v * ticks/1000 * 0.5

            if self.pos_y <= self.down:
                self.pos_y = self.down

            self.rect.y = self.pos_y
            self.rect.x = self.pos_x

            if self.ret:
                return self.rect.y
            else:
                return 0

# ---------------------------------------- Cloud ---------------------------------------->

    class Cloud(pygame.sprite.Sprite):
        def __init__(self, group, image, y1, v):
            super().__init__(group)
            k = random.randint(2, 3)
            self.size = 'small' if k < 3 else 'big'
            self.left = 300//k
            self.image = pygame.transform.scale(load_image(image, -1), (pr(300//k), pr(173//k)))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, width)
            self.rect.y = y1
            self.v = v

            self.mask = pygame.mask.from_surface(self.image)

            self.pos_x = self.rect.x
            self.pos_y = self.rect.y

        def update(self, ticks, v):
            self.pos_x -= self.v * bird_speed * ticks / 1000
            if self.pos_x <= -self.left:
                self.pos_x = width

            self.pos_y += v * self.v * ticks / 1000 * 0.5

            self.rect.x = self.pos_x
            self.rect.y = self.pos_y
