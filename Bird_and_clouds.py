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

    # ---------------------------------------- Wall ---------------------------------------->

    class Wall(pygame.sprite.Sprite):
        def __init__(self, group, image, y1):
            super().__init__(group)
            self.image = pygame.transform.scale(load_image(image, -1), (pr(1768), pr(172)))
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = y1
            self.pos_x = self.rect.x
            self.pos_y = self.rect.y

        def update(self, ticks, v):
            self.pos_x -= bird_speed * ticks / 1000
            if self.pos_x <= -pr(147):
                self.pos_x = 0

            self.pos_y += v * ticks / 1000 * 0.4

            self.rect.x = self.pos_x
            self.rect.y = self.pos_y

            if self.rect.y >= pr(height // 2 - height // 8 - pr(172) + pr(75/2)):
                end_game()

            return self.rect.y

    # ---------------------------------------- Settings ---------------------------------------->

    score = 0
    score1 = 0
    sc = 0
    flag1 = False
    flag_h = 0

    Ground(grounds, "fon4.png", 325, 0.25)
    Ground(grounds, "fon3.png", 239, 0.5)
    Ground(grounds, "fon1.png", 158, 0.75)
    Ground(grounds, "fon2.png", 113, 1, True)

    for _ in range(20):
        Cloud(clouds, 'cloud3.png', random.randint(-height, 0), random.random()+0.25)

    Cloud(clouds, 'cloud3.png', height // 2 - height // 8 - pr(172) + pr(75/2), random.random()+0.25)
    Cloud(clouds, 'cloud3.png', height // 2 - height // 8 - pr(172) + pr(75), random.random()+0.25)

    wall = Wall(clouds, 'wall2.png', -height)

    bird = Bird(birds, load_image("bird3.png", -1), 3, 3, 10)
    bird.set_pos(width // 10, height // 2 - height // 8)

    clock = pygame.time.Clock()
    running = True

    v_high = 0

    fon = load_image('fon5.png')

    heart1 = Heart(hearts, width-width//7, pr(30))
    heart2 = Heart(hearts, width-width//7+width//20, pr(30))
    heart3 = Heart(hearts, width-width//7+width//10, pr(30))

    # ---------------------------------------- running ---------------------------------------->

    while running:
        bird.vy = pr(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag1 = True
                if event.key == pygame.K_c and event.mod == 1:
                    score += 1000
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                flag1 = False

        clk = clock.tick(60)

        if flag1:
            bird_speed += pr(250) * clk / 1000
            if v_high < pr(200):
                v_high += pr(700) * clk / 1000
            wall.rect.y += v_high * clk / 1000
            a = bird.check_v(v_high, clk)
            if not a:
                v_high = 0

        screen.blit(fon, (0, 0), fon.get_rect())

        for i in grounds:
            flag_h = i.update(clk, v_high)

        for i in clouds:
            sc = i.update(clk, v_high)

        if bird_speed > pr(200):
            bird_speed -= pr(5)
        if v_high > -pr(150):
            v_high -= pr(10)

        if sc:
            score += (((sc + 1500) * clk // 10000) * 10 ** 3) // 1000

        if score < 0:
            score = 0

        font1 = pygame.font.Font(None, int(width / 18.75))

        string_rendered1 = font1.render(str(score), 1, (230, 168, 14))
        intro_rect1 = string_rendered1.get_rect()
        intro_rect1.y = pr(30)
        intro_rect1.x = width - width // 3

        for i in clouds:
            score, score1 = bird.check(i, score, score1)
        bird.update(clk, flag_h)
        grounds.draw(screen)
        birds.draw(screen)
        clouds.draw(screen)
        show_hearts(score1)
        screen.blit(string_rendered1, intro_rect1)

        pygame.display.flip()

        if score1 >= 3:
            end_game()
        if score >= win_level:
            win()

    pygame.quit()


pygame.init()

size1 = width1, height1 = 1500, int(1500/1.875)
screen1 = pygame.display.set_mode(size1)

ans = True
while ans:
    try:
        game()
    except ZeroDivisionError:
        pik = True
        while pik:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                if ev.type == pygame.MOUSEBUTTONDOWN and width1//2-width1//7 < ev.pos[0] < \
                        width1//2-width1//7 + width1//3.5 and height1//2-height1//10 + height1//5 \
                        > ev.pos[1] > height1//2-height1//10:
                    pik = False
            pygame.draw.rect(screen1, (154, 154, 154),
                             (width1//2-width1//7, height1//2-height1//10, width1//3.5, height1//5))

            font2 = pygame.font.Font(None, 60)

            string_rendered2 = font2.render('Начать заново', 1, (0, 0, 0))
            intro_rect2 = string_rendered2.get_rect()
            intro_rect2.y = height1//2-height1//30
            intro_rect2.x = width1//2-width1//8

            screen1.blit(string_rendered2, intro_rect2)

            pygame.display.flip()
