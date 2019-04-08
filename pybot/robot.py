import pygame
from random import randint
from collide import *
from math import cos, sin, radians
import mlp
# import ctypes

# Load the shared library into c types.
# libc = ctypes.CDLL("./collide.so")
# libc.collideRectLine.argtypes =[ctypes.c_double ]*12


class Robot(pygame.Rect):
    def __init__(self, beginPosition, image):
        super(pygame.Rect, self).__init__()
        self.center = beginPosition
        self.size = (32, 32)
        self.angle = randint(0, 360)
        # self.mymlp = mlp.MLP(12, 8, 2)
        # self.myBack = mlp.Backpropagation(self.mymlp, 0.3, 0.001)

    def move(self, speed, width, height, walls):
        # Intelligence du robot (Random Walk pour l'instant)
        # print(self.sensor(walls))
        # d, a = self.mymlp.compute(self.sensor(walls))
        # dist = int(d * 5)
        # angle = int(a * 360)
        old_center = self.center
        angle, dist = randint(-100, 100), randint(2, 3)

        self.angle = (self.angle + angle) % 360

        ox, oy = int(dist * cos(radians(self.angle))
                     ), int(dist * sin(radians(self.angle)))
        self.centerx += speed * ox
        self.centery += speed * oy
        if self.left < 0 or self.right > width or self.top < 0 or self.bottom > height:
            self.centerx -= speed * ox
            self.centery -= speed * oy

        if self.collideWalls(walls):
            self.centerx -= speed * ox
            self.centery -= speed * oy

        if distc(self.center, (width, height)) > distc(old_center, (width, height)):
            res = 0
        else:
            res = 1
        # myBack.iterate([d, a], [res])

    def collideWalls(self, walls):
        for w in walls:
            # print(self.topleft)
            if collideRectLine(self.topleft, self.bottomleft, self.topright, self.bottomright, w.begin, w.end):
                return True
        return False

    def sensor(self, walls):
        poss = []
        for angle in [0, 22.5, 45, 67.5, 90, 135, 180, -135, -90, -67.5, -45, -22.5]:
            poss.append(self.sensorX(walls, angle))
        return poss

    def sensorX(self, walls, angle):
        wp = []
        dist = 5
        for w in walls:
            mp = (int(self.center[0] + dist * cos(radians(self.angle + angle))),
                  int(self.center[1] + dist * sin(radians(self.angle + angle))))
            a, b = w.begin, w.end
            p = intersect(w.begin, w.end, self.center, mp)

            if p != None:
                if p[0] >= a[0] and p[0] <= b[0] and p[1] <= b[1] and p[1] >= a[1]:
                    wp.append(p)
                    # ms = (int(self.center[0] + dist * cos(radians(self.angle + angle + 90))),
                    #       int(self.center[1] + dist * sin(radians(self.angle + angle + 90))))
                    #
                    # c, d = droite(self.center, ms)
                    # d = evalPointDroite(p, (c, d))
                    # ang = (self.angle + angle) % 360
                    # if ang <= 270 and ang >= 90:
                    #     if c > 0:
                    #         wp.append(p)
                    # else:
                    #     if c < 0:
                    #         wp.append(p)
        # print(wp)
        dp = [distc(self.center, i) for i in wp]
        if dp != []:
            pos = dp.index(min(dp))
            return wp[pos]
        return None
