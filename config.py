import math

# Window settings
WIDTH = 1200
HEIGHT = 800
H_WIDTH = WIDTH // 2
H_HEIGHT = HEIGHT // 2

# Game settings
FPS = 60
TILE = 100

# Player settings
player_pos = H_WIDTH, H_HEIGHT
player_angle = 0
player_speed = 2

# Ray casting settings
FOV = math.pi / 3
H_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_A = FOV / NUM_RAYS
