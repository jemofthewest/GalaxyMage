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

import time
import random
import math
import pygame

from OpenGL.GL import *
from OpenGL.GLU import *

import Resources
import Clock
import Camera
import Sprite
import MapEditorSprite
import MapEditorCursor as MapEditorCursor
import GLUtil
import MainWindow
import Util
import Sound
import engine.Light as Light
import gui.Input as Input

is_map_editor = True

def get():
    return _gui

_gui = None

class MapEditorGUI(MainWindow.MainWindowDelegate):
    def __init__(self, m):
        global _gui
        _gui = self
        
        self.lightEnv = Light.Environment()
        self.lightEnv.addLight(Light.White(brightness=0.5,
                               position=[20, 15, 100]))
        self.lightEnv.setFog(color=[0.4,0.4,0.5],
                start=10.0,
                end=30.0)
        self.setLighting()

        self.m = m
        
        for j in xrange(0, m.height):
            for i in xrange(0, m.width):
                self.compileMapSquareList(m.squares[i][j])

        self._highlightAlpha = 1.0  
        self.camera = Camera.Camera()

        tdbWidth = 250
        tdbHeight = 8
        tdbY = MainWindow.get().size()[1] - tdbHeight * 20 - 30
        center = (MainWindow.get().size()[0]/2,MainWindow.get().size()[1]/2)
        
        self.cursor = MapEditorCursor.MapEditorCursor(m)
        self._topMenu = MapEditorSprite.TopMenu((290, tdbY))
        self._tagMenu = MapEditorSprite.TagMenu((500, tdbY))
        self._tagMenu.setOptions(self.m.tags.keys())
        self._tagMenu.setShowing(False)
        self._chooseTagMenu = MapEditorSprite.TagMenu2((500, tdbY))
        self._chooseTagMenu.setOptions(self.m.tags.keys())
        self._chooseTagMenu.setShowing(False)
        self._addTagDialog = MapEditorSprite.AddTagDialog((50, 50),
            MainWindow.get().size()[0] - 130)
        self._editTagDialog = MapEditorSprite.EditTagDialog((50, 50),
            MainWindow.get().size()[0] - 130)
        self._saveDialog = MapEditorSprite.SaveDialog((50, 50),
            MainWindow.get().size()[0] - 130)
        self._tileInfoDisplayer = MapEditorSprite.TileInfoDisplayer((50, 50),
            MainWindow.get().size()[0] - 130)
        
        self.delegates = {}
        self.delegates['cursor'] = self.cursor
        self.delegates['topMenu'] = self._topMenu
        self.delegates['setTag'] = self._tagMenu
        self.delegates['addTag'] = self._addTagDialog
        self.delegates['editTag'] = self._editTagDialog
        self.delegates['chooseTag'] = self._chooseTagMenu
        self.delegates['save'] = self._saveDialog
        self.delegates['tileInfo'] = self._tileInfoDisplayer        
        self.activeDelegate = self.delegates['cursor']
        
        self.cursorPosnDisplayer = Sprite.CursorPosnDisplayer(self.cursor)
        self.tileTextureDisplayer = MapEditorSprite.TileTextureDisplayer(self.cursor)
        self.tileColorDisplayer = MapEditorSprite.TileColorDisplayer(self.cursor)
        self.tileTagDisplayer = MapEditorSprite.TileTagDisplayer(self.cursor)
        self.firstHeightDisplayer = MapEditorSprite.FirstHeightDisplayer(self.cursor,self.camera)
        self.secondHeightDisplayer = MapEditorSprite.SecondHeightDisplayer(self.cursor,self.camera)
        self.thirdHeightDisplayer = MapEditorSprite.ThirdHeightDisplayer(self.cursor,self.camera)
        self.textDisplayerBox = Sprite.TextDisplayerBox([
            self.tileTagDisplayer,
            self.tileTextureDisplayer,
            self.tileColorDisplayer,
            self.firstHeightDisplayer,
            self.secondHeightDisplayer,
            self.thirdHeightDisplayer
            ], (10, tdbY) , tdbWidth)
#        self._specialMenu = Sprite.SpecialMenu((420, tdbY))

        self._centeredTextDisplayer = Sprite.TextDisplayer()
        self._centeredTextDisplayer.setCenterX(True)
        self._centeredTextDisplayer.setCenterY(True)
        self._centeredTextDisplayer.setFont(Resources.font(size=36, bold=True))
        self._centeredTextDisplayer.setPosn(center)
        self._centeredTextDisplayer.setBorder(True)
        self._centeredTextDisplayer.setEnabled(False)

        self._topTextDisplayer = Sprite.TextDisplayer()
        self._topTextDisplayer.setCenterX(True)
        self._topTextDisplayer.setCenterY(False)
        self._topTextDisplayer.setFont(Resources.font(size=16, bold=True))
        self._topTextDisplayer.setPosn((MainWindow.get().size()[0]/2, 10))
        self._topTextDisplayer.setBorder(True)
        self._topTextDisplayer.setEnabled(False)

        
        self.highlights = {}
        self.cursorHighlightAlpha = 0.0
        self.highlightEnabled = False
        self._activeSquare = None

        self.normalObjects = [self.cursor]
        self.fgObjects = [self.cursorPosnDisplayer,
                          self.textDisplayerBox,
                          self._addTagDialog,
                          self._saveDialog,
                          self._tileInfoDisplayer,
                          self._editTagDialog,
                          self._topMenu,
                          self._tagMenu,
                          self._chooseTagMenu,
#                          self._specialMenu,
                          self._centeredTextDisplayer,
                          self._topTextDisplayer]
        self.gameObjects = []
        self.gameObjects.extend(self.normalObjects)
        self.gameObjects.extend(self.fgObjects)

#        Sound.playMusic(scenario.music())

#        (clearr, clearg, clearb) = self.lightEnv.skyColor()
#        glClearColor(clearr, clearg, clearb, 0.0)
        glClearColor(0.8, 0.8, 0.85, 0.0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)       

        self.scrollTo((self.m.width/2.0, self.m.height/2.0))

    def __del__(self):
        m = self.m
        for j in xrange(0, m.height):
            for i in xrange(0, m.width):
                sq = m.squares[i][j]
                if sq.guiData.has_key("listID"):
                    try:
                        glDeleteLists(sq.guiData['listID'], 1)
                    except:
                        pass
                if sq.guiData.has_key("topListID"):
                    try:
                        glDeleteLists(sq.guiData['topListID'], 1)
                    except:
                        pass

    def setCenteredText(self, text):
        self._centeredTextDisplayer.setEnabled(True)
        self._centeredTextDisplayer.setText(text)

    def clearCenteredText(self):
        self._centeredTextDisplayer.setEnabled(False)

    def setTopText(self, text):
        self._topTextDisplayer.setEnabled(True)
        self._topTextDisplayer.setText(text)

    def clearTopText(self):
        self._topTextDisplayer.setEnabled(False)

#    def selectUnit(self, unit, playerControlled):
#        self.cursor.selectUnit(unit, playerControlled)

#    def setActiveUnit(self, activeUnit):
#        self._activeUnit = activeUnit
#        self._battleMenu.setEnabled(True)
#        self._specialMenu.setShowing(False)
#        self._specialMenu.setEnabled(False)
#        self._specialMenu.setSelectedUnit(activeUnit)
#        self.cursor.setActiveUnit(self._activeUnit)

    def topMenu(self):
        return self._topMenu

    def tagMenu(self):
        return self._tagMenu

    def chooseTagMenu(self):
        return self._chooseTagMenu

    def editTagDialog(self):
        return self._editTagDialog

    def addTagDialog(self):
        return self._addTagDialog
    
    def saveDialog(self):
        return self._saveDialog

    def tileInfoDisplayer(self):
        return self._tileInfoDisplayer        

#    def specialMenu(self):
#        return self._specialMenu

    def highlightAlpha(self):
        return self._highlightAlpha

    def scrollTo(self, (x, y)):
        self.camera.scrollTo((x, y, self.m.squares[int(x)][int(y)].z))

    def scrolling(self):
        return self.camera.scrolling()

    def saveMap(self, filename):
        self.m.save(filename)
    
    def compileMapSquareList(self, sq):
        if sq.guiData.has_key("listID"):
            glDeleteLists(sq.guiData["listID"], 1)

        textureNames = sq.texture()
        texIDt = Resources.texture(textureNames[0])
        sq.guiData['textureID'] = texIDt #fix me: update with the new amount of textures.
        
        texIDl = Resources.texture(textureNames[1])
        texIDb = Resources.texture(textureNames[2])
        texIDr = Resources.texture(textureNames[3])
        texIDf = Resources.texture(textureNames[4])
        
        textureIDs = [texIDt, texIDl, texIDb, texIDr, texIDf]
        
        listID = glGenLists(1)
        sq.guiData["listID"] = listID
        glNewList(listID, GL_COMPILE)

        GLUtil.makeCube(sq.z, sq.cornerHeights,
                        textureIDs, sq.cornerColors, sq.waterHeight,
                        sq.waterColor, sq.minHeight())
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        #glLineWidth(0.75)
        #GLUtil.makeCube(sq.z, (0.0,0.0,0.0,1.0), sq.cornerHeights, False)
        #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEndList()

        topListID = glGenLists(1)
        sq.guiData['topListID'] = topListID
        glNewList(topListID, GL_COMPILE)
        GLUtil.makeCubeTop(sq.z, sq.cornerHeights)
        glEndList()

    def setLighting(self):
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.lightEnv.ambientLight())
        lightIndex = GL_LIGHT0
        for l in self.lightEnv.lights():
            if lightIndex > GL_LIGHT7:
                break
            glEnable(lightIndex)
            glLightfv(lightIndex, GL_AMBIENT, l.ambient())
            glLightfv(lightIndex, GL_DIFFUSE, l.diffuse())
            glLightfv(lightIndex, GL_SPECULAR, l.specular())
            glLightf(lightIndex, GL_CONSTANT_ATTENUATION,
                     l.constantAttenuation())
            glLightf(lightIndex, GL_LINEAR_ATTENUATION,
                     l.linearAttenuation())
            glLightf(lightIndex, GL_QUADRATIC_ATTENUATION,
                     l.quadraticAttenuation())
            lightIndex += 1

        if self.lightEnv.fogEnabled():
            glFogi(GL_FOG_MODE, GL_LINEAR)
            glHint(GL_FOG_HINT, GL_FASTEST)
            glFogfv(GL_FOG_COLOR, self.lightEnv.fogColor())
            glFogf(GL_FOG_DENSITY, self.lightEnv.fogDensity())	
            glFogf(GL_FOG_START, self.lightEnv.fogStart())
            glFogf(GL_FOG_END, self.lightEnv.fogEnd())
            glEnable(GL_FOG)
        else:
            glDisable(GL_FOG)

    def resize(self, (width, height)):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.2, 100.0)
        glMatrixMode(GL_MODELVIEW)

        tdbWidth = 250
        tdbHeight = 8
        tdbY = MainWindow.get().size()[1] - tdbHeight * 20 - 30
        self._topTextDisplayer.setPosn((width/2, 10))
        self._topTextDisplayer.invalidate()
        self._centeredTextDisplayer.setPosn((width/2, height/2))
        self._centeredTextDisplayer.invalidate()
        self.textDisplayerBox.setPosn((10, tdbY))
        self.textDisplayerBox.invalidate()
        self._topMenu.setPosn((290, tdbY))
        self._topMenu.invalidate()
#        self._specialMenu.setPosn((420, tdbY))
#        self._specialMenu.invalidate()
        self.cursorPosnDisplayer.invalidate()

    def setCursorPosn(self, x, y):
        self.cursor.setPosn(x, y)

    def setTopMenuShowing(self, showing):
        self._topMenu.setShowing(showing)

    # highlights should be a dict mapping (x,y) pairs to colors
    def setHighlights(self, highlights, resetAlpha=True):
        self.highlightEnabled = True
        if resetAlpha:
            self.cursorHighlightAlpha = 0.0
        self.highlights = highlights

    def clearHighlights(self):
        self.highlightEnabled = False
        
    def setUpCamera(self):
        m = self.m
       
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)      
        glLoadIdentity()

        glTranslate(0.0, 0.0, -self.camera.height())
        glRotatef(self.camera.pitch(), 1.0, 0.0, 0.0)
        glRotatef(self.camera.mapRotation(), 0.0, 0.0, 1.0)
        glTranslate(self.camera.offset().x,
                    self.camera.offset().y,
                    -self.camera.offset().z)
        
        #glTranslate(self.camera.centerPosn.
        #glTranslate(-0.5*(m.width-1), 0.5*(m.height-1), 0.0)
        

#        lightIndex = GL_LIGHT0
#        for l in self.lightEnv.lights():
#            if lightIndex > GL_LIGHT7:
#                break
#            glLightfv(lightIndex, GL_POSITION, l.position())
#            lightIndex += 1

#         glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 90.0)
#         glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0)
#         glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, 0.4, -1.0, 1.0])
#        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 0.0, 0.0, 1.0])
#        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)
            

        # modify the highlights by an alpha value dependent on time
        # set to the range (0.0, 1.0)
        self._highlightAlpha = (math.sin(Clock.get().getTime() * 2.0) +
                                1.0) / 2.0
        # now scale to the range (0.5, 0.8)
        self._highlightAlpha = self._highlightAlpha * 0.3 + 0.5

    def drawBG(self):
        m = self.m
        glBindTexture(GL_TEXTURE_2D, 0)
        glPushMatrix()
        for j in xrange(0, m.height):
            for i in xrange(0, m.width):
                z = m.squares[i][j].z
                if z != 0:
                    glCallList(m.squares[i][j].guiData["listID"])
#                     GLUtil.makeCube(m.squares[i][j].z,
#                                     m.squares[i][j].guiData["color"],
#                                     m.squares[i][j].cornerHeights)
#                     glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
#                     GLUtil.makeCube(m.squares[i][j].z,
#                                     (0.0,0.0,0.0,1.0),
#                                     m.squares[i][j].cornerHeights,
#                                     False)
#                     glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                if (i,j) in self.highlights.keys():
                    (r,g,b,a) = self.highlights[(i,j)]
                    a = (a * self.highlightAlpha()
                         * self.cursorHighlightAlpha)
                    glColor4f(r, g, b, a)
                    glPolygonOffset(-1.0, -1.0)
                    glCallList(m.squares[i][j].guiData['topListID'])
                    glPolygonOffset(0.0, 0.0)       
                glTranslatef(1.0, 0.0, 0.0)
            glTranslatef(-1.0*m.width, -1.0, 0.0)

        glPopMatrix()

    def update(self, timeElapsed):
        if self.highlightEnabled:
            self.cursorHighlightAlpha += 2.0 * timeElapsed
        else:
            self.cursorHighlightAlpha -= 2.0 * timeElapsed
        self.cursorHighlightAlpha = min(1.0, self.cursorHighlightAlpha)
        if self.cursorHighlightAlpha < 0:
            self.cursorHighlightAlpha = 0
            self.highlights = {}

        # Move view smoothly if needed
        self.camera.adjustCamera(timeElapsed)

        # Figure out the active character, if any
#        if self._activeSquare == None:
#            self.topMenu().setEnabled(False)

        # Update game objects
        for obj in self.gameObjects:
            obj.update(timeElapsed)

        # Setup camera, draw background
        glPolygonOffset(0.0, 0.0)
        self.setUpCamera()
        self.drawBG()              

        # Draw the objects that have to be behind the unit sprites
        glPolygonOffset(-3.0, -3.0)
        for obj in self.normalObjects:
            obj.draw()
           
        # Draw units
        glPolygonOffset(-10.0, -10.0)
#        self.camera.sortSprites(self.unitDisplayers)
#        for u in self.unitDisplayers:
#            u.draw()

        # Draw the objects that have to be in front of the unit
        # sprites
        glPolygonOffset(1.0, 1.0)
        for obj in self.fgObjects:
            obj.draw()          

#        # Update unit slide
#        self._updateUnitSlide(timeElapsed)

#    def unitDisplayer(self, unit):
#        return self.unitDisplayersDict[unit]

    def updateMap(self):
        self._tagMenu.setOptions(self.m.tags.keys())
        for j in xrange(0, self.m.height):
            for i in xrange(0, self.m.width):
                self.m.squares[i][j].setTag()#keeps same tag, but rerandomizes color
        self.m.smoothColors()
        for j in xrange(0, self.m.height):
            for i in xrange(0, self.m.width):
                self.compileMapSquareList(self.m.squares[i][j])
                
    def handleEvent(self, event):
        newActive = self.activeDelegate.handleEvent(event)
        if self.delegates.has_key(newActive):
            self.activeDelegate = self.delegates[newActive]
        if (self.activeDelegate != self.delegates['addTag'] and
            self.activeDelegate != self.delegates['save']):
            if event.type == pygame.MOUSEBUTTONDOWN:
                (offsetX, offsetY, offsetZ) = self.camera.offset().asTuple()
                h = self.camera.height()
                if event.button == 4:   # scrolled up
                    h -= 1.0
                elif event.button == 5: # scrolled down
                    h += 1.0
                elif event.button == 6: # scrolled left
                    self.camera.change(-1)
                elif event.button == 7: # scrolled right
                    self.camera.change(1)
                self.camera.setHeight(h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.camera.reset()
                elif event.key == pygame.K_SCROLLOCK:
                    print self.m.loadString()
#                elif event.key == pygame.K_w:
#                    self.battle.playerGaveUp()
            elif event.type == Input.TRANSLATE_CAMERA:
                (x, y) = event.amount
                (x, y) = self.camera.mouseMovement(x, y)
                (offsetX, offsetY, offsetZ) = self.camera.offset().asTuple()
                offsetX += x * self.camera.height()
                offsetY -= y * self.camera.height()
                self.camera.setOffset(offsetX, offsetY, offsetZ)
            elif event.type == Input.ROTATE_CAMERA:
                self.camera.rotate(event.amount)
            elif event.type == Input.LOWER_CAMERA:
                h = self.camera.height()
                h -= 1.0
                self.camera.setHeight(h)
            elif event.type == Input.RAISE_CAMERA:
                h = self.camera.height()
                h += 1.0
                self.camera.setHeight(h)
            elif event.type == Input.ROTATE_CAMERA_CCW:
                self.camera.change(-1)
            elif event.type == Input.ROTATE_CAMERA_CW:
                self.camera.change(1)                   
            elif event.type == Input.PITCH_CAMERA:
                newPitch = self.camera.pitch() + event.amount
                self.camera.setPitch(newPitch)
