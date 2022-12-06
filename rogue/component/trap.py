'''Component that fires an event when moved on'''

from component.position import Position
from world import Component


class Trap(Component):
    '''Component that fires an event when moved on'''
    events = ('move_to',)

    def move_to(self, event):
        '''Event: move_to'''
        pos = self.world.component_for_entity(self.entity, Position)

        x = event.data['x']
        y = event.data['y']

        if x is pos.x and y is pos.y:
            self.send_to_entity(self.entity, "set_layer", "ground")
            self.send_to_entity(event.sender, "take_damage", {'amount': 10})

        return event

        # if (event.data['x'] is self.entity.components[Position].x and
        #        event.data['y'] is self.entity.components[Position].y):
        #    self.send_to_entity(self.entity, "set_layer", "ground")
        #    self.send_to_entity(event.sender, "take_damage", {'amount': 10})
