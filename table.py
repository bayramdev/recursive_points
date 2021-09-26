# This file currently is not used anywhere

from typing import Callable, List, Tuple

Position = Tuple[int, int]
PointFunction = Callable[[int, int], Position]


class Table(list[list[int]]):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        for _y in range(self.height):
            row = [0 for _x in range(self.width)]
            self.append(row)

    def mark_by_positions(self, positions: List[Position]) -> int:
        mark_count = 0
        for pos in positions:
            if self.is_in_boundry(pos):
                self.set_by_position(pos, 1)
        return mark_count

    def mark_by_functions(self, functions: List[PointFunction]) -> int:
        mark_count = 0
        finished = False
        while not finished:
            finished = True
            for y, row in enumerate(self):
                for x, value in enumerate(row):
                    for fn in functions:
                        if value == 1:
                            relative = fn(x, y)
                            if self.is_in_boundry(relative):
                                if self.get_by_position(relative) == 0:
                                    finished = False
                                    self.set_by_position(relative, 1)
                                    mark_count += 1
        return mark_count

    def get_mark_count(self):
        return sum(map(sum, self))

    def get_by_position(self, pos: Position):
        x, y = pos
        return self[y][x]

    def set_by_position(self, pos: Position, value: int):
        x, y = pos
        self[y][x] = value

    def is_in_boundry(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height
