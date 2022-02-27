import pygame
from pygame.locals import *
import os
import math
import random


# Переменные и костанты
FPS = 80
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
FON = (224, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ang = [0.78, 2.36, 3.9, 5.5]
button = []
text_button = ['Начать игру', 'Выход', 'Перезапустить', 'Продолжить']
score_p = 0
score_b = 0
game = False


class Button:
    def __init__(self, surf, text=None, size=10, sg=True, color_text=BLACK, color_button=WHITE):
        self.surf = surf
        self.text = text
        self.sg = sg
        self.color_text = color_text
        self.color_button = color_button
        self.font = pygame.font.SysFont(None, size)
        self.text_obj = self.font.render(self.text, self.sg, self.color_text, self.color_button)
        self.text_rect = self.text_obj.get_rect()

    def create(self, x=0, y=0):
        self.text_rect.centerx = x
        self.text_rect.centery = y
        self.surf.blit(self.text_obj, self.text_rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('RainbowBall.png', color_key=-1)
        self.vector = (random.choice(ang), 10)
        screen = pygame.display.get_surface()
        self.hit = False
        self.area = screen.get_rect()
        self.rect.topleft = (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 20)

    def re_init(self):
        self.rect.topleft = (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 20)
        self.vector = (random.choice(ang), 10)

    def update(self):
        new_pos = self.pos(self.vector)
        self.rect = new_pos
        (angle, z) = self.vector

        if not self.area.contains(new_pos):
            if self.rect.right > SCREEN_WIDTH:
                angle = math.pi - angle
            if self.rect.left < 0:
                angle = math.pi - angle
            if self.rect.top < 0:
                sound.play()
                gol(1)
                return
            if self.rect.bottom > SCREEN_HEIGHT:
                sound.play()
                gol(2)
                return
            self.hit = False
        else:
            if self.rect.colliderect(player1.rect) and not self.hit:
                angle = math.pi * 2 - angle
                self.hit = True
            elif self.rect.colliderect(player2.rect) and not self.hit:
                angle = math.pi * 2 - angle
                self.hit = True

        self.vector = (angle, z)

    def pos(self, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return self.rect.move(int(dx), int(dy))


class Player(pygame.sprite.Sprite):
    def __init__(self, where, name):
        super().__init__()
        self.image, self.rect = load_image(name, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 2
        self.where = where
        self.re_init()

    def re_init(self):
        if self.where == 'down':
            self.rect.midbottom = self.area.midbottom
        elif self.where == 'up':
            self.speed = 4
            self.rect.midtop = self.area.midtop

    def update(self):
        if self.where == 'down':
            if self.rect.left >= 0:
                if pressed_keys[K_a]:
                    self.rect.move_ip(-self.speed, 0)
            if self.rect.right <= SCREEN_WIDTH:
                if pressed_keys[K_d]:
                    self.rect.move_ip(self.speed, 0)
        elif self.where == 'up':
            if self.area.contains(self.rect):
                if self.rect.centerx > ball.rect.left:
                    self.speed = -4
                if self.rect.centerx < ball.rect.right:
                    self.speed = 4
            else:
                self.speed = -self.speed

            self.rect.move_ip(self.speed, 0)


# Перезапуск уровня
def gol(k):
    global score_b, score_p

    if k == 1:
        score_p += 1
    elif k == 2:
        score_b += 1
    elif k == 3:
        score_b = 0
        score_p = 0

    player1.re_init()
    player2.re_init()
    ball.re_init()


# Вывод надписей
def drawText(text, font, surface, x, y):
    text_obj = font.render(text, 1, BLACK)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# Меню игры
def menu(sc, cl):
    pygame.mouse.set_visible(1)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 1
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if game:
                    if button[3].text_rect.left < event.pos[0] < button[3].text_rect.right \
                            and button[3].text_rect.top < event.pos[1] < button[3].text_rect.bottom:
                        return
                    elif button[2].text_rect.left < event.pos[0] < button[2].text_rect.right \
                            and button[2].text_rect.top < event.pos[1] < button[2].text_rect.bottom:
                        return 2
                    elif button[1].text_rect.left < event.pos[0] < button[1].text_rect.right \
                            and button[1].text_rect.top < event.pos[1] < button[1].text_rect.bottom:
                        return 1
                else:
                    if button[0].text_rect.left < event.pos[0] < button[0].text_rect.right \
                            and button[0].text_rect.top < event.pos[1] < button[0].text_rect.bottom:
                        return 2
                    elif button[1].text_rect.left < event.pos[0] < button[1].text_rect.right \
                            and button[1].text_rect.top < event.pos[1] < button[1].text_rect.bottom:
                        return 1

        sc.fill(FON)

        if game:
            for j in range(3, 0, -1):
                button[j].create(SCREEN_WIDTH // 2, 550 - 100 * j)
        else:
            for j in range(2):
                button[j].create(SCREEN_WIDTH // 2, 280 + 100 * j)

        pygame.display.flip()
        cl.tick(FPS)


# Загрузка музыки, n == 0 - загрузка фоновой музыки (функция возвращает None),
# n == 1 - загрузка кратковременных звуков (функция возвращает sound).
def load_sound(name, n):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer:
        return NoneSound()

    full_name = os.path.join('sound', name)

    try:
        if n:
            voice = pygame.mixer.Sound(full_name)
        else:
            pygame.mixer.music.load(full_name)
            pygame.mixer.music.play(loops=-1)
            return
    except pygame.error as message:
        print(f'Cannot load sound: {full_name}')
        raise SystemExit(message)

    return voice


# Загрузка изображений, color_key - (R, G, B) цвет который не будет показываться
def load_image(name, color_key=None):
    full_name = os.path.join('image', name)

    try:
        image = pygame.image.load(full_name)
    except pygame.error as message:
        print(f'Cannot load image: {full_name}')
        raise SystemExit(message)

    image = image.convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))

        image.set_colorkey(color_key, RLEACCEL)

    return image, image.get_rect()


def main():
    # Инициализируем
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Самодельный pong v.2.0')

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 25)

    # глобал ставим чтоб ошибки небыло
    global player1, player2, ball, sound, pressed_keys, game

    # Загружаем музыку
    pygame.mixer.init()
    sound = load_sound('gol.wav', 1)
    load_sound('main.mp3', 0)

    # Создаём игроков
    player1 = Player('down', 'green_bt.png')
    player2 = Player('up', 'red_bt.png')

    # Создаём шар
    ball = Ball()

    # Создаём кнопки для главного меню и группу для их отрисовки
    for i in range(len(text_button)):
        button.append(Button(screen, text_button[i], 65, color_button=FON))

    # Группы спрайтов
    all_sprite = pygame.sprite.Group()
    all_sprite.add(player1, player2, ball)

    MainLoop = True
    while MainLoop:
        level = menu(screen, clock)
        if level == 1:
            return
        elif level == 2:
            gol(3)

        pygame.mouse.set_visible(0)

        game = True
        GameLoop = True
        while GameLoop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        GameLoop = False

            pressed_keys = pygame.key.get_pressed()

            screen.fill(FON)

            for entity in all_sprite:
                screen.blit(entity.image, entity.rect)

            drawText(f'Бот:{score_b}', font, screen, 0, SCREEN_HEIGHT // 2 - 10)
            drawText(f'Игрок:{score_p}', font, screen, 0, SCREEN_HEIGHT // 2 + 10)

            all_sprite.update()

            pygame.display.flip()
            clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()
