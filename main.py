import pygame
from config import *
from player import Player
from rayCasting import ray_casting
from drawing import Drawing

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player()
    drawing = Drawing(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.movement()
        screen.fill('black')

        drawing.background()
        drawing.world(player.pos, player.angle)
        drawing.fps(clock)

        pygame.display.flip()
        clock.tick(FPS)
