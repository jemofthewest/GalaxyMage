# Class definition file, version 1
VERSION = 1

# Name is the class name that is displayed to the player
NAME = "Healer"

# Stats
MOVE = 5
JUMP = 6

HP_BASE      = 56
HP_GROWTH    = 5.6
HP_MULT      = 0.9

SP_BASE      = 36
SP_GROWTH    = 3.6
SP_MULT      = 1.1

WATK_BASE    = 16
WATK_GROWTH  = 1.6
WATK_MULT    = 0.9

WDEF_BASE    = 16
WDEF_GROWTH  = 1.6
WDEF_MULT    = 0.9

MATK_BASE    = 20
MATK_GROWTH  = 2.0
MATK_MULT    = 1.1

MDEF_BASE    = 24
MDEF_GROWTH  = 2.4
MDEF_MULT    = 1.1

SPEED_BASE   = 45
SPEED_GROWTH = 2.25
SPEED_MULT   = 1.0

#ABILITIES = [(1, "mend"), (3, "wingedfeet"), (10, "righteousness"), (5, "regenerate")]
ABILITIES = [(1, "mend"), (1, "wingedfeet"), (10, "righteousness"),
             (1, "protect")]

SPRITE_ROOT = "healer"
