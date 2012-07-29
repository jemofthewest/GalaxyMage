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
4   4   0   0   18w 14w 14w 14w 18w 14w 14w 14w 18w 0   0   4   4   
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   18w 4g  4g  4g  4g  4g  4g  4g  18w 0   0   4   4     
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   14w 4g  4g  4g  4g  4g  4g  4g  14w 0   0   4   4     
4   4   0   0   18w 14w 20w 26w 4g  26w 20w 14w 18w 0   0   4   4     
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
