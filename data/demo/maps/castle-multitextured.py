# CONSTANT DEFINITIONS

# Colors
white = (0.8, 0.8, 0.8)
grey = (0.6, 0.6, 0.6)
tan = (0.8, 0.8, 0.8)
green = (0.3, 0.5, 0.3)
red = (0.8, 0.3, 0.0)
brown = (0.5, 0.3, 0.15)
blue = (0.0, 0.3, 0.8)

# Color variances
lowVar = (0.0, 0.0, 0.0)
mediumVar = (0.08, 0.08, 0.08)
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
    'w': { 'color': [tan,brown],
           'colorVar': mediumVar,
           'texture': [wood],
           'cornerHeights': pointy,
          },
    # White stone, left edge is higher
    'l': { 'color': [brown,white],
           'colorVar': mediumVar,
           'texture': [wood,stone],
           'cornerHeights': raisedLeft },
    # White stone, right edge is higher
    'r': { 'color': [brown,white],
           'colorVar': mediumVar,
           'texture': [wood,stone],
           'cornerHeights': raisedRight },
    # White stone, back edge is higher
    'u': { 'color': [white],
           'colorVar': mediumVar,
           'texture': stone,
           'cornerHeights': raisedBack },
    # Grey marble
    'g': { 'color': [grey,tan],
           'colorVar': mediumVar,
           'texture': [marble,wood],
           'cornerHeights': flat },
    # Tan wood
    't': { 'color': [brown],
           'colorVar': mediumVar,
           'texture': wood,
           'cornerHeights': flat },
    # Default: green grass
    '': { 'color': [green,brown],
          'colorVar': [mediumVar,highVar],
          'texture': [grass,stone],
          'cornerHeights': flat },
    
    'q' : { 'color': [red,blue,blue,blue,green],
            'colorVar' : [highVar, lowVar, mediumVar, lowVar, mediumVar],
            'texture': [marble,stone],
            'cornerHeights': flat 
            }
    }

LAYOUT = '''
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4 
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    18r  20r  22r  24r  26r  26l  24l  22l  20l  18l  4    4    4    4
4    4    4    4    18r  4g   4g   4g   4g   4g   4g   4g   4g   18l  4    4    4    4
4    4    4    4    18r  4g   4g   4g   9q   9q   4g   4g   4g   18l  4    4    4    4
4    4    4    4    18r  4g   4g   4g   9q   9q   4g   4g   4g   18l  4    4    4    4
4    4    4    4    18r  4g   4g   4g   4g   4g   4g   4g   4g   18l  4    4    4    4
4    4    4    4    18r  4g   4g   4g   4g   4g   4g   4g   4g   18l  4    4    4    4
4    4    4    4    18r  20r  22r  26r  4g   4g   26l  22l  20l  18l  4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4    4
'''

