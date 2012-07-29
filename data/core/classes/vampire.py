# Class definition file, version 1
VERSION = 1

# Name is the class name that is displayed to the player
NAME = "Vampire"

# Stats
MOVE = 5
JUMP = 6

HP_BASE      = 64
HP_GROWTH    = 6.4
HP_MULT      = 1.0

SP_BASE      = 28
SP_GROWTH    = 2.8
SP_MULT      = 1.1

WATK_BASE    = 16
WATK_GROWTH  = 1.6
WATK_MULT    = 1.0

WDEF_BASE    = 16
WDEF_GROWTH  = 1.6
WDEF_MULT    = 0.9

MATK_BASE    = 20
MATK_GROWTH  = 2.0
MATK_MULT    = 1.1

MDEF_BASE    = 20
MDEF_GROWTH  = 2.0
MDEF_MULT    = 1.0

SPEED_BASE   = 50
SPEED_GROWTH = 2.5
SPEED_MULT   = 1.0

SPRITE_ROOT = "mage"

#ABILITIES = [(1, 'biteofthevampire'), (3, "crawl"), (5, "lifesink")]
ABILITIES = [(1, 'biteofthevampire'), (1, "crawl"), (1, "lifesink"),
             (1, "poison")]
