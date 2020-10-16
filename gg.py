import pygame
import random
from pygame.draw import *
from random import randint
import numpy as np
pygame.init()
username = input("Представьтесь ") # get username for highscore
FPS = 10 # fps
font = pygame.font.Font('freesansbold.ttf', 52)
X = Y = 800
screen = pygame.display.set_mode((X, Y))
skill = 0  # score of user
#colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE =(255,255,255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN,WHITE]


class user():
    '''describes each line in highscore table'''
    def __init__(self,name,score):
        self.name = name
        self.score = score

class ball():
    '''describes parameters of each ball
    pair of coordinates
    radius
    pair of speeds
    color
    time before been  eliminated'''
    def __init__(self,x,y,r,color,time,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
        self.time = time


class ellipse():
    '''descibes each small point flying in the screen (they fly along ellipse trajectory)
    parameters:
    pair of coordinates
    pair of half-axes
    color
    time before been deleted
    period : period of revolution'''
    def __init__(self,x,y,a,b,color,time,period):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.color = color
        self.time = time

clock = pygame.time.Clock()
finished = False
# initialize arrays of elements on the screen
balllist=[]
ellipselist=[]
pygame.display.update()

while not finished:
    clock.tick(FPS)
    # here we spawn whire ellipse-point with probability of 10%
    prob = random.randint(0,100)
    period=50
    if prob>90:
        ellipselist.append(ellipse(randint(300,500),randint(300,500),randint(20,100),randint(20,100),COLORS[randint(0, 5)],randint(100,300),period))

    # here we spawn a new ball
    balllist.append(ball(randint(100, 700),randint(100, 700),randint(10, 10),COLORS[randint(0, 5)],randint(100,300),randint(0,20),randint(0,20)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # here we go again by adding highscore to the table
            current = user(username, skill)
            text = ''
            out = ''
            text = open('highscore.txt', 'r')
            s = text.read()
            data = [user('', '')]
            j = 0
            k = 0
            # inthe cycle we read the file as an array of user-class objects
            while j < len(s) - 3:
                while s[j] != "*":
                    data[k].name += s[j]
                    j += 1
                j += 1
                while s[j] != '\n':
                    data[k].score += s[j]
                    j += 1
                j += 1
                data.append(user('', ''))
                k += 1

            del data[len(data) - 1] # we delete last empty string
            data.append(current)
            b = len(data) - 2
            # here we sort the array
            while (int(data[b].score) < int(current.score) and b >= 0):
                bqw = data[b]
                data[b] = current
                data[b + 1] = bqw
                b -= 1

            pop = 0
            # here we search for items with the same name
            for i in range(len(data) - 1):
                for j in range(i + 1, len(data)):
                    if data[i].name == data[j].name:
                        data[j].name = '01'

            data1 = []
            # here we do not take in the new array unnessesary repeated elements
            for i in range(len(data)):
                if data[i].name != '01':
                    data1.append(data[i])
            data = data1
            #here we write new highscore to the file
            for i in data:
                out += str(i.name) + '*' + str(i.score) + '\n'
            file = open('highscore.txt', 'w')
            file.write(out)
            file.close()

            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x1,y1 = pygame.mouse.get_pos() #gettin mouseclick coordinates
            for i in balllist:
                # checking if ball got caught
                if (i.x-x1)**2+(i.y-y1)**2 <= i.r**2:
                    balllist.remove(i)
                    skill+=1
            for j in ellipselist:
                # checking if a white point got caught
                if ((j.x+j.a*np.sin(j.time/period*2*np.pi))-x1)**2+((j.y+j.b*np.cos(j.time/period*2*np.pi))-y1)**2 <= 100:
                    ellipselist.remove(j)
                    skill+=5


    for i in balllist:
        # checking flying off the boundaries and reflection
        if ((abs(i.x+i.vx-X/2)<X/2-i.r) and (abs(i.y+i.vy-Y/2)<Y/2-i.r)):
            i.x+=i.vx
            i.y+=i.vy
        elif (abs(i.x+i.vx-X/2)>X/2-i.r) and (abs(i.y+i.vy-Y/2)<Y/2-i.r):
            if i.vx>0:
                i.x = X-(i.vx - (X-i.x))
            else:
                i.x = -i.vx-i.x
            i.vx = -i.vx
            i.y += i.vy
        elif (abs(i.x+i.vx-X/2)<X/2-i.r) and (abs(i.y+i.vy-Y/2)>Y/2-i.r):
            if i.vy>0:
                i.y = Y-(i.vy - (X-i.y))
            else:
                i.y = -i.vy-i.y
            i.vy = -i.vy
            i.x += i.vx
        else:
            if i.vy>0:
                i.y = Y - (i.vy - (Y - i.y))
            else:
                i.y = -i.vy-i.y
            if i.vx>0:
                i.x = X - (i.vx - (X - i.x))
            else:
                i.x = -i.vx-i.x
            i.vy = -i.vy
            i.vx = -i.vx
        # checking is it time for an onject to be deleted or draw
        if i.time>= 0:
            circle(screen, i.color, (i.x, i.y), i.r)
            i.time-=1
    for j in ellipselist:
        # checking is it time for an onject to be deleted or drawn
        if j.time>= 0:
            circle(screen, WHITE, ((int(j.x)+int(j.a*np.sin(j.time/period*2*np.pi))), (int(j.y)+int(j.b*np.cos(j.time/period*2*np.pi)))), 5)
            j.time-=1
    #write score in the upper-left corner
    text = font.render(str(skill), True, GREEN, RED)
    textRect = text.get_rect()
    textRect.center = (100, 100)
    screen.blit(text, textRect)


    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()