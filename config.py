import math

# Window settings
WIDTH = 1200
HEIGHT = 800
H_WIDTH = WIDTH // 2
H_HEIGHT = HEIGHT // 2

# Game settings
FPS = 60
FPS_DRAW_POS = WIDTH - 60, 5
TILE = 100

# Minimap settings
MAP_SCALE = 5
MAP_TILE = TILE // MAP_SCALE
MAP_DRAW_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)

# Player settings
player_pos = H_WIDTH, H_HEIGHT
player_angle = 0
player_speed = 2

# Ray casting settings
FOV = math.pi / 3
H_FOV = FOV / 2
NUM_RAYS = 600
MAX_DEPTH = 800
DELTA_A = FOV / NUM_RAYS
DISTANCE = NUM_RAYS / (2 * math.tan(H_FOV))
PROJ_COEFF = DISTANCE * TILE
SCALE = WIDTH // NUM_RAYS

# Texture settings
TEXTURE_WIDTH, TEXTURE_HEIGHT = 1200, 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# Colors
SKY = (115, 223, 250)
GRAY = (66, 66, 66)
