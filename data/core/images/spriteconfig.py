# Tuples refer to handle location, angle and weapon orientation:
# (x, y, angle, orientation)
# orientation: False means that when the weapon is upright, the attacking side
#              points left. True means it points right.


VERSION = 1

HAND = { 'fighter-unisex-standing-1' : (24, 45, 45, True),
         'fighter-unisex-melee-1'    : (19, 39, -30, True),
         'fighter-unisex-melee-2'    : (22, 36, 0, True),
         'fighter-unisex-melee-3'    : (37, 40, 20, True),
         'fighter-unisex-melee-4'    : (41, 43, 45, True),
         'archer-female-standing-1'  : (17, 44, -45, False),
         'archer-male-standing-1'    : (17, 44, -45, False),
         'ranger-female-standing-1'  : (25, 45, -45, False),
         'ranger-male-standing-1'    : (25, 45, -45, False),
         'rogue-female-standing-1'   : (44, 39, 45, True),
         'rogue-male-standing-1'     : (45, 39, 45, True)
       }

GRIP = { 'composite-bow'    : (29, 33, -45, False),
         'short-bow'        : (30, 33, -45, False),
         'long-bow'         : (28, 35, -45, False),
         'dagger'           : (35, 35, -45, False),
         'fine-short-sword' : (37, 37, -45, False),
         'fine-long-sword'  : (39, 39, -45, False),
         'short-sword'      : (37, 37, -45, False),
         'long-sword'       : (39, 39, -45, False),
       }
