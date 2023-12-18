import pygame
from config import *
from rayCasting import ray_casting


class Drawing:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font(None, 36)

    def background(self):
        pygame.draw.rect(self.surface, SKY, (0, 0, WIDTH, H_HEIGHT))
        pygame.draw.rect(self.surface, GRAY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, pos, angle):
        ray_casting(self.surface, pos, angle)

    def fps(self, clock):
        fps = str(int(clock.get_fps()))
        render = self.font.render(fps, 0, 'red')
        self.surface.blit(render, FPS_DRAW_POS)
