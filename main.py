from rayCasting import walls_ray_cast
from objects import *
from player import Player
from drawing import Drawing

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mouse.set_visible(False)
    map_surface = pygame.Surface(MINIMAP)

    sprites = Sprites()
    clock = pygame.time.Clock()
    player = Player(sprites)
    drawing = Drawing(screen, map_surface)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        player.movement()
        screen.fill('black')

        drawing.background(player.angle)
        walls = walls_ray_cast(player, drawing.textures)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.fps(clock)
        drawing.minimap(player)

        pygame.display.flip()
        clock.tick(FPS)
