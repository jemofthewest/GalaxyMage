# Copyright (C) 2005 Colin McMillen <mcmillen@cs.cmu.edu>
#
# This file is part of GalaxyMage.
#
# GalaxyMage is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# GalaxyMage is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GalaxyMage; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import Constants
import random
from twisted.spread import pb

class Light(pb.Copyable, pb.RemoteCopy):
    def __init__(self,
                 position = [0, 0, 100, 1.0],
                 ambient = [0.0, 0.0, 0.0, 0.0],
                 diffuse = [0.0, 0.0, 0.0, 0.0],
                 specular = [0.0, 0.0, 0.0, 0.0],
                 attenuation = [1.0, 0.0, 0.0]):
        self._position = position
        self._position[1] = -self._position[1]
        self._position[2] = self._position[2] * Constants.Z_HEIGHT
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular
        self._attenuation = attenuation
        self._constantAttenuation = attenuation[0]
        self._linearAttenuation = attenuation[1]
        self._quadraticAttenuation = attenuation[2]
        if len(self._position) == 3:
            self._position.append(1.0)
        if len(self._ambient) == 3:
            self._ambient.append(1.0)
        if len(self._diffuse) == 3:
            self._diffuse.append(1.0)
        if len(self._specular) == 3:
            self._specular.append(1.0)

    def position(self):
        return self._position
    
    def ambient(self):
        return self._ambient

    def diffuse(self):
        return self._diffuse

    def specular(self):
        return self._specular

    def constantAttenuation(self):
        return self._constantAttenuation

    def linearAttenuation(self):
        return self._linearAttenuation

    def quadraticAttenuation(self):
        return self._quadraticAttenuation

class Foo(pb.Copyable, pb.RemoteCopy):
    def __init__(self, x):
        self.x = x

class White(Light):
    def __init__(self, brightness, position=[0,0,100,1.0]):
        Light.__init__(self,
                       position,
                       ambient=[brightness, brightness, brightness, 1.0],
                       diffuse=[brightness, brightness, brightness, 1.0])

class Point(Light):
    pass

class Environment(pb.Copyable, pb.RemoteCopy):
    def __init__(self):
        self._lights = []
        self._fogEnabled = False
        self._fogColor = [0.0, 0.0, 0.2]
        self._fogStart = 1.0
        self._fogEnd = 100.0
        self._fogDensity = 1.0
        self._ambientLight = (0.0, 0.0, 0.0, 1.0)
        self._skyColor = None
    
    def addLight(self, light):
        if len(self._lights) < 7:
            self._lights.append(light)

    def setFog(self,
               color=[1.0, 1.0, 1.0],
               density=1.0,
               start=1.0,
               end=100.0):
        self._skyColor = color
        self._fogEnabled = True
        self._fogColor = color
        self._fogDensity = density
        self._fogStart = start
        self._fogEnd = end

    def setAmbientLight(self, (r, g, b, a)):
        self._ambientLight = (r, g, b, a)
        
    def lights(self):
        return self._lights

    def ambientLight(self):
        return self._ambientLight

    def fogEnabled(self):
        return self._fogEnabled

    def fogColor(self):
        return self._fogColor

    def fogStart(self):
        return self._fogStart

    def fogEnd(self):
        return self._fogEnd

    def fogDensity(self):
        return self._fogDensity

    def skyColor(self):
        if self._skyColor != None:
            return self._skyColor
        else:
            return self._fogColor

    def setSkyColor(self, color):
        self._skyColor = color  

def defaultEnvironment(brightness = 0.7, position = [0, 0, 500, 1.0]):
    e = Environment()
    e.addLight(White(brightness, position))
    return e

def randomEnvironment(width=0.0, height=0.0):
    lighting = Environment()
    (r,g,b) = (random.uniform(0.2, 0.8),
               random.uniform(0.2, 0.8),
               random.uniform(0.2, 0.8))
    lightx = random.uniform(0, width)
    lighty = random.uniform(0, height)
    lighting.addLight(Point(diffuse=[r,g,b],
                            ambient=[r,g,b],
                            position=[lightx, lighty, 500]))
    fogstart = random.uniform(15.0, 25.0)
    fogend = random.uniform(fogstart+10.0, fogstart+20.0)
    lighting.setFog(color=((1.0+r)/2,(1.0+g)/2,(1.0+b)/2),
                    start=fogstart, end=fogend)
    return lighting
