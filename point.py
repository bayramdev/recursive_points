# IMPORTS

from __future__ import annotations

from typing import Callable, List, Tuple
import enum

import pygame.math


# TYPES
class ValidationResult(enum.Enum):
    Unique = 0
    Duplicate = 1
    OutOfBoundry = 2


Position = Tuple[int, int]
PointFunction = Callable[[int, int], Position]
Validator = Callable[['Point'], ValidationResult]


# CLASSES

class Point(pygame.math.Vector2):
    def __init__(self, x: int, y: int = 0):
        super().__init__(x, y)
        self.children = []

    def __str__(self) -> str:
        return "Point({}, {}, {})".format(self.x, self.y, self.children)

    def __repr__(self) -> str:
        return str(self)

    def includes(self, match: Point):
        if self == None or match == None:
            return False

        if self.x == match.x and self.y == match.y:
            return True

        return any(map(lambda p: p.includes(match), self.children))


class RootPoint(Point):
    def __init__(
        self,
        x: int,
        y: int,
        functions: List[PointFunction],
        area_width: int,
        area_height: int
    ):
        super().__init__(x, y)
        self.area_width = area_width
        self.area_height = area_height
        RootPoint._create_point_tree(self, functions, self._validate)

    @staticmethod
    def _create_point_tree(
        point: Point,
        functions: List[PointFunction],
        validate: Validator,
        is_parent_in_boundry: bool = True
    ) -> Point:
        for fn in functions:
            child = Point(fn(point.x, point.y))
            result = validate(child)
            if result == ValidationResult.Unique:
                RootPoint._create_point_tree(child, functions, validate)
                point.children.append(child)
            elif result == ValidationResult.OutOfBoundry and is_parent_in_boundry:
                RootPoint._create_point_tree(child, functions, validate, False)
                point.children.append(child)

    def _validate(self, other: Point):
        if self.includes(other):
            return ValidationResult.Duplicate
        elif 0 <= other.x < 16 and 0 <= other.y < 16:
            return ValidationResult.Unique
        else:
            return ValidationResult.OutOfBoundry
