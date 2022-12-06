'''Gives the entity health'''

from component.name import Name
from world import Component


class Health(Component):
    '''Gives the entity health
    Args:
        health: Max health. Current health starts as this param.
    '''
    events = ('take_damage', )

    def __init__(self, health):
        self.health = health
        self.max_health = health
        super().__init__()

    def take_damage(self, event):
        '''Event: take_damage
        Damages the entity.'''
        name = self.world.component_for_entity(self.entity, Name)

        self.health -= event.data['amount']
        print("{} took {} damage.".format(name.name,
                                          event.data['amount']))

        if self.health <= 0:
            print("OH MY GOD IM FUCKING DEAD")

        return event
