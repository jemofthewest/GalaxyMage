VERSION = 1

MAP = 'hill-ravine'

ENDING_CONDITIONS = [Battle.PLAYER_DEFEATED,
                     Battle.DEFEAT_ALL_ENEMIES]

player = Faction(id=0,
                 units=[("fighter1", (4,14)),
                        ("fighter1", (5,17)),
                        ("archer1", (3,17)),
                        ("healer1", (1,14)),
                        ("mage1", (1,16)),
                        ])

opponent = Faction(id=1,
                   units=[("archer1", (15,3)),
                          ("archer1",  (10,2)),
                          ("archer1",  (15,14)),
                          ("archer1",  (17,7)),
                          ("archer1",  (15,4)),
                          ("archer1",  (17,8))])

FACTIONS = [player, opponent]

LIGHTING = Light.Environment()
LIGHTING.addLight(Light.White(brightness=0.5,
                              position=[20, 15, 100]))
LIGHTING.setFog(color=[0.4,0.4,0.5],
                start=10.0,
                end=30.0)

MUSIC = 'barbieri-lyta'

