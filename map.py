from config import *

map_model = [
    'WWWWWWWWWWWW',
    'W..........W',
    'W...WWW....W',
    'W...W......W',
    'W...W......W',
    'W...WWW....W',
    'W..........W',
    'WWWWWWWWWWWW'
]
world_map = set()
for j, row in enumerate(map_model):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * TILE, j * TILE))
