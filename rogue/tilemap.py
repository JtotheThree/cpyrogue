'''Tile and TileMap for generating and storing the map.'''

from random import randint

import constants
from bearlibterminal import terminal
from tiles import Tile
from world import Component
# from profilehooks import profile

TILE_WALL_COLOR = (255, 150, 180, 150)
TILE_FLOOR_COLOR = (255, 55, 50, 55)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


class Feature:
    def __init__(self, kind, x1, x2, y1, y2, variant=None):
        self.kind = kind
        self.variant = variant

        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

        self.w = self.x2 - self.x1
        self.h = self.y2 - self.y1

        self.data = [[Tile('#', TILE_WALL_COLOR, True)
                     for y in range(self.h)]
                     for x in range(self.w)]

        self.neighbor_north = None
        self.wall_north = False
        self.neighbor_east = None
        self.wall_east = False
        self.neighbor_south = None
        self.wall_south = False
        self.neighbor_west = None
        self.wall_west = False

        self.generate()

    def center(self):
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        return (cx, cy)

    def generate(self):
        #print(f"Kind: {self.kind} Variant: {self.variant} | x1: {self.x1} x2: {self.x2} w: {self.w} | y1: {self.y1} y2: {self.y2} h: {self.h}")
        for x in range(0, self.w): # Make room for walls
            for y in range(0, self.h):
                self.data[x][y] = Tile(' ', TILE_FLOOR_COLOR, False, background=(255, 30, 25, 30))
    
    def create_door(self, x, y):
        print(f"Creating door at {x} {y}")
        x = x - self.x1
        y = y - self.y1
        print(f"Translated {x} {y}")
        print(f"Feature {self.x1} {self.x2} {self.y1} {self.y2}")

        self.data[x][y] = Tile('=', TILE_FLOOR_COLOR, False, background=(255, 80, 25, 30))

    def fill_walls(self):
        self.fill_wall(NORTH)
        self.fill_wall(EAST)
        self.fill_wall(SOUTH)
        self.fill_wall(WEST)
    
    def fill_wall(self, direction):
        if direction == NORTH:
            for x in range(0, self.w):
                self.data[x][0] = Tile('#', TILE_WALL_COLOR, True)
        if direction == SOUTH:
            for x in range(0, self.w):
                self.data[x][self.h - 1] = Tile('#', TILE_WALL_COLOR, True)
        if direction == EAST:
            for y in range(0, self.h):
                self.data[0][y] = Tile('#', TILE_WALL_COLOR, True)
        if direction == WEST:
            for y in range(0, self.h):
                self.data[self.w - 1][y] = Tile('#', TILE_WALL_COLOR, True) 



class TileMap(Component):
    '''Generates and stores the level tilemap'''
    events = ()

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tilemap = [[Tile('#', TILE_WALL_COLOR, True)
                        for y in range(height)]
                        for x in range(width)]
        self.features = []

        super().__init__()

    def is_blocked(self, x, y):
        '''Returns true if the tile blocks movement.'''
        return self.tilemap[x][y].blocked

    

    def generate(self):
        '''Generates the tilemap'''
        from component.player import Player
        from component.position import Position

        failures = 0
        last_failed = False

        tx = 0
        ty = 0
        tdir = NORTH

        x1 = randint(1, self.width - constants.MAP_ROOM_MAX_SIZE - 1)
        x2 = x1 + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
        y1 = randint(1, self.height - constants.MAP_ROOM_MAX_SIZE - 1)
        y2 = y1 + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)

        # Generate first feature around player
        feature = Feature('room', x1, x2, y1, y2)
        self.features.append(feature)

        # Set the Player Spawn in the First Room
        for _, (_, pos) in self.world.get_components(Player, Position):
            pos.x = randint(x1 + 2, x2 - 2)
            pos.y = randint(y1 + 2, y2 - 2)
            print(f"Player Spawn {pos.x}, {pos.y}")
    
        last_good_feature = len(self.features) - 1
        

        while failures < constants.MAP_MAX_FAILURES:
            prev_feature = self.features[last_good_feature]

            # Pick a random direction
            tdir = randint(0, 3)

            # Pick an exit area from the previous feature
            if tdir == NORTH:
                if (prev_feature.x2 - prev_feature.x1) < 2:
                    exit_x = prev_feature.x1
                else:
                    exit_x = randint(prev_feature.x1 + 1, prev_feature.x2 - 1)
                exit_y = prev_feature.y1 # NORTH
            elif tdir == EAST:
                exit_x = prev_feature.x2 # EAST
                if (prev_feature.y2 - prev_feature.y1) < 2:
                    exit_y = prev_feature.y1
                else:
                    exit_y = randint(prev_feature.y1 + 1, prev_feature.y2 - 1)
            elif tdir == SOUTH:
                if (prev_feature.x2 - prev_feature.x1) < 2:
                    exit_x = prev_feature.x1
                else:
                    exit_x = randint(prev_feature.x1 + 1, prev_feature.x2 - 1)
                exit_y = prev_feature.y2 # SOUTH
            elif tdir == WEST:
                exit_x = prev_feature.x1 # WEST
                if (prev_feature.y2 - prev_feature.y1) < 2:
                    exit_y = prev_feature.y1
                else:
                    exit_y = randint(prev_feature.y1 + 1, prev_feature.y2 - 1)
            else:
                print("Reached end of exit chosing????")
            
            which_feature = randint(0, 1)

            if which_feature == 0: # HALLWAY
                kind = 'hallway'
                if tdir == NORTH:
                    variant = 'north'
                    x1 = exit_x
                    x2 = exit_x + randint(1, 2)
                    y1 = exit_y - randint(1, 10)
                    y2 = exit_y
                elif tdir == EAST:
                    variant = 'east'
                    x1 = exit_x 
                    x2 = exit_x + randint(1, 10)
                    y1 = exit_y
                    y2 = exit_y + randint(1, 2)
                elif tdir == SOUTH:
                    variant = 'south'
                    x1 = exit_x 
                    x2 = exit_x + randint(1, 2)
                    y1 = exit_y
                    y2 = exit_y + randint(1, 10)
                elif tdir == WEST:
                    variant = 'west'
                    x1 = exit_x - randint(1, 10)
                    x2 = exit_x
                    y1 = exit_y
                    y2 = exit_y + randint(1, 2)
                else:
                    print("Reached the end of hallway direction choosing???")
            elif which_feature == 1: # ROOM
                kind = 'room'
                if tdir == NORTH:
                    variant = 'north'
                    x1 = exit_x + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
                    x2 = exit_x
                    y1 = exit_y - randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
                    y2 = exit_y
                elif tdir == EAST:
                    variant = 'east'
                    x1 = exit_x 
                    x2 = exit_x + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
                    y1 = exit_y
                    y2 = exit_y + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
                elif tdir == SOUTH:
                    variant = 'south'
                    x1 = exit_x 
                    x2 = exit_x + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
                    y1 = exit_y
                    y2 = exit_y + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
                elif tdir == WEST:
                    variant = 'west'
                    x1 = exit_x - randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)
                    x2 = exit_x
                    y1 = exit_y
                    y2 = exit_y + randint(constants.MAP_ROOM_MIN_SIZE, constants.MAP_ROOM_MAX_SIZE)

            feature = Feature(kind, x1, x2, y1, y2, variant=variant)

            (valid, intersection) = self.valid(feature, tdir)

            if valid:
                # feature.fill_wall(tdir)
                if tdir == NORTH:
                    prev_feature.neighbor_north = feature
                    feature.neighbor_south = prev_feature
                elif tdir == EAST:
                    prev_feature.neighbor_east = feature
                    feature.neighbor_west = prev_feature
                elif tdir == SOUTH:
                    prev_feature.neighbor_south = feature
                    feature.neighbor_north = prev_feature
                elif tdir == WEST:
                    prev_feature.neighbor_west = feature
                    feature.neighbor_east = prev_feature
                
                #print(f"Success Kind: {feature.kind}, Variant: {feature.variant} X1: {feature.x1} X2: {feature.x2} Y1: {feature.y1} Y2: {feature.y2} W: {feature.w} H: {feature.h}")
                self.features.append(feature)
                last_good_feature = len(self.features) - 1
            else:
                #print(f"Failure Kind: {feature.kind}, Variant: {feature.variant} X1: {feature.x1} X2: {feature.x2} Y1: {feature.y1} Y2: {feature.y2} W: {feature.w} H: {feature.h}")
                failures += 1
                last_failed = True
                last_good_feature = len(self.features) - 2
                if last_good_feature < 0:
                    last_good_feature = 0

        self.create_walls_and_doors()
        self.dig()

        return

    def create_walls_and_doors(self):
        for feature in self.features:
            if feature.kind == 'room':
                if feature.neighbor_north is not None:
                    if feature.neighbor_south.wall_south:
                        continue
                    feature.fill_wall(NORTH)
                    x1 = max(feature.x1, feature.neighbor_north.x1)
                    x2 = min(feature.x2, feature.neighbor_north.x2)
                    x = (x2 - x1) // 2 + x1
                    y = feature.y1
                    feature.create_door(x, y)
                    feature.wall_north = True
                if feature.neighbor_east is not None:
                    if feature.neighbor_south.wall_west:
                        continue
                    feature.fill_wall(EAST)
                    y1 = max(feature.y1, feature.neighbor_east.y1)
                    y2 = min(feature.y2, feature.neighbor_east.y2)
                    x = feature.x2 - 1
                    y = (y2 - y1) // 2 + y1
                    feature.create_door(x, y)
                    feature.wall_east = True
                if feature.neighbor_south is not None:
                    if feature.neighbor_south.wall_north:
                        continue
                    feature.fill_wall(SOUTH)
                    x1 = max(feature.x1, feature.neighbor_south.x1)
                    x2 = min(feature.x2, feature.neighbor_south.x2)
                    x = (x2 - x1) // 2 + x1
                    y = feature.y2 - 1
                    feature.create_door(x, y)
                    feature.wall_south = True
                if feature.neighbor_west is not None:
                    if feature.neighbor_south.wall_east:
                        continue
                    feature.fill_wall(WEST)
                    y1 = max(feature.y1, feature.neighbor_west.y1)
                    y2 = min(feature.y2, feature.neighbor_west.y2)
                    x = feature.x1
                    y = (y2 - y1) // 2 + y1
                    feature.create_door(x, y)
                    feature.wall_west = True

    def dig(self):
        for feature in self.features:
            fx = 0
            fy = 0

            for x in range(feature.x1, feature.x2):
                for y in range(feature.y1, feature.y2):
                    if x >= 0 and x < self.width and y >= 0 and y < self.height:
                        self.tilemap[x][y] = feature.data[fx][fy]
                    fy += 1
                fy = 0
                fx += 1

    def valid(self, feature, direction):
        if feature.x1 <= 0 or feature.x2 >= self.width or feature.y1 <= 0 or feature.y2 >= self.height:
            return (False, None)

        for test in self.features:
            if (feature.x1 < test.x2 and feature.x2 > test.x1 and 
                feature.y1 < test.y2 and feature.y2 > test.y1):
                if feature.kind == 'hallway':
                    if direction == NORTH:
                        if test.neighbor_south is None:
                            feature.y1 = test.y2
                            if feature.y2 - feature.y1 < 1:
                                return (False, None)
                            test.neighbor_south = feature
                            return (True, test)
                        else:
                            return (False, None)    
                    elif direction == SOUTH:
                        if test.neighbor_north is None:
                            feature.y2 = test.y1
                            if feature.y2 - feature.y1 < 1:
                                return (False, None)
                            test.neighbor_north = feature
                            return (True, test)
                        else:
                            return (False, None)
                    elif direction == EAST:
                        if test.neighbor_west is None:
                            feature.x1 = test.x2
                            if feature.x2 - feature.x1 < 1:
                                return (False, None)
                            test.neighbor_west = feature
                            return (True, test)
                        else:
                            return (False, None)
                    elif direction == WEST:
                        if test.neighbor_east is None:
                            feature.x1 = test.x2
                            if feature.x2 - feature.x1 < 1:
                                return (False, None)
                            test.neighbor_east = feature
                            return (True, test)
                        else:
                            return (False, None)
                    return (True, test)
                return (False, test)

        return (True, None)