'''Component that gives the entity a name.'''

from world import Component


class Name(Component):
    '''
    Component that gives the entity a name.

    Args:
        name: String for the entity name.
    '''
    events = ()

    def __init__(self, name):
        self.name = name
        super().__init__()
