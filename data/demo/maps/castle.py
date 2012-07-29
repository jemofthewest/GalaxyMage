# CONSTANT DEFINITIONS

# Colors
white = (0.8, 0.8, 0.8)
grey = (0.6, 0.6, 0.6)
tan = (0.8, 0.8, 0.8)
green = (0.5, 0.75, 0.5)

# Color variances
lowVar = (0.0, 0.0, 0.0)
mediumVar = (0.05, 0.05, 0.05)
highVar = (0.2, 0.2, 0.2)

# Corner heights
height = 2
flat = (0, 0, 0, 0)
raisedLeft = (height, 0, height, 0)
raisedRight = (0, height, 0, height)
raisedBack = (height, height, 0, 0)
pointy = (-2*height, -2*height, -2*height, -2*height)

# Textures
stone = 'stone'
marble = 'marble-slight'
wood = 'wood-2'
grass = 'grass'

# ACTUAL MAP DATA

VERSION = 1

WIDTH = 17
HEIGHT = 22

TILE_PROPERTIES = {
    # White stone, flat top
    'w': { 'color': white,
           'colorVar': mediumVar,
           'texture': stone,
           'cornerHeights': pointy,
          },
    # White stone, left edge is higher
    'l': { 'color': white,
           'colorVar': mediumVar,
           'texture': stone,
           'cornerHeights': raisedLeft },
    # White stone, right edge is higher
    'r': { 'color': white,
           'colorVar': mediumVar,
           'texture': stone,
           'cornerHeights': raisedRight },
    # White stone, back edge is higher
    'u': { 'color': white,
           'colorVar': mediumVar,
           'texture': stone,
           'cornerHeights': raisedBack },
    # Grey marble
    'g': { 'color': grey,
           'colorVar': mediumVar,
           'texture': marble,
           'cornerHeights': flat },
    # Tan wood
    't': { 'color': tan,
           'colorVar': mediumVar,
           'texture': wood,
           'cornerHeights': flat },
    # Default: green grass
    '': { 'color': green,
          'colorVar': highVar,
          'texture': grass,
          'cornerHeights': flat },
    }

LAYOUT = '''
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    
4    4    4    4    0    0    0    0    0    0    0    0    0    4    4    4    4    
4    4    4    0    0    0    0    0    0    0    0    0    0    0    4    4    4    
4    4    0    0    18l  18w  18w  18w  18u  18w  18w  18w  18r  0    0    4    4    
4    4    0    0    18w  4g   4g   4g   4g   4g   4g   4g   18w  0    0    4    4   
4    4    0    0    18w  4g   4g   4g   4g   4g   4g   4g   18w  0    0    4    4   
4    4    0    0    18l  4g   4g   4g   4g   4g   4g   4g   18r  0    0    4    4   
4    4    0    0    18w  4g   4g   4g   4g   4g   4g   4g   18w  0    0    4    4   
4    4    0    0    18w  4g   4g   4g   4g   4g   4g   4g   18w  0    0    4    4   
4    4    0    0    18l  20l  22l  26l  4g   26r  22r  20r  18r  0    0    4    4   
4    4    0    0    0    0    0    0    4t   0    0    0    0    0    0    4    4   
4    4    4    0    0    0    0    0    4t   0    0    0    0    0    4    4    4   
4    4    4    4    0    0    0    0    4t   0    0    0    0    4    4    4    4   
4    4    4    4    4    4    0    0    4t   0    0    4    4    4    4    4    4   
4    4    4    4    4    4    0    0    4t   0    0    4    4    4    4    4    4   
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4   
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4   
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4   
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4   
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4   
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
'''

