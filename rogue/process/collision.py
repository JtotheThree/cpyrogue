from component.position import Position
from component.velocity import Velocity
from component.collision import Collision
from tilemap import TileMap
import world


class CollisionProcessor(world.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (col, pos, vel) in self.world.get_components(Collision, Position, Velocity):
            if col.layer == "blocking":
                for ent, tilemap in self.world.get_component(TileMap):
                    if tilemap.is_blocked(pos.x + vel.x, pos.y + vel.y):
                        (vel.x, vel.y) = (0, 0)