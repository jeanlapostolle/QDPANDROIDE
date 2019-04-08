import sys
import pygame
from robot import Robot
from wall import Wall
from math import cos, sin, radians
import threading


pygame.init()

# Parametre
maze = 2
background_color = 255, 255, 255
NbOfRobot = 1
fps = 99
speed = 3
debug = True

# Creation des murs & choix du maze
if maze == 1:
    size = width, height = 640, 480
    finish_position = (width / 10, height / 10)
    w1 = Wall((0, height / 5), (width * 4 / 5, (height) / 5))
    w2 = Wall((width / 5, height / 5), ((width + 1) / 5, height * 4 / 5))
    w3 = Wall((width * 3 / 5, height * 2 / 5), (width, height * 4 / 5))
    w4 = Wall((width * 1 / 5, height * 2 / 5), (width * 3 / 5, height * 4 / 5))
    walls = [w1, w2, w3, w4]

elif maze == 2:
    size = width, height = 400, 200
    finish_position = (width, height)
    w1 = Wall((50, 80), (340, 200))
    w2 = Wall((120, 0), (70, 50))
    w3 = Wall((220, 0), (170, 70))
    w4 = Wall((350, 0), (300, 100))
    w5 = Wall((350, 140), (380, 200))
    w6 = Wall((120, 60), (150, 125))
    w7 = Wall((220, 85), (250, 190))
    walls = [w1, w2, w3, w4, w5, w6, w7]

wa = Wall((0, 0), (width - 1, 1))
wb = Wall((0, 0), (1, height - 1))
wc = Wall((width, 0), (width - 1, height - 1))
wd = Wall((0, height), (width - 1, height - 1))
walls += [wa, wb, wc, wd]

# Affichage
screen = pygame.display.set_mode(size)

robotimg = pygame.image.load("ressources/robot.gif")
finishimg = pygame.image.load("ressources/finish.png")

finish = finishimg.get_rect()
finish.center = finish_position


robots = [Robot((width / 10, height * 3 / 10), robotimg)
          for i in range(NbOfRobot)]


clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)


def moveall():
    for robot in robots:
        robot.move(speed, width, height, walls)


# Boucle de "Jeu"
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Déplacement
    moveall()

    # Réussite
    if finish.collidelist(robots) != -1:
        print("Finish est atteint")
        break

    # Affichage
    print("fps :" + str(int(clock.get_fps())), end='\r', flush=True)

    screen.fill(background_color)

    for robot in robots:
        mimg = pygame.transform.rotate(robotimg, - robot.angle - 90)
        pp = robot.sensor(walls)
        if debug:
            for i in pp:
                if (i != None):
                    pygame.draw.line(screen, (0, 255, 0), robot.center, i, 1)
                    pygame.draw.rect(screen, (255, 0, 0),
                                     pygame.Rect(i[0], i[1], 10, 10))

        screen.blit(mimg, robot)
    for w in walls:
        w.show(screen)

    screen.blit(finishimg, finish)
    pygame.display.flip()
    clock.tick(fps)
