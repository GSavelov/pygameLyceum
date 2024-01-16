from config import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

_ = False


def load_map(name):
    with open('levels/' + name + '.txt', 'r') as lvl:
        try:
            matrix = []
            for line in lvl:
                string = []
                line = line.strip()
                for c in line:
                    if c in '12345':
                        string.append(int(c))
                    else:
                        string.append(_)
                if len(string) != 24:
                    raise EOFError
                else:
                    matrix.append(string)
            if len(matrix) != 16:
                raise EOFError
            else:
                return matrix
        except EOFError:
            print('Неверный формат уровня')


class WorldMap:
    def __init__(self, lvl):
        self.matrix = load_map(lvl)
        self.map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        self.WORLD_WIDTH = len(self.matrix[0]) * TILE
        self.WORLD_HEIGHT = len(self.matrix) * TILE
        self.mini_map = set()
        self.wall_collisions = []
        for j, row in enumerate(self.matrix):
            for i, char in enumerate(row):
                if char:
                    self.mini_map.add((i * MAP_TILE, j * MAP_TILE))
                    self.wall_collisions.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                    if char == 1:
                        self.map[(i * TILE, j * TILE)] = 1
                    elif char == 2:
                        self.map[(i * TILE, j * TILE)] = 2
                    elif char == 3:
                        self.map[(i * TILE, j * TILE)] = 3
                    elif char == 4:
                        self.map[(i * TILE, j * TILE)] = 4
                    elif char == 5:
                        self.map[(i * TILE, j * TILE)] = 5
