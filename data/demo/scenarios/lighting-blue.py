# Castle with "evening" lighting
VERSION = 1

MAP = 'castle'

# We create an empty lighting environment then add a light with a
# bluish tinge.
LIGHTING = Light.Environment()
LIGHTING.addLight(Light.Point(diffuse=[0.0, 0.0, 0.8],
                              ambient=[0.3, 0.3, 0.8],
                              position=[20, 30, 100]))

# Now we add some fog to the air...
LIGHTING.setFog(color=[0.75,0.75,1.0],
                density=0.5,
                start=1.0,
                end=30.0)

            



