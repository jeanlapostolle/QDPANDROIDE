import sys
import pygame
from robot import Robot
from wall import Wall
from math import cos, sin, radians
import threading


pygame.init()

# Parametre
size = width, height = 640, 480
finish_position = (width / 10, height / 10)
background_color = 255, 255, 255
NbOfRobot = 1
fps = 100
speed = 3

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

# Creation des murs
wa = Wall((0, 0), (width - 1, 1))
wb = Wall((0, 0), (1, height - 1))
wc = Wall((width, 0), (width - 1, height - 1))
wd = Wall((0, height), (width - 1, height - 1))

w1 = Wall((0, height / 5), (width * 4 / 5, (height) / 5))
w2 = Wall((width / 5, height / 5), ((width + 1) / 5, height * 4 / 5))
w3 = Wall((width * 3 / 5, height * 2 / 5), (width, height * 4 / 5))
w4 = Wall((width * 1 / 5, height * 2 / 5), (width * 3 / 5, height * 4 / 5))


walls = [w1, w2, w3, w4, wa, wb, wc, wd]


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
        for i in pp:
            if (i != None):

                pygame.draw.rect(screen, (255, 0, 0),
                                 pygame.Rect(i[0], i[1], 10, 10))

        screen.blit(mimg, robot)
    for w in walls:
        w.show(screen)

    screen.blit(finishimg, finish)
    pygame.display.flip()
    clock.tick(fps)
