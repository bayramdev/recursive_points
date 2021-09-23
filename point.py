import pygame.math


class Point(pygame.math.Vector2):
    def __init__(self, x, y=0, children: list = None):
        super().__init__(x, y)
        self.children = children
        if self.children == None:
            self.children = []
