# CONSTANT DEFINITIONS

# Colors
rock = (0.6, 0.6, 0.6)
tan = (0.7, 0.6, 0.5)
green = (0.5, 0.6, 0.4)
darkgreen = (0.4, 0.6, 0.4)

# Color variances
mediumVar = (0.05, 0.05, 0.05)
highVar = (0.1, 0.1, 0.1)

# Textures
stone = 'stone'
wood = 'wood'
grass = 'grass'

# ACTUAL MAP DATA

VERSION = 1

WIDTH = 20
HEIGHT = 20

TILE_PROPERTIES = {
    # Rock
    'r': { 'color': rock,
           'colorVar': mediumVar,
           'texture': stone,
         },
    # Wood
    'w': { 'color': tan,
           'colorVar': mediumVar,
           'texture': wood,
         },            
    # Hills
    'd': { 'color': darkgreen,
           'colorVar': highVar,
           'texture': grass,
           'smooth': True
         },            
    # Default: green grass
    '': { 'color': green,
          'colorVar': mediumVar,
          'texture': grass,
          'smooth': True
        },
    }

LAYOUT = '''
8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    
8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    
8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    
8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    
8    8    8    8    8    12w  16w  8    8    8    8    8    8    16w  12w  8    8    8    8    8    
8    8    8    8    8    20r  20r  20r  20r  8    8    20r  20r  20r  20r  20r  20r  8    8    8    
8    8    8    20r  20r  20r  8    8    8    8    8    8    8    8    8    8    20r  20r  8    8 
20r  20r  20r  20r  8    8    8    8    8    8    8    8    8    8    8    8    8    20r  20r  20r    
8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    
8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8    8
8    8    8    8    8    8    8    8    12d  12d  12d  12d  12d  12d  12d  8    8    8    8    8
8    8    8    8    8    8    8    12d  12d  16d  16d  16d  16d  16d  12d  12d  8    8    8    8
8    8    8    8    8    12d  12d  12d  16d  16d  20d  20d  20d  16d  12d  12d  12d  12d  8    8
8    8    8    12d  12d  12d  16d  16d  16d  20d  20d  24d  20d  16d  12d  12d  12d  12d  12d  12d
8    8    12d  16d  16d  16d  16d  20d  20d  20d  24d  24d  20d  16d  12d  12d  12d  12d  12d  12d
8    8    12d  16d  20d  20d  20d  20d  24d  24d  24d  24d  20d  16d  12d  12d  14d  14d  14d  14d
8    8    12d  16d  20d  24d  24d  24d  24d  24d  24d  20d  20d  16d  12d  14d  14d  16d  16d  16d
8    8    12d  16d  16d  20d  20d  20d  20d  20d  20d  20d  16d  16d  12d  14d  16d  16d  18d  18d
8    8    12d  12d  16d  16d  16d  16d  16d  16d  16d  16d  16d  12d  12d  14d  16d  18d  18d  20d   
8    8    8    12d  12d  12d  12d  12d  12d  12d  12d  12d  12d  12d  12d  14d  16d  18d  20d  20d   
'''

