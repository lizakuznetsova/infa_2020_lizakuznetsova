import pygame as pg
from pygame.draw import *

pg.init()

FPS = 30
screen = pg.display.set_mode((400, 400))

rect(screen, (255, 255, 255), (0, 0, 1000, 1000))
circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (255, 0, 0), (160, 180), 22)
circle(screen, (0, 0, 0), (160, 180), 22, 1)
circle(screen, (255, 0, 0), (240, 180), 16)
circle(screen, (0, 0, 0), (240, 180), 16, 1)
circle(screen, (0, 0, 0), (240, 180), 7)
circle(screen, (0, 0, 0), (160, 180), 10)
circle(screen, (0, 0, 0), (200, 200), 100, 1)
rect(screen, (0, 0, 0), (155, 250, 90, 18))
polygon(screen, (0, 0, 0), [(105, 120), (100, 128),
                               (185, 169), (190, 161)])
polygon(screen, (0, 0, 0), [(215, 161), (219, 169),
                               (305, 145), (301, 137)])

pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

pg.quit()
