'''Position component that stores the position and takes a move event'''

from component.pushable import Pushable
from component.render import Render
from world import Component
from tilemap import TileMap


class Position(Component):
    '''Position component that stores the position and takes a move event'''
    events = ('move', )

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move_x = 0
        self.move_y = 0
        super().__init__()

    def move(self, event):
        '''move event that moves the entity'''
        for ent, tilemap in self.world.get_component(TileMap):
            new_x = self.x + event.data['x']
            new_y = self.y + event.data['y']
            if tilemap.is_blocked(new_x, new_y):
                self.send_to_entity(ent, 'collided',
                                    {'with': self.entity,
                                     'x': new_x,
                                     'y': new_y})
                return event


        for ent, (pos, ren) in self.world.get_components(Position, Render):
            if ren.layer is 'blocking':
                if (pos.x == self.x + event.data['x'] and
                        pos.y == self.y + event.data['y']):
                    self.world.send_to_entity(ent, 'collided',
                                              {'with': self.entity})
                    if self.world.has_component(ent, Pushable):
                        self.send_to_entity(ent, 'move', {'x': event.data['x'],
                                                          'y': event.data['y']})
                        continue

                    return event

        self.x += event.data['x']
        self.y += event.data['y']

        self.send("move_to", {'x': self.x, 'y': self.y})

        return event
