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


matrix_map = load_map('level_1')

WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
wall_collisions = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            wall_collisions.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4
            elif char == 5:
                world_map[(i * TILE, j * TILE)] = 5

