from config import *

map_model = [
    '111111111111',
    '1..........1',
    '1..........1',
    '11.........1',
    '11.........1',
    '1..........1',
    '1..........1',
    '111111111111'
]
world_map = {}
mini_map = set()
for j, row in enumerate(map_model):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = '1'
            elif char == '2':
                world_map[(i * TILE, j * TILE)] = '2'
