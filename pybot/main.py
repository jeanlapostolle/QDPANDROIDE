import sys, pygame
from robot import Robot
from wall import Wall
from math import cos, sin, radians

pygame.init()

# Parametre
size = width, height = 640, 480
finish_position = (width/10, height/10)
background_color = 255, 255, 255
NbOfRobot = 100
fps = 200
speed = 4

# Affichage
screen = pygame.display.set_mode(size)

robotimg = pygame.image.load("ressources/robot.gif")
finishimg = pygame.image.load("ressources/finish.png")

finish = finishimg.get_rect()
finish.center = finish_position


robots = [ Robot((width/10, height*3/10), robotimg) for i in range(NbOfRobot)]


clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Creation des murs
w1 = Wall((0, height/5), (width*4/5, height/5))
w2 = Wall((width/5, height/5), (width/5, height*4/5))
w3 = Wall((width*3/5, height*2/5), (width, height*4/5))
w4 = Wall((width*1/5, height*2/5), (width*3/5, height*4/5))


walls = [w1, w2, w3, w4]


# Boucle de "Jeu"
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Déplacement
    for robot in robots:
        robot.move(speed, width, height, walls)

    # Réussite
    if finish.collidelist(robots) != -1:
        print("Finish est atteint")
        break

    # Affichage
    print("fps :"  + str(int(clock.get_fps())), end='\r', flush=True)

    screen.fill(background_color)

    for robot in robots:
        mimg = pygame.transform.rotate(robotimg, robot.angle)
        screen.blit(mimg,robot)
    for w in walls:
        w.show(screen)

    screen.blit(finishimg, finish)
    pygame.display.flip()
    clock.tick(fps)
