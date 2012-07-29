VERSION = 1

WIDTH = 19
HEIGHT = 22

WATER_HEIGHT = 10
WATER_COLOR = (0.3, 0.3, 0.7, 0.5)

TILE_PROPERTIES = {
    'grass':  { 'color': (0.5, 0.7, 0.5),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'grass',
                'smooth': True },
    'rock':   { 'color': (0.7, 0.5, 0.3),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'stone',
                'smooth': True,
              },
    'water':  { 'color': (0.5, 0.7, 0.5),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'grass',
                'smooth': True,
                },
    'stone':  { 'color': (0.8, 0.8, 0.8),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'stone',
                'smooth': False
              },
    'wood':   { 'color': (0.7, 0.7, 0.5),
                'colorVar': (0.05, 0.05, 0.05),
                'texture': 'wood-1',
                'smooth': True },
    'marble': { 'color': (0.6, 0.6, 0.6),
                'colorVar': (0.05, 0.05, 0.05),
                'texture': 'marble-slight',
                'smooth': False},
    }

LAYOUT = '''
13grass   13grass   13grass   13grass   11water   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass
13grass   13grass   13grass   13grass   11water   11water   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass
13grass   13grass   13grass   13grass   13grass   11water   13grass   13grass   13grass   13grass   19grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass
13grass   13grass   13grass   13grass   11water   11water   18grass   18grass   19grass   18grass   25grass   20grass   18grass   18grass   18grass   13grass   13grass   13grass   13grass
13grass   13grass   13grass   11water   11water   19grass   18grass   26grass   25grass   25grass   32grass   26grass   25grass   25grass   20grass   18grass   13grass   13grass   13grass
13grass   13grass   13grass   11water   19grass   27grass   27grass   33grass   32grass   33grass   40grass   32grass   34grass   34grass   26grass   27grass   19grass   13grass   13grass
13grass   13grass   13grass   17water   25grass   25grass   34grass   40grass   39grass   41grass   48grass   33stone   27stone   27stone   27stone   33stone   26grass   18grass   13grass
13grass   13grass   19grass   18water   27grass   32grass   40grass   47grass   48grass   48grass   54grass   27stone   13marble  13marble  13marble  27stone   26grass   18grass   20grass
13grass   13grass   19grass   26grass   33grass   41grass   48grass   47grass   53grass   55grass   61grass   27stone   13marble  13marble  13marble  27stone   32grass   26grass   18grass
13grass   13grass   19grass   26grass   33grass   41grass   46grass   53grass   60grass   60grass   69grass   27stone   13marble  13marble  13marble  27stone   34grass   25grass   20grass
13grass   13grass   18grass   26grass   34grass   39grass   47grass   54grass   61grass   69grass   75grass   27stone   13marble  13marble  13marble  27stone   32grass   25grass   19grass
13grass   18grass   25grass   32grass   40grass   48grass   55grass   60grass   69grass   76grass   83grass   27stone   13marble  13marble  13marble  27stone   40grass   33grass   25grass
13grass   13grass   18grass   26grass   34grass   40grass   47grass   55grass   60grass   67grass   74grass   27stone   13marble  13marble  13marble  27stone   33grass   26grass   18grass
13grass   13grass   20grass   26grass   33grass   41grass   47grass   54grass   61grass   61grass   69grass   27stone   13marble  13marble  13marble  27stone   33grass   27grass   19grass
13grass   13grass   20grass   27grass   33grass   39grass   46grass   46grass   55grass   55grass   62grass   27stone   13marble  13marble  13marble  27stone   34grass   26grass   20grass
13grass   13grass   20grass   20grass   25grass   32grass   41grass   46grass   46grass   46grass   54grass   33stone   27stone   13marble  27stone   33stone   27grass   18grass   19grass
13grass   13grass   13grass   19grass   26grass   26grass   34grass   41grass   40grass   40grass   47grass   41grass   41grass   41grass   32grass   27grass   27grass   18grass   13grass
13grass   13grass   13grass   13grass   18grass   25grass   25grass   34grass   33grass   33grass   40grass   32grass   34grass   33grass   25grass   26grass   20grass   4water    4water
13grass   13grass   13grass   13grass   5water    18grass   19grass   25grass   25grass   25grass   34grass   27grass   25grass   27grass   20grass   18grass   4water    4water    13grass
13grass   13grass   13grass   13grass   5water    13grass   20grass   18grass   19grass   18grass   26grass   19grass   20grass   20grass   18grass   13grass   13grass   13grass   13grass
13grass   13grass   13grass   13grass   5water    13grass   13grass   13grass   13grass   13grass   19grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass
13grass   13grass   13grass   13grass   5water    13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass   13grass
'''
