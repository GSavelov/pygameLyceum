import pygame
from config import *
from rayCasting import ray_casting
from map import mini_map


class Drawing:
    def __init__(self, surface, map_surface):
        self.surface = surface
        self.map_surface = map_surface
        self.font = pygame.font.Font(None, 36)
        self.textures = {'1': pygame.image.load('textures/texture_1.png').convert(),
                         '2': pygame.image.load('textures/texture_2.png').convert()}

    def background(self):
        pygame.draw.rect(self.surface, SKY, (0, 0, WIDTH, H_HEIGHT))
        pygame.draw.rect(self.surface, GRAY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, pos, angle):
        ray_casting(self.surface, pos, angle, self.textures)

    def fps(self, clock):
        fps = str(int(clock.get_fps()))
        render = self.font.render(fps, 0, 'red')
        self.surface.blit(render, FPS_DRAW_POS)

    def minimap(self, player):
        self.map_surface.fill('black')
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.circle(self.map_surface, 'green', (map_x, map_y), 5)
        pygame.draw.line(self.map_surface, 'green', (map_x, map_y), (map_x + 10 * math.cos(player.angle),
                                                                     map_y + 10 * math.sin(player.angle)))
        for x, y in mini_map:
            pygame.draw.rect(self.map_surface, 'green', (x, y, MAP_TILE, MAP_TILE), 5)
        self.surface.blit(self.map_surface, MAP_DRAW_POS)
