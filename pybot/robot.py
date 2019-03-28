import pygame
from random import randint
from collide import *
from math import cos, sin, radians


class Robot(pygame.Rect):
    def __init__(self, beginPosition, image):
        super(pygame.Rect, self).__init__()
        self.center = beginPosition
        self.size = (32,32)
        self.angle = randint(0, 360)

    def move(self, speed, width, height, walls):
        # Intelligence du robot (Random Walk pour l'instant)
        angle, dist = randint(-100, 100), randint(2, 3)
        self.angle = (self.angle + angle) %360


        ox, oy = int(dist * cos(radians(self.angle))), int(dist * sin(radians(self.angle)))
        self.centerx += speed * ox
        self.centery += speed * oy
        if self.left < 0 or self.right > width or self.top < 0 or self.bottom > height:
            self.centerx -= speed *ox
            self.centery -= speed *oy

        if self.collideWalls(walls):
            self.centerx -= speed *ox
            self.centery -= speed *oy

    def collideWalls(self, walls):
        for w in walls:
            if collideRectLine(self.topleft, self.bottomleft, self.topright, self.bottomright, w.begin, w.end):
                return True
        return False
