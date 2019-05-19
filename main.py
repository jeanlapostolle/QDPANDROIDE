import sys
import pygame
from robot import Robot
from wall import Wall
#from math import cos, sin, radians
#import threading
#import random
pygame.init()
budgetRestant = [[None for i in range(200//5)] for j in range(400//5)]; # utiliser dans mapElite
# Parametre
maze = 2
background_color = 255, 255, 255
NbOfRobot = 1
fps = 99
debug = True
budget = 50;
speed = 20
radarRayon = 50
# Creation des murs & choix du maze
if maze == 1:
    size = width, height = 640, 480
    start_position = (1,1);
    finish_position = (width / 10, height / 10)
    w1 = Wall((0, height / 5), (width * 4 / 5, (height) / 5))
    w2 = Wall((width / 5, height / 5), ((width + 1) / 5, height * 4 / 5))
    w3 = Wall((width * 3 / 5, height * 2 / 5), (width, height * 4 / 5))
    w4 = Wall((width * 1 / 5, height * 2 / 5), (width * 3 / 5, height * 4 / 5))
    walls = [w1, w2, w3, w4]

elif maze == 2:
    size = width, height = 400, 200
    start_position = (width // 10, height * 3 // 10)
    finish_position = (370,150)
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

robotimg = pygame.image.load("ressources/robot.gif")
finishimg = pygame.image.load("ressources/finish.png")

def affichage(robot,clock,screen,finish):
#    print("fps :" + str(int(clock.get_fps())), end='\r', flush=True)

    screen.fill(background_color)

    mimg = pygame.transform.rotate(robotimg, - robot.angle - 90)
    pp = robot.sensor(walls)
    if debug:
        for i in pp:
            if (i != None):
                pygame.draw.line(screen, (0, 255, 0), robot.center, i, 1)
                pygame.draw.rect(screen, (255, 0, 0),
                                 pygame.Rect(int(i[0]), int(i[1]), 10, 10))

    screen.blit(mimg, robot)
    for w in walls:
        w.show(screen)

    screen.blit(finishimg, finish)
    pygame.display.flip()
    clock.tick(fps)
def simulationNavigation(brain):
    # pygame initialization
    pygame.init()
    finish = finishimg.get_rect()
    finish.center = finish_position
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    # creation de robot
    robot = Robot(start_position, robotimg, radarRayon,brain,finish.center, speed)
    # Boucle de "Jeu"
    for i in range(budget):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Deplacement
        budgetRestant[robot.center[0],robot.center[1]] = budget;
        robot.move(speed, width, height, walls);
        # Reussite
        if finish.collidelist([robot]) != -1:
            print("Finish est atteint")
            break
    
        affichage(robot,clock,screen,finish);   
    pygame.quit();
    return robot.center;
def simulationNavigationSansImage(brain):
    # pygame initialization
    pygame.init()
    finish = finishimg.get_rect()
    finish.center = finish_position
#    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    # creation de robot
    robot = Robot(start_position, robotimg, radarRayon,brain,finish.center, speed)
    # Boucle de "Jeu"
    for i in range(budget):
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                sys.exit()
        # Deplacement
        robot.move(speed, width, height, walls);
        # Reussite
        if finish.collidelist([robot]) != -1:
            print("Finish est atteint")
            break    
    return robot.center;

