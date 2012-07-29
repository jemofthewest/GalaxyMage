
VERSION = 1

WIDTH = 20
HEIGHT = 20

TILE_PROPERTIES = {
    'grass':  { 'color': (0.5, 0.7, 0.5),
                'colorVar': (0.2, 0.2, 0.2),
                'texture': 'grass' },
    'rock':   { 'color': (0.7, 0.5, 0.3),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'stone' },
    'water':  { 'color': (0.4, 0.4, 0.7),
                'colorVar': (0.05, 0.05, 0.05),
                'texture': 'none'
              }
    }
    
LAYOUT = '''
14rock    19rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   
4water    4water    19rock    24rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   33grass   29grass   29grass   29grass   29grass   29grass   
19rock    4water    19rock    19rock    19rock    24rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   33grass   37grass   33grass   29grass   29grass   29grass   29grass   
19rock    4water    4water    4water    4water    19rock    19rock    24rock    29grass   29grass   29grass   29grass   33grass   37grass   41grass   37grass   33grass   29grass   29grass   29grass   
24rock    19rock    19rock    19rock    4water    4water    4water    19rock    24rock    29grass   29grass   33grass   37grass   41grass   45grass   41grass   37grass   33grass   33grass   33grass   
29grass   24rock    24rock    24rock    19rock    19rock    4water    4water    19rock    24rock    29rock    34rock    39rock    44rock    49grass   45grass   41grass   37grass   37grass   37grass   
29grass   29grass   29grass   29grass   24rock    24rock    19rock    4water    4water    19rock    24rock    29rock    34rock    39rock    44rock    49grass   45grass   41grass   41grass   41grass   
29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    4water    9water    14water   19water   24water   39rock    44rock    49rock    49grass   45grass   45grass   45grass   
29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29rock    24water   39rock    44rock    49rock    53grass   49grass   49grass   49grass   
29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29rock    24water   29water   34water   39water   53grass   53grass   53grass   53grass   
29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   33grass   37grass   41grass   45grass   49grass   49grass   49grass   49grass   
29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    14rock    19rock    24rock    29grass   33grass   37grass   41grass   45grass   45grass   45grass   45grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   29grass   33grass   37grass   41grass   41grass   41grass   41grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   29grass   29grass   33grass   37grass   37grass   37grass   37grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   29grass   29grass   29grass   33grass   33grass   33grass   33grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    14rock    19rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   29grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   29grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   29grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   29grass   
29grass   29grass   29grass   29grass   29grass   29grass   29grass   29grass   24rock    19rock    14rock    19rock    24rock    29grass   29grass   29grass   29grass   29grass   29grass   29grass   
'''