import pygame
import math
from config import *
from player import Player
from map import world_map
from rayCasting import ray_casting

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.movement()
        screen.fill('black')

        ray_casting(screen, player.pos, player.angle)

        pygame.draw.circle(screen, 'green', player.pos, 15)
        pygame.draw.line(screen, 'green', player.pos, (player.x + WIDTH * math.cos(player.angle),
                                                       player.y + WIDTH * math.sin(player.angle)))
        for x, y in world_map:
            pygame.draw.rect(screen, 'white', (x, y, TILE, TILE), 2)

        pygame.display.flip()
        clock.tick(FPS)
