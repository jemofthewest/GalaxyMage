VERSION = 1

WIDTH = 24
HEIGHT = 20

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
                'waterColor': (0.4, 0.4, 0.7, 1.0),
                'waterHeight': 20
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
25grass   25grass   25grass   25grass   25grass   25grass   29grass   29grass   32grass   27grass   28grass   25grass   25grass   25grass   25grass   25grass   25grass   32grass   39grass   37grass   39grass   44grass   39grass   39grass
25grass   25grass   25grass   25grass   25grass   28grass   31grass   32grass   37grass   32grass   32grass   29grass   25grass   25grass   25grass   25grass   30grass   37grass   44grass   46grass   44grass   52grass   44grass   46grass
25grass   25grass   25grass   25grass   25grass   29grass   31grass   37grass   40grass   36grass   33grass   29grass   25grass   25grass   25grass   30grass   38grass   45grass   45grass   52grass   53grass   60grass   52grass   51grass
25grass   25grass   25grass   25grass   28grass   31grass   37grass   41grass   43grass   41grass   36grass   33grass   27grass   31grass   30grass   31grass   39grass   45grass   52grass   60grass   59grass   67grass   59grass   58grass
25grass   25grass   25grass   25grass   25grass   27grass   32grass   37grass   39grass   35grass   33grass   29grass   32grass   38grass   39grass   39grass   45grass   45grass   52grass   59grass   66grass   72grass   65grass   60grass
25grass   25grass   26grass   26grass   27grass   31grass   31grass   33grass   35grass   32grass   33grass   32grass   38grass   39grass   44grass   46grass   53grass   52grass   59grass   65grass   73grass   80grass   74grass   66grass
25grass   27grass   31grass   31grass   29grass   32grass   31grass   29grass   32grass   28grass   28grass   31grass   39grass   45grass   51grass   52grass   59grass   52grass   51grass   59grass   65grass   73grass   66grass   59grass
28grass   29grass   30grass   32grass   34grass   36grass   33grass   32grass   30grass   30grass   27grass   32grass   39grass   45grass   53grass   60grass   65grass   59grass   51grass   58grass   60grass   66grass   58grass   60grass
28grass   31grass   33grass   37grass   36grass   39grass   36grass   37grass   33grass   31grass   30grass   37grass   44grass   53grass   58grass   67grass   72grass   67grass   60grass   51grass   52grass   58grass   53grass   53grass
28grass   31grass   33grass   35grass   40grass   42grass   39grass   36grass   32grass   31grass   33grass   39grass   39grass   46grass   52grass   58grass   65grass   59grass   53grass   46grass   44grass   52grass   44grass   46grass
31grass   32grass   37grass   39grass   41grass   44grass   41grass   40grass   36grass   34grass   31grass   35grass   38grass   45grass   51grass   53grass   59grass   53grass   52grass   44grass   39grass   46grass   38grass   39grass
27grass   31grass   33grass   36grass   38grass   41grass   39grass   37grass   33grass   30grass   27grass   30grass   39grass   37grass   44grass   45grass   53grass   46grass   44grass   38grass   37grass   37grass   32grass   32grass
27grass   30grass   32grass   36grass   36grass   39grass   37grass   36grass   33grass   30grass   5water    4water    31grass   39grass   38grass   39grass   45grass   38grass   39grass   37grass   30grass   30grass   25grass   25grass
26grass   30grass   30grass   33grass   33grass   36grass   34grass   32grass   30grass   30grass   26grass   4water    4water    32grass   31grass   32grass   38grass   40grass   31grass   31grass   25grass   25grass   25grass   25grass
25grass   28grass   31grass   31grass   31grass   33grass   30grass   29grass   31grass   28grass   4water    4water    4water    4water    25grass   31grass   41grass   49grass   39grass   33grass   25grass   25grass   25grass   25grass
25grass   25grass   28grass   26grass   28grass   29grass   26grass   28grass   27grass   25grass   4water    4water    4water    4water    32grass   40grass   49grass   57grass   48grass   41grass   32grass   25grass   25grass   25grass
25grass   25grass   25grass   25grass   25grass   28grass   25grass   25grass   25grass   41stone   35stone   35stone   35stone   35stone   35stone   35stone   35stone   35stone   41stone   32grass   25grass   25grass   25grass   25grass
25grass   25grass   25grass   25grass   25grass   25grass   25grass   25grass   25grass   35stone   25marble  25marble  25marble  25marble  25marble  25marble  25marble  25marble  35stone   33grass   25grass   25grass   25grass   25grass
25grass   25grass   25grass   25grass   25grass   25grass   25grass   25grass   25grass   35stone   25marble  25marble  25marble  25marble  25marble  25marble  25marble  25marble  35stone   25grass   25grass   25grass   25grass   25grass
25grass   25grass   25grass   25grass   25grass   25grass   25grass   25grass   25grass   35stone   25marble  25marble  25marble  25marble  25marble  25marble  25marble  25marble  25marble  25grass   25grass   25grass   25grass   25grass
'''
