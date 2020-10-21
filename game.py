import pygame
from pygame.draw import *
from random import randint
import numpy as np

pygame.init()

FPS = 10
font = pygame.font.SysFont('arial', 36)
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

k = 0
X = Y = 800
click = 0

username = input("Name: ")


class Ball():
    """параметры шара:
    пара координат,
    радиус,
    пара скоростей,
    цвет,
    время до устранения"""

    def __init__(self, x, y, r, color, time, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
        self.time = time


class Circles():
    """параметры квадрата:
    пара координат,
    длина, ширина,
    пара скоростей,
    цвет,
    время до устранения"""

    def __init__(self, x, y, r, color, time, vx, vy, period):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.time = time


class User():
    """описание строки в файле"""

    def __init__(self, name, score):
        self.name = name
        self.score = score


pygame.display.update()
clock = pygame.time.Clock()
finished = False

balllist = []
cirlist = []

while not finished:
    clock.tick(FPS)
    # рисуем шарик
    balllist.append(Ball(randint(100, 700), randint(100, 700),
                         randint(10, 20), COLORS[randint(0, 5)],
                         randint(100, 300), randint(0, 20), randint(0, 20)))
    # рисуем окружность с вероятностью 20%
    probability = randint(0, 100)
    period = 50
    if probability > 80:
        cirlist.append(Circles(randint(100, 700), randint(100, 700),
                               randint(10, 50), COLORS[randint(0, 5)],
                               randint(100, 300), randint(0, 20),
                               randint(0, 20),
                               period))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # добавляем рекорд
            current = User(username, click)
            text = ''
            out = ''
            text = open('rating.txt', 'r')
            s = text.read()
            data = [User('', '')]
            j = 0
            k = 0
            while j < len(s) - 3:
                while s[j] != "*":
                    data[k].name += s[j]
                    j += 1
                j += 1
                while s[j] != '\n':
                    data[k].score += s[j]
                    j += 1
                j += 1
                data.append(User('', ''))
                k += 1

            del data[len(data) - 1]  # последняя пустаю строка
            data.append(current)
            b = len(data) - 2
            # сортировка
            while int(data[b].score) < int(current.score) and b >= 0:
                bqw = data[b]
                data[b] = current
                data[b + 1] = bqw
                b -= 1

            pop = 0
            # одинаковые игроки
            for i in range(len(data) - 1):
                for j in range(i + 1, len(data)):
                    if data[i].name == data[j].name:
                        data[j].name = '01'

            data1 = []
            # не берём одинаковые элементы
            for i in range(len(data)):
                if data[i].name != '01':
                    data1.append(data[i])
            data = data1
            # добавляем результат
            for i in data:
                out += str(i.name) + '*' + str(i.score) + '\n'
            file = open('rating.txt', 'w')
            file.write(out)
            file.close()

            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = pygame.mouse.get_pos()  # координаты щелчка мыши
            for i in balllist:
                # проверка, не попался ли мяч
                if (i.x - x1) ** 2 + (i.y - y1) ** 2 <= i.r ** 2:
                    balllist.remove(i)
                    click += 1
                    print('Ваш результат: ', click)
            for j in cirlist:
                # проверка, не попался ли кружочек
                if ((j.x + j.r * np.sin(
                        j.time / period * 2 * np.pi)) - x1) ** 2 + (
                        (j.y + j.r * np.cos(
                            j.time / period * 2 * np.pi)) - y1) ** 2 <= 100:
                    cirlist.remove(j)
                    click += 3
                    print('Ваш результат: ', click)

    for i in balllist:
        # проверка отлёта от границ и отражения
        if ((abs(i.x + i.vx - X / 2) < X / 2 - i.r) and (
                abs(i.y + i.vy - Y / 2) < Y / 2 - i.r)):
            i.x += i.vx
            i.y += i.vy
        elif (abs(i.x + i.vx - X / 2) > X / 2 - i.r) and (
                abs(i.y + i.vy - Y / 2) < Y / 2 - i.r):
            if i.vx > 0:
                i.x = X - (i.vx - (X - i.x))
            else:
                i.x = -i.vx - i.x
            i.vx = -i.vx
            i.y += i.vy
        elif (abs(i.x + i.vx - X / 2) < X / 2 - i.r) and (
                abs(i.y + i.vy - Y / 2) > Y / 2 - i.r):
            if i.vy > 0:
                i.y = Y - (i.vy - (X - i.y))
            else:
                i.y = -i.vy - i.y
            i.vy = -i.vy
            i.x += i.vx
        else:
            if i.vy > 0:
                i.y = Y - (i.vy - (Y - i.y))
            else:
                i.y = -i.vy - i.y
            if i.vx > 0:
                i.x = X - (i.vx - (X - i.x))
            else:
                i.x = -i.vx - i.x
            i.vy = -i.vy
            i.vx = -i.vx

        if i.time >= 0:
            circle(screen, i.color, (i.x, i.y), i.r)
            i.time -= 1

    for j in cirlist:
        # рисуем кружочки, двигающиеся по окружностям
        if j.time >= 0:
            circle(screen, WHITE, ((int(j.x) + int(j.r * np.sin(j.time / period
                                                                * 2 * np.pi))),
                                   (int(j.y) + int(j.r * np.cos(j.time / period
                                                                * 2 * np.pi)))),
                   5)
            j.time -= 1

    # очки
    text = font.render(str(click), True, BLUE, WHITE)
    textRect = text.get_rect()
    textRect.center = (80, 80)
    screen.blit(text, textRect)

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
