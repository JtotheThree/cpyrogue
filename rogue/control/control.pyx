# cython: languagelevel=3

from world import World
from component.velocity import Velocity

cdef extern from "BearLibTerminal.h":
    # Input
    int terminal_has_input()
    int terminal_read()

cdef _read_input(player, world):
    cdef int key

    if terminal_has_input():
        key = terminal_read()

        vel = world.component_for_entity(player, Velocity)

        if key is TK_ESCAPE:
            return False
        elif key is TK_LEFT:
            (vel.x, vel.y) = (-1, 0)
        elif key is TK_RIGHT:
            (vel.x, vel.y) = (1, 0)
        elif key is TK_UP:
            (vel.x, vel.y) = (0, -1)
        elif key is TK_DOWN:
            (vel.x, vel.y) = (0, 1)

    return True

# cdef _read_input(player, world):
#    cdef int key

#    if terminal_has_input():
#        key = terminal_read()

#        if key is TK_ESCAPE:
#            return False
#        elif key is TK_LEFT:
#            world.send_to_entity(player, "move", {'x': -1, 'y': 0})
#        elif key is TK_RIGHT:
#            world.send_to_entity(player, "move", {'x': 1, 'y': 0})
#        elif key is TK_UP:
#            world.send_to_entity(player, "move", {'x': 0, 'y': -1})
#        elif key is TK_DOWN:
#            world.send_to_entity(player, "move", {'x': 0, 'y': 1})

#    return True

def read_input(player, world):
    return _read_input(player, world)

TK_A                = 0x04
TK_B                = 0x05
TK_C                = 0x06
TK_D                = 0x07
TK_E                = 0x08
TK_F                = 0x09
TK_G                = 0x0A
TK_H                = 0x0B
TK_I                = 0x0C
TK_J                = 0x0D
TK_K                = 0x0E
TK_L                = 0x0F
TK_M                = 0x10
TK_N                = 0x11
TK_O                = 0x12
TK_P                = 0x13
TK_Q                = 0x14
TK_R                = 0x15
TK_S                = 0x16
TK_T                = 0x17
TK_U                = 0x18
TK_V                = 0x19
TK_W                = 0x1A
TK_X                = 0x1B
TK_Y                = 0x1C
TK_Z                = 0x1D
TK_1                = 0x1E
TK_2                = 0x1F
TK_3                = 0x20
TK_4                = 0x21
TK_5                = 0x22
TK_6                = 0x23
TK_7                = 0x24
TK_8                = 0x25
TK_9                = 0x26
TK_0                = 0x27
TK_RETURN           = 0x28
TK_ENTER            = 0x28
TK_ESCAPE           = 0x29
TK_BACKSPACE        = 0x2A
TK_TAB              = 0x2B
TK_SPACE            = 0x2C
TK_MINUS            = 0x2D
TK_EQUALS           = 0x2E
TK_LBRACKET         = 0x2F
TK_RBRACKET         = 0x30
TK_BACKSLASH        = 0x31
TK_SEMICOLON        = 0x33
TK_APOSTROPHE       = 0x34
TK_GRAVE            = 0x35
TK_COMMA            = 0x36
TK_PERIOD           = 0x37
TK_SLASH            = 0x38
TK_F1               = 0x3A
TK_F2               = 0x3B
TK_F3               = 0x3C
TK_F4               = 0x3D
TK_F5               = 0x3E
TK_F6               = 0x3F
TK_F7               = 0x40
TK_F8               = 0x41
TK_F9               = 0x42
TK_F10              = 0x43
TK_F11              = 0x44
TK_F12              = 0x45
TK_PAUSE            = 0x48
TK_INSERT           = 0x49
TK_HOME             = 0x4A
TK_PAGEUP           = 0x4B
TK_DELETE           = 0x4C
TK_END              = 0x4D
TK_PAGEDOWN         = 0x4E
TK_RIGHT            = 0x4F
TK_LEFT             = 0x50
TK_DOWN             = 0x51
TK_UP               = 0x52
TK_KP_DIVIDE        = 0x54
TK_KP_MULTIPLY      = 0x55
TK_KP_MINUS         = 0x56
TK_KP_PLUS          = 0x57
TK_KP_ENTER         = 0x58
TK_KP_1             = 0x59
TK_KP_2             = 0x5A
TK_KP_3             = 0x5B
TK_KP_4             = 0x5C
TK_KP_5             = 0x5D
TK_KP_6             = 0x5E
TK_KP_7             = 0x5F
TK_KP_8             = 0x60
TK_KP_9             = 0x61
TK_KP_0             = 0x62
TK_KP_PERIOD        = 0x63
TK_SHIFT            = 0x70
TK_CONTROL          = 0x71
TK_ALT              = 0x72

# Mouse events/states.
TK_MOUSE_LEFT       = 0x80 # Buttons
TK_MOUSE_RIGHT      = 0x81
TK_MOUSE_MIDDLE     = 0x82
TK_MOUSE_X1         = 0x83
TK_MOUSE_X2         = 0x84
TK_MOUSE_MOVE       = 0x85 # Movement event
TK_MOUSE_SCROLL     = 0x86 # Mouse scroll event
TK_MOUSE_X          = 0x87 # Cusor position in cells
TK_MOUSE_Y          = 0x88
TK_MOUSE_PIXEL_X    = 0x89 # Cursor position in pixels
TK_MOUSE_PIXEL_Y    = 0x8A
TK_MOUSE_WHEEL      = 0x8B # Scroll direction and amount
TK_MOUSE_CLICKS     = 0x8C # Number of consecutive clicks

# If key was released instead of pressed, it's code will be OR'ed with VK_KEY_RELEASED.
TK_KEY_RELEASED     = 0x100

# Virtual key-codes for internal terminal states/variables.
# These can be accessed via terminal_state function.
TK_WIDTH            = 0xC0 # Terminal width in cells
TK_HEIGHT           = 0xC1 # Terminal height in cells
TK_CELL_WIDTH       = 0xC2 # Cell width in pixels
TK_CELL_HEIGHT      = 0xC3 # Cell height in pixels
TK_COLOR            = 0xC4 # Current foregroung color
TK_BKCOLOR          = 0xC5 # Current background color
TK_LAYER            = 0xC6 # Current layer
TK_COMPOSITION      = 0xC7 # Current composition state
TK_CHAR             = 0xC8 # Translated ANSI code of last produced character
TK_WCHAR            = 0xC9 # Unicode codepoint of last produced character
TK_EVENT            = 0xCA # Last dequeued event
TK_FULLSCREEN       = 0xCB # Fullscreen state

# Other events.
TK_CLOSE            = 0xE0
TK_RESIZED          = 0xE1

# Generic mode enum. Used in Terminal.composition call only.
TK_OFF              =    0
TK_ON               =    1

# Input result codes for terminal_read_str function.
TK_INPUT_NONE       =    0
TK_INPUT_CANCELLED  =   -1

# Text printing alignment.
TK_ALIGN_DEFAULT    =    0
TK_ALIGN_LEFT       =    1
TK_ALIGN_RIGHT      =    2
TK_ALIGN_CENTER     =    3
TK_ALIGN_TOP        =    4
TK_ALIGN_BOTTOM     =    8
TK_ALIGN_MIDDLE     =   12