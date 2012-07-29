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

import Sprite
import ScenarioGUI
import Util
import GLUtil
import Resources
import Constants

from OpenGL.GL import *

class Cursor(Sprite.Sprite):
    def __init__(self, map):
        Sprite.Sprite.__init__(self)
        self.map = map
        self.x = map.width / 2
        self.y = map.height / 2
        self.selectedUnit = None
        self.alpha = 1.0
        self.facingMode = False

    def setPosn(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        glDisable(GL_LIGHTING)
        glPushMatrix()
        GLUtil.mapTrans(self.x, self.y, 0.0)
        glColor4f(0.0, 0.0, 0.75,
                  ScenarioGUI.get().highlightAlpha())
        GLUtil.makeCubeTop(self.mapSquare().z,
                           self.mapSquare().cornerHeights)
        glPopMatrix()
        glEnable(GL_LIGHTING)

    def mapSquare(self):
        return self.map.squares[self.x][self.y]

    def posn(self):
        return (self.x, self.y)

    def posn3d(self):
        return (self.x, self.y, self.map.squares[self.x][self.y].z)

    def selectUnit(self, u, playerUnit=True):
        self.x = u.x()
        self.y = u.y()
        self.selectedUnit = u

    def hoveredUnit(self):
        u = self.map.squares[self.x][self.y].unit
        if u != None:
            return u
        return self.selectedUnit

    def setFacingMode(self, facingMode):
        self.facingMode = facingMode

    def move(self, (x,y)):
        while x > 0:
            self.moveRight()
            x -= 1
        while x < 0:
            self.moveLeft()
            x += 1
        while y > 0:
            self.moveDown()
            y -= 1
        while y < 0:
            self.moveUp()
            y += 1
        
    def moveUp(self):
        if self.facingMode:
            self.selectedUnit.setFacing(Constants.N)
            return
        if self.y > 0:
            self.y -= 1
            ScenarioGUI.get().scrollTo((self.x, self.y))
            
    def moveDown(self):
        if self.facingMode:
            self.selectedUnit.setFacing(Constants.S)
            return
        if self.y < self.map.height - 1:
            self.y += 1
            ScenarioGUI.get().scrollTo((self.x, self.y))

    def moveLeft(self):
        if self.facingMode:
            self.selectedUnit.setFacing(Constants.W)
            return       
        if self.x > 0:
            self.x -= 1
            ScenarioGUI.get().scrollTo((self.x, self.y))
            
    def moveRight(self):
        if self.facingMode:
            self.selectedUnit.setFacing(Constants.E)
            return       
        if self.x < self.map.width - 1:
            self.x += 1
            ScenarioGUI.get().scrollTo((self.x, self.y))
