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

import Geometry
import math
import Constants
import Clock

class Camera(object):

    def __init__(self):
        self._pitch = -60.0 # 0.0 is looking straight down at the map
        self.current = Constants.NW # logical camera direction, ~setRotation/45
        self._setRotation = Constants.NW*45.0 # requested camera rotation
        self._mapRotation = self._setRotation # current camera rotation
        self._height = 15.0
        self.needToRotate = True
        self._changed = True
        self._scrollTarget = None
        self._offset = Geometry.Point3D(0.0, 0.0, 0.0)
        
    def reset(self):
        self._pitch = -60.0 # 0.0 is looking straight down at the map
        self.current = Constants.NW # logical camera direction, ~setRotation/45
        self._setRotation = Constants.NW*45.0 # requested camera rotation
        self._mapRotation = self._setRotation # current camera rotation
        self._height = 15.0
        self.needToRotate = True
        self._changed = True

    def changed(self):
        result = self._changed
        self._changed = False
        return result

    def get(self):
        return self.current

    def offset(self):
        return self._offset

    def height(self):
        return self._height

    def setHeight(self, z):
        z = max(z, 5.0)
        z = min(z, 50.0)
        self._height = z
        self._changed = True

    def setOffset(self, x, y, z):
        z = max(z, 0.0)
        z = min(z, 50.0)
        self._offset = Geometry.Point3D(x, y, z)
        self._changed = True

    def scrollTo(self, posn):
        if len(posn) == 2:
            (x, y) = posn
            z = self._offset.z
        else:
            (x, y, z) = posn
            z *= Constants.Z_HEIGHT
        self._scrollTarget = (-x, y, z)

    def pitch(self):
        return self._pitch

    def setPitch(self, pitch):
        pitch = min(0.0, pitch)
        pitch = max(-90.0, pitch)
        self._pitch = pitch
        self._changed = True

    def change(self, amount):
        if self.needToRotate:
            return
        if amount != 0:
            self.current = self.current + amount
            while self.current < 0:
                self.current += 8
            while self.current > 7:
                self.current -= 8
            self._setRotation = self.current * 45.0
            self.needToRotate = True
            self._changed = True

    def rotate(self, degrees):
        self.setRotation(self._mapRotation + degrees)

    def setRotation(self, degrees):
        self._mapRotation = self._setRotation = degrees % 360.0
        self.current = int(degrees/45.0 + 0.5) % 8
        self.needToRotate = False
        self._changed = True
            
    def mapRotation(self):
        return self._mapRotation

    def set(self, new):
        self.current = new
        self._setRotation = new * 45.0
        self.needToRotate = True
        self._changed = True

    def adjustCamera(self, timeElapsed):
        self._adjustRotation(timeElapsed)
        self._adjustTranslation(timeElapsed)

    def _adjustTranslation(self, timeElapsed):
        if self._scrollTarget == None:
            return
        (x, y, z) = self._scrollTarget
        if Clock.get().getFPS() <= 10:
            self.setOffset(x, y, z)
            self._scrollTarget = None
            return
        (offsetX, offsetY, offsetZ) = self._offset.asTuple()
        dx = x - offsetX
        dy = y - offsetY
        dz = 0
        if z != None:
            dz = z - offsetZ
        speed = 5.0
        offsetX += dx * timeElapsed * speed
        offsetY += dy * timeElapsed * speed
        offsetZ += dz * timeElapsed * speed
        cutoff = 0.2
        if abs(dx) < cutoff and abs(dy) < cutoff and abs(dz) < cutoff:
            self._scrollTarget = None
        else:
            self.setOffset(offsetX, offsetY, offsetZ)

    def scrolling(self):
        return self._scrollTarget != None

    def _adjustRotation(self, timeElapsed):
        if not self.needToRotate:
            return
        rotateAmount = self._setRotation - self._mapRotation
        if rotateAmount < -180.0:
            rotateAmount += 360.0
        elif rotateAmount > 180.0:
            rotateAmount -= 360.0
        speed = 270 # degrees/second
        distToRotate = timeElapsed * speed
        if rotateAmount < 0.0:
            distToRotate *= -1.0
        if abs(rotateAmount) < abs(distToRotate):
            distToRotate = rotateAmount
            self.needToRotate = False
        self._mapRotation += distToRotate       
        self._mapRotation = self._mapRotation % 360.0
        self._changed = True

    def sortSprites(self, l):

        def cmpSpritesN(s1, s2):
            t1 = s1.y
            t2 = s2.y
            return cmp(t1, t2)

        def cmpSpritesNE(s1, s2):
            t1 = -s1.x + s1.y
            t2 = -s2.x + s2.y
            return cmp(t1, t2)

        def cmpSpritesE(s1, s2):
            t1 = -s1.x
            t2 = -s2.x
            return cmp(t1, t2)

        def cmpSpritesSE(s1, s2):
            t1 = -s1.x - s1.y
            t2 = -s2.x - s2.y
            return cmp(t1, t2)

        def cmpSpritesS(s1, s2):
            t1 = -s1.y
            t2 = -s2.y
            return cmp(t1, t2)

        def cmpSpritesSW(s1, s2):
            t1 = s1.x - s1.y
            t2 = s2.x - s2.y
            return cmp(t1, t2)

        def cmpSpritesW(s1, s2):
            t1 = s1.x
            t2 = s2.x
            return cmp(t1, t2)
            
        def cmpSpritesNW(s1, s2):
            t1 = s1.x + s1.y
            t2 = s2.x + s2.y
            return cmp(t1, t2)

        if self.current == Constants.N:
            l.sort(cmpSpritesN)
        elif self.current == Constants.NE:
            l.sort(cmpSpritesNE)
        elif self.current == Constants.E:
            l.sort(cmpSpritesE)
        elif self.current == Constants.SE:
            l.sort(cmpSpritesSE)
        elif self.current == Constants.S:
            l.sort(cmpSpritesS)
        elif self.current == Constants.SW:
            l.sort(cmpSpritesSW)
        elif self.current == Constants.W:
            l.sort(cmpSpritesW)
        elif self.current == Constants.NW:
            l.sort(cmpSpritesNW)

    def cursorMovement(self, x, y):
        if self.current == Constants.N or self.current == Constants.NW:
            return (x, y)
        elif self.current == Constants.E or self.current == Constants.NE:
            return (-y, x)
        elif self.current == Constants.S or self.current == Constants.SE:
            return (-x, -y)
        else:
            return (y, -x)   

    def getCorner(self, corner):
        if self.current == Constants.N or self.current == Constants.NW:
            return corner
        elif self.current == Constants.E or self.current == Constants.NE:
            if corner == 0: return 1
            if corner == 1: return 3
            if corner == 3: return 2
            if corner == 2: return 0
        elif self.current == Constants.S or self.current == Constants.SE:
            if corner == 0: return 3
            if corner == 1: return 2
            if corner == 3: return 0
            if corner == 2: return 1
        else:
            if corner == 0: return 2
            if corner == 1: return 0
            if corner == 3: return 1
            if corner == 2: return 3

    def mouseMovement(self, x, y):
        return Geometry.rotate2d((x, y), math.radians(self._mapRotation))
        if self.current == Constants.N:
            return (x, y)
        elif self.current == Constants.NW:
            return Geometry.rotate2d((x, y), math.radians(-45))
        elif self.current == Constants.E:
            return (-y, x)
        elif self.current == Constants.NE:
            return Geometry.rotate2d((-y, x), math.radians(-45))
        elif self.current == Constants.S:
            return (-x, -y)
        elif self.current == Constants.SE:
            return Geometry.rotate2d((-x, -y), math.radians(-45))
        elif self.current == Constants.W:
            return (y, -x)
        else:
            return Geometry.rotate2d((y, -x), math.radians(-45))

