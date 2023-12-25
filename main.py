import pygame
from config import *
from player import Player
from drawing import Drawing

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    map_surface = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
    clock = pygame.time.Clock()
    player = Player()
    drawing = Drawing(screen, map_surface)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.movement()
        screen.fill('black')

        drawing.background(player.angle)
        drawing.world(player.pos, player.angle)
        drawing.fps(clock)
        drawing.minimap(player)

        pygame.display.flip()
        clock.tick(FPS)
