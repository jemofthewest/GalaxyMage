# Castle with "evening" lighting
VERSION = 1

MAP = 'castle'

# We create an empty lighting environment, then add a somewhat dim
# light at the position [20, 30, 100]. Notice how the light position
# highlights the front of the castle and shadows the back.
LIGHTING = Light.Environment()
LIGHTING.addLight(Light.White(brightness=0.5,
                              position=[20, 30, 100]))




