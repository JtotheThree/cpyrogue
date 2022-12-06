from render.render import open_window, close_window, set_window, render
from control.control import read_input
from fps.fps import Fps
import constants
from world import World
from los.los import get_visible_points
from tilemap import TileMap

# Components
from component.animation import Animation
from component.health import Health
from component.name import Name
from component.player import Player
from component.position import Position
from component.render import Render
from component.trap import Trap
from component.velocity import Velocity
from component.collision import Collision

# Processes
from process.movement import MovementProcessor
from process.collision import CollisionProcessor


from profilehooks import profile
import random

def allows_light(tilemap, point):
    """Check if a position on the map allows light or not"""
    try:
        return tilemap[point[0]][point[1]].block_sight
    except IndexError:
        return False

def main():
    fps = Fps()
    open_window("window: title=Rogue, size={}x{}, fullscreen=false; output.vsync=false"
                .format(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    set_window('font: res/Yun_16x16_sm.png, size=16x16, codepage=437')

    world = World()

    random_seed = random.randint(0, 100000000000)
    print(f"Random seed: {random_seed}")
    random.seed(random_seed)

    player = world.create_entity(Name("Player"),
                                 Player(),
                                 Render("@", (255, 255, 255, 255),
                                        layer="blocking"),
                                 Position(0, 0),
                                 Velocity(),
                                 Collision(layer="blocking"),
                                 Health(25),
                                 Animation())

    _ = world.create_entity(Render("x", (180, 255, 100, 50), layer="trap"),
                            Position(5, 10),
                            Trap())

    tilemap = TileMap(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    world.create_entity(tilemap)

    tilemap.generate()

    collision_processor = CollisionProcessor()
    world.add_processor(collision_processor, priority=2)

    movement_processor = MovementProcessor()
    world.add_processor(movement_processor, priority=1)

    while read_input(player, world):
        player_pos = world.component_for_entity(player, Position)
        if constants.CALC_LOS:
            los_cache = get_visible_points((player_pos.x, player_pos.y),
                                           lambda p: allows_light(tilemap.tilemap, p),
                                           max_distance=30)
        else:
            los_cache = None

        world.process()
        render(world, tilemap.tilemap, los_cache)
        fps.tick()

    close_window()

    print("***FPS: {}".format(fps.current()))

if __name__ == '__main__':
    main()
