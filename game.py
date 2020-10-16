import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 10
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

k = 0
X = Y = 800
click = 0

class ball():
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





pygame.display.update()
clock = pygame.time.Clock()
finished = False

balllist = []

while not finished:
    clock.tick(FPS)
    balllist.append(ball(randint(100, 700), randint(100, 700),
                         randint(10, 10), COLORS[randint(0, 5)],
                         randint(100, 300), randint(0, 20), randint(0, 20)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = pygame.mouse.get_pos()  # координаты щелчка мыши
            for i in balllist:
                # проверка, не попался ли мяч
                if (i.x - x1) ** 2 + (i.y - y1) ** 2 <= i.r ** 2:
                    balllist.remove(i)
                    click += 1
                    print('Ваш результат: ', click)

    for i in balllist:
        # проверка отлета от границ и отражения
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
        # проверка отлета от границ и отражения
        if i.time >= 0:
            circle(screen, i.color, (i.x, i.y), i.r)
            i.time -= 1


    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
