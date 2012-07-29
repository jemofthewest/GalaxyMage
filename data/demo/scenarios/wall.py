VERSION = 1

MAP = 'wall'

ENDING_CONDITIONS = [Battle.PLAYER_DEFEATED,
                     Battle.DEFEAT_ALL_ENEMIES]

player = Faction(id=0,
                 units=[("fighter1", (15,15)),
                        ("defender1", (17,14)),
                        ("mage1", (18,18)),
                        ("healer1", (18,19)),
                        ("rogue1", (17,17)),
                        ("archer1", (18,10))])

opponent = Faction(id=1,
                   units=[("mage1", (9,3)),
                          ("healer1", (10,2)),
                          ("fighter1", (10,4)),
                          ("fighter1", (9,6)),
                          ("defender1", (10,6)),
                          ("archer1", (6,5)),
                          ("rogue1", (10,11)),
                          ("archer1", (13,5))])

FACTIONS = [player, opponent]

LIGHTING = Light.Environment()
LIGHTING.addLight(Light.White(brightness=0.7,
                              position=[20, 15, 100]))
LIGHTING.setFog(color=[0.5,0.5,1.0],
                start=15.0,
                end=25.0)

MUSIC = 'barbieri-army-march'
