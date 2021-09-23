import pygame.math


class Point(pygame.math.Vector2):
    def __init__(self, x, y=0, left=None, right=None):
        super().__init__(x, y)
        self.left = left
        self.right = right
