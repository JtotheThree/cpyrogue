from component.position import Position
from component.velocity import Velocity
import world

class MovementProcessor(world.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            pos.x += vel.x
            vel.x = 0
            pos.y += vel.y
            vel.y = 0
