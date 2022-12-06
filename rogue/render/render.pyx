# cython: languagelevel=3
# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1

from world import World
from tilemap import TileMap
import constants
from component.render import Render
from component.position import Position

DARK_COLOR = color_from_argb(255, 20, 20, 30)
DARK_BKGND = color_from_argb(255, 10, 10, 20)

cdef extern from "BearLibTerminal.h":
    # Init
    int terminal_open()
    void terminal_clear()
    void terminal_refresh()
    void terminal_close()
    int terminal_set(const char* s)

    # Rendering
    ctypedef unsigned long color_t;
    void terminal_layer(int index)
    color_t color_from_argb(unsigned char a, unsigned char r, unsigned char g, unsigned char b)
    void terminal_color(color_t color)
    void terminal_bkcolor(color_t color)
    void terminal_put(int x, int y, int code)

cdef _render(world, tilemap, los_cache):
    cdef int x, y, ch
    cdef unsigned int color, background, prev_background

    terminal_clear()
    terminal_layer(0)

    for x in range(constants.SCREEN_WIDTH):
        for y in range(constants.SCREEN_HEIGHT):
            color = tilemap[x][y].color
            background = tilemap[x][y].background
            ch = tilemap[x][y].char

            if constants.FOV:
                if(x, y) in los_cache:
                    tilemap[x][y].explored = True

                if(x, y) not in los_cache:
                    color = DARK_COLOR
                    background = DARK_BKGND

                if not tilemap[x][y].explored:
                    continue

            terminal_bkcolor(background)
            terminal_color(color)
            terminal_put(x, y, ch)

    for ent, (pos, render) in world.get_components(Position, Render):
        if (pos.x < 0 or pos.x > constants.SCREEN_WIDTH or
                pos.y < 0 or pos.y > constants.SCREEN_HEIGHT):
            continue

        if render.layer is 'background':
            terminal_layer(constants.LAYER_BACKGROUND)
        elif render.layer is 'ground':
            terminal_layer(constants.LAYER_GROUND)
        elif render.layer is 'blocking':
            terminal_layer(constants.LAYER_BLOCKING)
        else:
            continue

        terminal_color(render.color)
        terminal_put(pos.x, pos.y, ord(render.char))

    terminal_bkcolor(color_from_argb(255, 0, 0, 0))
    terminal_refresh()

def render(world, tilemap, los_cache):
    _render(world, tilemap, los_cache)

def open_window(window_settings):
    terminal_open()
    terminal_set(str.encode(window_settings))
    terminal_clear()
    terminal_refresh()

def set_window(window_settings):
    terminal_set(str.encode(window_settings))

def close_window():
    terminal_close()