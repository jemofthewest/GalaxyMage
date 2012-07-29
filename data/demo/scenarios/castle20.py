VERSION = 1

MAP = 'castle'

ENDING_CONDITIONS = [Battle.PLAYER_DEFEATED,
                     Battle.DEFEAT_ALL_ENEMIES]

player = Faction(id=0,
                 units=[("fighter20", (9,6))])

opponent = Faction(id=1,
                   units=[("fighter1", (1,17)),
                          ("fighter1", (2,17)),
                          ("fighter1", (3,17)),
                          ("fighter1", (4,17)),
                          ("fighter1", (5,17)),
                          ("fighter1", (6,17)),
                          ("fighter1", (7,17))])

FACTIONS = [player, opponent]

# Start with an empty environment.
LIGHTING = Light.Environment()

# Add a very dim light at [20, 30, 100].
LIGHTING.addLight(Light.White(brightness=0.3,
                              position=[20, 30, 100]))

# Add the "fire" in the middle of the castle. The "diffuse" parameter
# is the color of the diffuse light: a reddish-yellow. The attenuation
# values are for constant, linear, and quadratic attenuation, which
# control how the diffuse component of the light attenuates (reduces
# in intensity) with distance. The default value of attenuation is
# [1.0, 0.0, 0.0]... try playing around with it a bit and see what the
# results are!
LIGHTING.addLight(Light.Point(position=[8, 7, 12],
                              diffuse=[0.5, 0.2, 0.0],
                              attenuation=[0.05, 0.05, 0.01]))

# Set some fog. This will make the map and units appear to fade away
# into the distance.
LIGHTING.setFog(color=[0.0,0.0,0.0],
                start=10.0,
                end=30.0)

MUSIC = 'barbieri-battle'

