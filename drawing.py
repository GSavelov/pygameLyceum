from objects import *
from map import mini_map


class Drawing:
    def __init__(self, surface, map_surface):
        self.surface = surface
        self.map_surface = map_surface
        self.font = pygame.font.Font(None, 36)
        self.textures = {1: pygame.image.load('textures/brick_wall.png').convert(),
                         2: pygame.image.load('textures/brick_moss_wall.png').convert(),
                         3: pygame.image.load('textures/doom_brick_wall.png').convert(),
                         4: pygame.image.load('textures/doom_metal_wall.png').convert(),
                         5: pygame.image.load('textures/doom_metal_sheet_wall.png').convert(),
                         's': pygame.image.load('textures/doom_skybox.png').convert()}

    def background(self, angle):
        offset = -5 * math.degrees(angle) % WIDTH
        self.surface.blit(self.textures['s'], (offset, 0))
        self.surface.blit(self.textures['s'], (offset + WIDTH, 0))
        self.surface.blit(self.textures['s'], (offset - WIDTH, 0))
        pygame.draw.rect(self.surface, DARKGRAY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.surface.blit(object, object_pos)

    def fps(self, clock):
        fps = str(int(clock.get_fps()))
        render = self.font.render(fps, 0, 'green')
        self.surface.blit(render, FPS_DRAW_POS)

    def minimap(self, player):
        self.map_surface.fill('black')
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.circle(self.map_surface, MAP_COLOR, (map_x, map_y), 5)
        pygame.draw.line(self.map_surface, MAP_COLOR, (map_x, map_y), (map_x + 10 * math.cos(player.angle),
                                                                       map_y + 10 * math.sin(player.angle)))
        for x, y in mini_map:
            pygame.draw.rect(self.map_surface, MAP_COLOR, (x, y, MAP_TILE, MAP_TILE), 5)
        self.surface.blit(self.map_surface, MAP_DRAW_POS)
