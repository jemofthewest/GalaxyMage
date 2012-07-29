# Castle with night lighting and a "fire" inside
VERSION = 1

MAP = 'castle'

# Start with an empty environment.
LIGHTING = Light.Environment()

# Add a very dim light at [20, 30, 100].
LIGHTING.addLight(Light.White(brightness=0.2,
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

