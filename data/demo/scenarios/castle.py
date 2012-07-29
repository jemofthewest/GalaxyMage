VERSION = 1

MAP = 'castle'

ENDING_CONDITIONS = [Battle.PLAYER_DEFEATED,
                     Battle.DEFEAT_ALL_ENEMIES]

player = Faction(id=0,
                 units=[("fighter1", (9,6)),
                        ("rogue1", (10,8)),
                        ("healer1", (6,6)),
                        ("mage1", (11,7))])

opponent = Faction(id=1,
                   units=[("fighter1", (8,17)),
                          ("healer1", (5,16)),
                          ("mage1", (9,19)),
                          ("rogue1", (5,18)),
                          ("archer1",  (8,16))
                          ])
FACTIONS = [player, opponent]

# Start with an empty environment.
LIGHTING = Light.Environment()

# Add a very dim light at [20, 30, 200].
LIGHTING.addLight(Light.White(brightness=0.3,
                              position=[20, 30, 200]))

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

