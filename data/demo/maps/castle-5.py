# MAP DATA

# Version of the map file format
VERSION = 1

# Width and height of the map
WIDTH = 17
HEIGHT = 22

# Tile properties
TILE_PROPERTIES = {
    'w': { 'color': (0.8, 0.8, 0.8),
           'colorVar': (0.05, 0.05, 0.05),
           'texture': 'stone' }, 
    'l': { 'color': (0.8, 0.8, 0.8),
           'colorVar': (0.05, 0.05, 0.05),
           'texture': 'stone',
           'cornerHeights': (2, 0, 2, 0) }, 
    'r': { 'color': (0.8, 0.8, 0.8),
           'colorVar': (0.05, 0.05, 0.05),
           'texture': 'stone',
           'cornerHeights': (0, 2, 0, 2) },
    'u': { 'color': (0.8, 0.8, 0.8),
           'colorVar': (0.05, 0.05, 0.05),
           'texture': 'stone',
           'cornerHeights': (2, 2, 0, 0) }, 
    'g': { 'color': (0.6, 0.6, 0.6),
           'colorVar': (0.05, 0.05, 0.05),
           'texture': 'marble-slight' }, 
    't': { 'color': (0.7, 0.5, 0.3),
           'texture': 'wood' }, 
    '':  { 'color': (0.5, 0.7, 0.5),
           'colorVar': (0.2, 0.2, 0.2),
           'texture': 'grass' }, 
    }

# Layout of map tiles
LAYOUT = '''
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   
4   4   4   4   0   0   0   0   0   0   0   0   0   4   4   4   4   
4   4   4   0   0   0   0   0   0   0   0   0   0   0   4   4   4   
4   4   0   0   18l 14w 14w 14w 18u 14w 14w 14w 18r 0   0   4   4   
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   18l 4g  4g  4g  4g  4g  4g  4g  18r 0   0   4   4     
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   18l 14r 20r 26r 4g  26l 20l 14l 18r 0   0   4   4     
4   4   0   0   0   0   0   0   4t  0   0   0   0   0   0   4   4     
4   4   4   0   0   0   0   0   4t  0   0   0   0   0   4   4   4     
4   4   4   4   0   0   0   0   4t  0   0   0   0   4   4   4   4     
4   4   4   4   4   4   0   0   4t  0   0   4   4   4   4   4   4     
4   4   4   4   4   4   0   0   4t  0   0   4   4   4   4   4   4     
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4     
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4     
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4     
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4     
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4     
4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4
'''
