from rayCasting import walls_ray_cast
from objects import *
from player import Player
from drawing import Drawing, MenuDrawing
from interactions import Interaction
from map import WorldMap

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    map_surface = pygame.Surface(MINIMAP)
    clock = pygame.time.Clock()

    menu = MenuDrawing(screen, clock)
    menu.mixer_init()
    menu.menu()

    world_map = WorldMap(menu.select)
    sprites = Sprites()
    sprites.load_objects(menu.select)
    player = Player(sprites, world_map.wall_collisions)
    drawing = Drawing(screen, map_surface, player, clock, world_map.mini_map, menu.select)
    interaction = Interaction(player, sprites, drawing, world_map.map)

    pygame.mouse.set_visible(False)

    score = START_SCORE
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and not player.shot:
                    player.shot = True

        if score > 0:
            score -= SCORE_COEFF

        player.movement()
        screen.fill('black')

        drawing.background(player.angle)
        walls, shot = walls_ray_cast(player, drawing.textures, world_map.map, world_map.WORLD_WIDTH,
                                     world_map.WORLD_HEIGHT)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.fps(clock)
        drawing.minimap(player, sprites.list_of_objects)
        drawing.weapon([shot, sprites.shot])

        interaction.interaction_objects()
        interaction.npc_action()
        interaction.clear()
        interaction.check_end(score)

        pygame.display.flip()
        clock.tick(FPS)
