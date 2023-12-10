import pygame
from config import *
from player import Player
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

        pygame.display.flip()
        clock.tick(FPS)
