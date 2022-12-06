'''Adds collision to the entity'''

from world import Component


class Collision(Component):
    events = ()
    
    def __init__(self, layer="blocking"):
        self.layer = layer
        super().__init__()