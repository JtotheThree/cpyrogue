'''Component that gives an entity desired movement.'''

from world import Component


class Velocity(Component):
    events = ()

    def __init__(self):
        self.x = 0
        self.y = 0
        super().__init__()