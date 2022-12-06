'''Contains the base tile and unique tile types'''

from bearlibterminal import terminal


class Tile:
    '''Map tile'''
    def __init__(self, char, color, blocked, background=None,
                 block_sight=None, trait=None):
        self.char = ord(char)
        if background is None:
            self.background = terminal.color_from_argb(255, 0, 0, 0)
        else:
            self.background = terminal.color_from_argb(*background)
        self.color = terminal.color_from_argb(*color)
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

        self.block_sight = not blocked

        self.explored = False

        self.trait = trait
