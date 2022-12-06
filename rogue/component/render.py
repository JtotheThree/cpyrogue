'''Allows the entity to be rendered.'''
from bearlibterminal import terminal
from world import Component


class Render(Component):
    '''
    Allows the entity to be rendered.

    Args:
        char: Sets the char to be rendered.
        color: (u8, u8, u8) Foreground color of the entity.
        layer: String. Rendering and collision layer.
    '''
    events = ('set_layer', )

    def __init__(self, char, color, layer="background"):
        self.char = char
        self.color = terminal.color_from_argb(*color)
        self.layer = layer
        super().__init__()

    def set_layer(self, event):
        '''Event to change the active layer'''
        self.layer = event.data

        return event
