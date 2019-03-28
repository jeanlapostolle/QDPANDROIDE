import pygame

class Wall():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def show(self, screen):
        pygame.draw.line(screen, (0,0,0), self.begin, self.end, 3)
