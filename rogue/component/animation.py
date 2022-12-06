'''Basic components for the ecs.'''

from bearlibterminal import terminal
from component.render import Render
from world import Component


class Animation(Component):
    '''Allows this entity to be animated'''
    events = ()

    def __init__(self):
        self.alpha = 255
        self.red = 60
        self.green = 60
        self.blue = 255
        super().__init__()

    def animate(self):
        '''Animation function to update the animation.'''
        ren = self.world.component_for_entity(self.entity, Render)

        self.blue -= 0.1
        if self.blue < 60:
            self.blue = 255

        ren.color = terminal.color_from_argb(self.alpha,
                                             self.red,
                                             self.green,
                                             int(self.blue))
