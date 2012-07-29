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
import MapEditorGUI
import Util
import GLUtil
import Resources
import Sound
import Input
#import engine.Battle as Battle

from OpenGL.GL import *

# Added for GuiMapEditor
import MapEditorGUI as GUI
# End Added for GuiMapEditor

# FIXME: let the user undo a move if they've not yet acted
# FIXME: remove all the GUI.get() nonsense


class MapEditorCursor(Sprite.Sprite):
    DISABLED = 0
    FREE = 1
    SELECTED = 2
    UNIT_SELECTED = 3
    IN_DIALOG = 4
    SETTING_TAG = 5
    CREATING_TAG = 6
    
    def __init__(self, map):
        Sprite.Sprite.__init__(self)
        self.map = map
        self.x = map.width / 2
        self.y = map.height / 2
        while map.squares[self.x][self.y].z == 0:
            self.x += 1
        self._selectedUnit = None
        self.unitTarget = []
        self.alpha = 1.0
        self.state = MapEditorCursor.FREE

    def setPosn(self, x, y):
        self.x = x
        self.y = y

    def disable(self):
        self.state = MapEditorCursor.DISABLED

    def draw(self):
        glDisable(GL_LIGHTING)
        glPushMatrix()
        GLUtil.mapTrans(self.x, self.y, 0.0)
        glColor4f(0.0, 0.0, 0.75,
                  GUI.get().highlightAlpha())
        GLUtil.makeCubeTop(self.mapSquare().z,
                           self.mapSquare().cornerHeights)
        glPopMatrix()
        glEnable(GL_LIGHTING)

    def mapSquare(self):
        return self.map.squares[self.x][self.y]

    def posn3d(self):
        return (self.x, self.y, self.map.squares[self.x][self.y].z)

    def selectUnit(self, u, playerUnit=True):
        self.x = u.x()
        self.y = u.y()
        if playerUnit:
            self.state = MapEditorCursor.UNIT_SELECTED
        else:
            self.state = MapEditorCursor.DISABLED
        self._selectedUnit = u
        ScenarioGUI.get().battleMenu().setSelectedUnit(u)
    
    def selectSquare(self, x=None, y=None):
        if x != None and y != None:
            self.x = x
            self.y = y
        GUI.get().topMenu().setEnabled(True)
        GUI.get().topMenu().setShowing(True)
        self.state = MapEditorCursor.SELECTED
        #add stuff about units
            
    def unclick(self):
        if self.state == MapEditorCursor.DISABLED:
            return
        elif self.state == MapEditorCursor.FREE:
            Sound.cursorCancel()
#            if self.selectedSquare != None:
#                pass#for now
        elif self.state == MapEditorCursor.SELECTED:
            Sound.cursorCancel()
            self.state = MapEditorCursor.FREE
            self._selectedUnit = None
            GUI.get().topMenu().setSelectedOption(0)
            GUI.get().topMenu().setEnabled(False)
            GUI.get().topMenu().setShowing(False)
        elif (self.state == MapEditorCursor.IN_DIALOG):
            Sound.cursorCancel()
            GUI.get().topMenu().setEnabled(True)
            GUI.get().clearTopText() # from special menu
            GUI.get().clearHighlights()
        elif (self.state == MapEditorCursor.SETTING_TAG):
            Sound.cursorCancel()
            self.state = MapEditorCursor.SELECTED
            GUI.get().topMenu().setEnabled(True)
            GUI.get().tagMenu().setEnabled(False)
            GUI.get().tagMenu().setShowing(False)
            GUI.get().clearTopText() # from special menu
            GUI.get().clearHighlights()
        else:
            print 'Error: unhandled unclick() call in MapEditorCursor'
    
    def click(self):
        if self.state == MapEditorCursor.DISABLED:
            return
        elif self.state == MapEditorCursor.FREE:
            Sound.cursorClick()
            GUI.get().topMenu().setShowing(True)
            return 'topMenu'
        elif self.state == MapEditorCursor.SELECTED:
            Sound.cursorClick()
            choice = GUI.get().topMenu().getSelection()
            if choice == Sprite.TopMenu.SET_TAG:
                self.state = MapEditorCursor.SETTING_TAG
                GUI.get().tagMenu().setShowing(True)
            elif choice == Sprite.TopMenu.NEW_TAG:
                self.state = MapEditorCursor.CREATING_TAG
                GUI.get().topMenu().setEnabled(False)
                #GUI.get().addTagDialog().setEnabled(True)
                #GUI.get().addTagDialog().setShowing(True)
                GUI.get().addTagDialog().execute()
                GUI.get().topMenu().setShowing(False)
                self.state = MapEditorCursor.FREE
            #elif choice == Sprite.TopMenu.EDIT_TAG:
            #    self.state = MapEditorCursor.EDITING_TAG
            #    GUI.get().topMenu().setEnabled(False)
            #    GUI.get().editTagDialog().setEnabled(True)
            #    GUI.get().editTagDialog().setShowing(True)
            #elif choice == Sprite.TopMenu.SAVE:
            #    self.state = MapEditorCursor.SETTING_TAG
            #    GUI.get().topMenu().setEnabled(False)
            #    GUI.get().saveMapDialog().setEnabled(True)
            #    GUI.get().saveMapDialog().setShowing(True)
            else:
                print "ERROR: menu option %s not implemented yet" % choice
        elif self.state == MapEditorCursor.SETTING_TAG:
            tagNum = GUI.get().tagMenu().getSelection()
            tags = GUI.get().m.tags
            tagName = tags.keys()[tagNum]
            self.mapSquare().setTag(tags[tagName])
            GUI.get().updateMap()
            GUI.get().topMenu().setEnabled(False)
            GUI.get().topMenu().setShowing(False)
            GUI.get().tagMenu().setEnabled(False)
            GUI.get().tagMenu().setShowing(False)
            self.state = MapEditorCursor.FREE
            #GUI.get().clearTopText() # from special menu
            #GUI.get().clearHighlights()
        #    if ability == None:
        #        Sound.cursorInvalid()
        #        return
        #    self.selectedAbility = ability
        #    Sound.cursorClick()
        #    self.state = MapEditorCursor.CHOOSING_ABILITY_TARGET
        #    GUI.get().showAbilityRange(self.activeUnit,
        #                                       self.selectedAbility)
        #    GUI.get().battleMenu().setEnabled(False)             
        #    GUI.get().specialMenu().setEnabled(False)             
        #elif self.state == MapEditorCursor.CHOOSING_ABILITY_TARGET:
        #    Sound.cursorClick()
        #    a = self.selectedAbility
        #    if (self.x, self.y) not in a.range(self.map,
        #                                       self.activeUnit):
        #        Sound.cursorInvalid()
        #        return
        #    if not a.hasEffect(self.map, self.activeUnit, self.posn3d()):
        #        Sound.cursorInvalid()
        #        return
        #    self.state = MapEditorCursor.UNIT_SELECTED
        #    Battle.get().unitActed(a, self.posn3d())
        #    GUI.get().topMenu().setSelectedOption(0)
        #    GUI.get().topMenu().setEnabled(True)
        #    GUI.get().specialMenu().setEnabled(False)
        #    GUI.get().specialMenu().setShowing(False)
        #    GUI.get().clearHighlights()
        #    self.x = self.activeUnit.x()
        #    self.y = self.activeUnit.y()
        #elif self.state == MapEditorCursor.CHOOSING_MOVE_TARGET:
        #    if self.map.squares[self.x][self.y].unit != None:
        #        Sound.cursorInvalid()                
        #        return
        #    u = self._selectedUnit
        #    reachable = self.map.reachable(u)
        #    if (self.x, self.y) not in reachable:
        #        Sound.cursorInvalid()                
        #        return
        #    Sound.cursorClick()
        #    ScenarioGUI.get().moveUnit(u, (self.x, self.y))
        #    self.state = MapEditorCursor.UNIT_MOVING
        #elif self.state == MapEditorCursor.UNIT_MOVING:
        #    return
        else:
            print 'Error: unhandled click() call in MapEditorCursor'

    def update(self, timeElapsed):
#        if self.visible():
        self.alpha += 2.0 * timeElapsed
#        else:
#            self.alpha -= 2.0 * timeElapsed
        self.alpha = min(1.0, self.alpha)
        self.alpha = max(0.0, self.alpha)

    def canMove(self):
        return (self.state == MapEditorCursor.FREE)
    
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
        if self.canMove() and self.y > 0:
            self.y -= 1
            Sound.cursorMove()
            GUI.get().scrollTo((self.x, self.y))
            
    def moveDown(self):
        if self.canMove() and self.y < self.map.height - 1:
            self.y += 1
            Sound.cursorMove()
            GUI.get().scrollTo((self.x, self.y))

    def moveLeft(self):
        if self.canMove() and self.x > 0:
            self.x -= 1
            Sound.cursorMove()
            GUI.get().scrollTo((self.x, self.y))
            
    def moveRight(self):
        if self.canMove() and self.x < self.map.width - 1:
            self.x += 1
            Sound.cursorMove()
            GUI.get().scrollTo((self.x, self.y))

    # Unit stuff
    def hoveredUnit(self):
        if self.mapSquare().unit != None:
            return self.mapSquare().unit
        return self._selectedUnit    
            
    # Map editing stuff
    def plusTileHeight(self):
        self.map.squares[self.x][self.y].z += 1
        
    def minusTileHeight(self):
        self.map.squares[self.x][self.y].z -= 1

    def plusCenterHeight(self):
        self.map.squares[self.x][self.y].plusHeight()
        
    def minusCenterHeight(self):
        self.map.squares[self.x][self.y].minusHeight()

    def setHeight(self,height):
        self.map.squares[self.x][self.y].z = height
        
    def plusCornerHeight(self,corner):
        self.map.changeCorner(self.x, self.y, corner, 1)
        
    def minusCornerHeight(self,corner):
        self.map.changeCorner(self.x, self.y, corner, -1)

    def raiseWater(self):
        self.map.squares[self.x][self.y].waterHeight += 1
        
    def lowerWater(self):
        self.map.squares[self.x][self.y].waterHeight -= 1

    # Events stuff
    def handleEvent(self, event):
        if event.type == Input.CURSOR_UP:
            self.move(GUI.get().camera.cursorMovement(0, -1))
        elif event.type == Input.CURSOR_DOWN:
            self.move(GUI.get().camera.cursorMovement(0, 1))
        elif event.type == Input.CURSOR_LEFT:
            self.move(GUI.get().camera.cursorMovement(-1, 0))
        elif event.type == Input.CURSOR_RIGHT:
            self.move(GUI.get().camera.cursorMovement(1, 0))
        elif event.type == Input.CURSOR_ACCEPT:
            return self.click()
        elif event.type == Input.CURSOR_CANCEL:
            return self.unclick()
        elif event.type == Input.RAISE_CENTER:
            self.plusCenterHeight()
            GUI.get().updateMap()
        elif event.type == Input.LOWER_CENTER:
            self.minusCenterHeight()
            GUI.get().updateMap()
        elif event.type == Input.RAISE_TILE:
            self.plusTileHeight()
            GUI.get().updateMap()
        elif event.type == Input.LOWER_TILE:
            self.minusTileHeight()
            GUI.get().updateMap()
        elif (event.type >= Input.RAISE_B_BL_CORNER and
              event.type <= Input.RAISE_F_FR_CORNER):
            self.plusCornerHeight(
                GUI.get().camera.getCorner(event.type - Input.RAISE_B_BL_CORNER))
            GUI.get().updateMap()
        elif (event.type >= Input.LOWER_B_BL_CORNER and
              event.type <= Input.LOWER_F_FR_CORNER):
            self.minusCornerHeight(
                GUI.get().camera.getCorner(event.type - Input.LOWER_B_BL_CORNER))
            GUI.get().updateMap()
        elif event.type == Input.RAISE_WATER:
            self.raiseWater()
            GUI.get().updateMap()
        elif event.type == Input.LOWER_WATER:
            self.lowerWater()
            GUI.get().updateMap()
