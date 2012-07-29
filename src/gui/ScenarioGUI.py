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
from twisted.python import util
from twisted.internet import reactor

import Constants
import Resources
import Clock
import Camera
import Sprite
import Cursor
import GLUtil
import gui.MainWindow as MainWindow
import Util
import Sound
import engine.Class as Class
import engine.Unit as Unit
import gui.Input as Input
import engine.Faction
import FSM

def get():
    return _gui

_gui = None

class ScenarioGUI(MainWindow.MainWindowDelegate):
    def __init__(self, client, scenario, faction):
        global _gui
        _gui = self

        self.scenario = scenario
        self.client = client
        self.faction = faction
        self.lightEnv = scenario.lightEnvironment()
        self.setLighting()
        self.focusedElement = None
        self.fsm = ScenarioGUIFSM(self)

        self.m = scenario.map()
        m = self.m
        for j in xrange(0, m.height):
            for i in xrange(0, m.width):
                self.compileMapSquareList(m.squares[i][j])

        self._highlightAlpha = 1.0  
        self.camera = Camera.Camera()
        self.lastCameraRotation = None
        self.sortedMapSquares = []

        # FIXME: make a single chatbox object
        textColor = (64, 0, 0)
        self.textEntry = Sprite.TextEntry()
        self.textEntry.setPosn((10, 160))
        self.textEntry.setColor(textColor) # FIXME: 0-255 color
        self.chatBox1 = Sprite.TextDisplayer()
        self.chatBox1.setPosn((10, 60))
        self.chatBox1.setColor(textColor) # FIXME: 0-255 color
        self.chatBox1.setText("")
        self.chatBox2 = Sprite.TextDisplayer()
        self.chatBox2.setPosn((10, 80))
        self.chatBox2.setColor(textColor) # FIXME: 0-255 color
        self.chatBox2.setText("")
        self.chatBox3 = Sprite.TextDisplayer()
        self.chatBox3.setPosn((10, 100))
        self.chatBox3.setColor(textColor) # FIXME: 0-255 color
        self.chatBox3.setText("")
        self.chatBox4 = Sprite.TextDisplayer()
        self.chatBox4.setPosn((10, 120))
        self.chatBox4.setColor(textColor) # FIXME: 0-255 color
        self.chatBox4.setText("")
        self.chatBox5 = Sprite.TextDisplayer()
        self.chatBox5.setPosn((10, 140))
        self.chatBox5.setColor(textColor) # FIXME: 0-255 color
        self.chatBox5.setText("")
        
        self.cursor = Cursor.Cursor(m)
        self.cursorPosnDisplayer = Sprite.CursorPosnDisplayer(self.cursor)
        self.unitNameDisplayer = Sprite.UnitNameDisplayer(self.cursor)
        self.unitMovementDisplayer = Sprite.UnitMovementDisplayer(self.cursor)
        self.unitHPDisplayer = Sprite.UnitHPDisplayer(self.cursor)
        self.unitSPDisplayer = Sprite.UnitSPDisplayer(self.cursor)
        self.unitPhysicalDisplayer = Sprite.UnitPhysicalDisplayer(self.cursor)
        self.unitMagicalDisplayer = Sprite.UnitMagicalDisplayer(self.cursor)
        self.unitClassDisplayer = Sprite.UnitClassDisplayer(self.cursor)
        self.unitSpeedDisplayer = Sprite.UnitSpeedDisplayer(self.cursor)
        tdbWidth = 250
        tdbHeight = 8
        tdbY = MainWindow.get().size()[1] - tdbHeight * 20 - 30
        self.textDisplayerBox = Sprite.TextDisplayerBox([
            self.unitNameDisplayer,
            self.unitClassDisplayer,
            self.unitHPDisplayer,
            self.unitSPDisplayer,
            self.unitMovementDisplayer,
            self.unitSpeedDisplayer,
            self.unitPhysicalDisplayer,
            self.unitMagicalDisplayer,
            ], (10, tdbY) , tdbWidth)
        self._battleMenu = Sprite.BattleMenu((290, tdbY))
        self._specialMenu = Sprite.SpecialMenu((420, tdbY))

        self._centeredTextDisplayer = Sprite.TextDisplayer()
        self._centeredTextDisplayer.setCenterX(True)
        self._centeredTextDisplayer.setCenterY(True)
        self._centeredTextDisplayer.setFont(Resources.font(size=36, bold=True))
        self._centeredTextDisplayer.setPosn((MainWindow.get().size()[0]/2,
                                             MainWindow.get().size()[1]/2))
        self._centeredTextDisplayer.setBorder(True)
        self._centeredTextDisplayer.setEnabled(False)

        self._topTextDisplayer = Sprite.TextDisplayer()
        self._topTextDisplayer.setCenterX(True)
        self._topTextDisplayer.setCenterY(False)
        self._topTextDisplayer.setFont(Resources.font(size=16, bold=True))
        self._topTextDisplayer.setPosn((MainWindow.get().size()[0]/2, 10))
        self._topTextDisplayer.setBorder(True)
        self._topTextDisplayer.setEnabled(False)
        self._topTextDisplayerClearer = None
        
        self.units = scenario.units()
        self.battle = scenario.battle()
        self.unitDisplayers = []
        self.unitDisplayersDict = {}
        for u in self.units:
            ud = Sprite.UnitDisplayer(u)
            self.unitDisplayers.append(ud)
            self.unitDisplayersDict[u] = ud
        self.highlights = {}
        self.cursorHighlightAlpha = 0.0
        self.highlightEnabled = False

        self.normalObjects = [self.cursor]
        self.fgObjects = [self.textEntry,
                          self.chatBox1,
                          self.chatBox2,
                          self.chatBox3,
                          self.chatBox4,
                          self.chatBox5,                          
                          self.cursorPosnDisplayer,
                          self.textDisplayerBox,
                          self._battleMenu,
                          self._specialMenu,
                          self._centeredTextDisplayer,
                          self._topTextDisplayer]
        self.gameObjects = []
        self.gameObjects.extend(self.normalObjects)
        self.gameObjects.extend(self.fgObjects)
        self.gameObjects.extend(self.unitDisplayers)

        # FIXME: rename/remove these
        self._unitMoving = None
        self.unitTarget = None
        self.originalUnitPosn = None
        self.lastUnitMove = None
        self.nextUnitMovePosn = None
        self.unitMoveZDiff = None

        Sound.playMusic(scenario.music())

        (clearr, clearg, clearb) = self.lightEnv.skyColor()
        glClearColor(clearr, clearg, clearb, 0.0)
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

    def moveUnit(self, x, y):
        u = self.unit
        self.setCursorPosn(x, y)
        cd = self.unitDisplayersDict[u]
        cd.resetSlide()

        # FIXME: variable names suck
        self._unitMoving = u
        self.m.reachable(u)
        self.unitTarget = self.m.shortestPath(x, y)
        self.originalUnitPosn = u.posn()
        self.lastUnitMove = 0.0
        self.nextUnitMovePosn = self.unitTarget.pop()
        self.unitMoveZDiff = self.nextUnitMovePosn.z - cd.z

    def activateUnit(self, unit):
        self.unit = unit
        self.scrollTo(unit.posn())
        self.cursor.selectUnit(unit)
        if unit.faction() == self.faction:
            self.fsm.trans('battleMenu', unit)
        else:
            self.fsm.trans('opponentTurn', unit)

    def moveActCancel(self, move, act, cancel):
        self._battleMenu.moveActCancel(move, act, cancel)

    def done(self):
        return self.nextUnitMovePosn == None

    def showMessage(self, text):
        self.chatBox1.setText(self.chatBox2.getText())
        self.chatBox2.setText(self.chatBox3.getText())
        self.chatBox3.setText(self.chatBox4.getText())
        self.chatBox4.setText(self.chatBox5.getText())
        self.chatBox5.setText(text)

    def showActionPerformed(self, abilityID):
        action = engine.Ability.Ability.get[abilityID]
        unit = self.unit
        self.setTopText(action.name())
        Sound.action(action.sound(unit.attack()))
        # FIXME: don't compare against the string name! Will break
        # when "Attack" is translated
        if action.name() == "Attack":
            ud = self.unitDisplayer(unit)
            attDisp = Sprite.AttackDisplayer(unit, 0.0)
            ud.addAnimation(attDisp)

    def showActionResults(self, targetID, results):
        delay = 0.0
        for r in results:
            self.showEffect(targetID, r, delay)
            delay += 0.5

    def showEffect(self, targetID, effect, delay):
        target = self.scenario.unitFromID(targetID)
        ud = self.unitDisplayer(target)
        if isinstance(effect, engine.Effect.MissResult):
            dd = Sprite.DamageDisplayer(_("Miss"), Sprite.NEUTRAL, delay)
            ud.addAnimation(dd)
        elif (isinstance(effect, engine.Effect.DamageResult) or
              isinstance(effect, engine.Effect.DamageSPResult)):
            dd = Sprite.DamageDisplayer(effect.damage, Sprite.NEGATIVE, delay)
            ud.addAnimation(dd)
        elif isinstance(effect, engine.Effect.HealResult):
            dd = Sprite.DamageDisplayer(effect.damage, Sprite.BENEFICIAL,
                                        delay)
            ud.addAnimation(dd)
        elif isinstance(effect, engine.Effect.StatusResult):
            effectName = engine.Effect.Status.effectNames[effect.type]
            effectType = Sprite.NEGATIVE
            if engine.Effect.Status.beneficial(effect):
                effectType = Sprite.BENEFICIAL
            dd = Sprite.DamageDisplayer(effectName, effectType, delay)
            ud.addAnimation(dd)

    def setCenteredText(self, text):
        self._centeredTextDisplayer.setEnabled(True)
        self._centeredTextDisplayer.setText(text)

    def clearCenteredText(self):
        self._centeredTextDisplayer.setEnabled(False)

    def setTopText(self, text):
        self._topTextDisplayer.setEnabled(True)
        self._topTextDisplayer.setText(text)
        if self._topTextDisplayerClearer:
            self._topTextDisplayerClearer.cancel()
        self._topTextDisplayerClearer = reactor.callLater(2,
                                                          self.clearTopText)
        
    def clearTopText(self):
        self._topTextDisplayer.setEnabled(False)
        self._topTextDisplayerClearer = None

    def showAbilityRange(self, unit, ability):
        highlights = {}
        for s in ability.range(self.m,
                               unit):
            highlights[s] = (1.0, 1.0, 0.0, 0.75)
        self.setHighlights(highlights, False)

    def showAbilityAOE(self, unit, ability, posn):
        highlights = self.highlights
        for s in ability.aoe(self.m,
                             unit,
                             posn):
            if highlights.has_key(s):
                if highlights[s] == (1.0, 1.0, 0.0, 0.75):
                    highlights[s] = (1.0, 0.0, 0.0, 0.75)
            else:
                highlights[s] = (1.0, 0.0, 0.0, 0.75)

    def showMovementRange(self, unit):
        reachable = self.m.reachable(unit)
        highlights = {}
        for r in reachable:
            highlights[r] = (0.0, 1.0, 1.0, 0.75)
        highlights[(unit.x(), unit.y())] = (0.0, 0.0, 1.0, 0.75)
        self.setHighlights(highlights)

    def battleMenu(self):
        return self._battleMenu

    def specialMenu(self):
        return self._specialMenu

    def highlightAlpha(self):
        return self._highlightAlpha

    def scrollTo(self, (x, y)):
        zx = int(x)
        zy = int(y)
        zx = max(0, zx)
        zy = max(0, zy)
        zx = min(zx, self.m.width-1)
        zy = min(zy, self.m.height-1)
        self.camera.scrollTo((x, y, self.m.squares[zx][zy].z))

    def scrolling(self):
        return self.camera.scrolling()

    def unitMoving(self):
        return self.nextUnitMovePosn != None

    def _updateUnitSlide(self, timeElapsed):
        if self.nextUnitMovePosn == None:
            return
        squareMoveTime = 0.2
        zSpeedup = 3.0 
        self.lastUnitMove += timeElapsed
        sq = self.nextUnitMovePosn
        u = self._unitMoving
        ud = self.unitDisplayersDict[u]

        dx = Util.sign(sq.x-ud.x) * timeElapsed * (1.0 / squareMoveTime)
        dy = Util.sign(sq.y-ud.y) * timeElapsed * (1.0 / squareMoveTime)
        if abs(dx) < 0.001:
            dx = 0
        if abs(dy) < 0.001:
            dy = 0

        dz = 0
        if self.unitMoveZDiff > 0:
            if self.lastUnitMove < squareMoveTime * zSpeedup:
                dz = (timeElapsed * (1.0 / squareMoveTime) *
                      zSpeedup * self.unitMoveZDiff)
                if sq.z - ud.z < dz:
                    dz = sq.z - ud.z
        elif self.unitMoveZDiff < 0:
            if (self.lastUnitMove >
                squareMoveTime * (zSpeedup - 1) / zSpeedup):
                dz = (timeElapsed * (1.0 / squareMoveTime) *
                      zSpeedup * self.unitMoveZDiff)
                if ud.z - sq.z < dz:
                    dz = sq.z - ud.z
        if abs(dz) < 0.01:
            dz = 0
           
        ud.slide(dx, dy, dz)
        self.scrollTo((ud.getX(), ud.getY()))
        if self.lastUnitMove > squareMoveTime:
            if len(self.unitTarget) == 0:
                ud.resetSlide()
                u.setPosn(sq.x, sq.y, sq.z)
                self.nextUnitMovePosn = None
                if u.faction() == self.faction:
                    self.fsm.trans('battleMenu', u)
                else:
                    self.fsm.trans('opponentTurn', u)
                reactor.callLater(1.0, self.client.remote, 'readyToDisplay')
                return
            ud.setPosn(sq.x, sq.y, sq.z)
            sq = self.unitTarget.pop()
            self.unitMoveZDiff = sq.z - ud.z
            self.lastUnitMove = 0.0
            self.nextUnitMovePosn = sq

    def compileMapSquareList(self, sq):
        if sq.guiData.has_key("listID"):
            glDeleteLists(sq.guiData["listID"], 1)

          
        textureNames = sq.texture()
        texIDt = Resources.texture(textureNames[0])
        sq.guiData['textureID'] = texIDt # FIXME: update with the new amount of textures.
        
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
        for light in xrange(GL_LIGHT0, GL_LIGHT7+1):
            glDisable(light)
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
        self._battleMenu.setPosn((290, tdbY))
        self._battleMenu.invalidate()
        self._specialMenu.setPosn((420, tdbY))
        self._specialMenu.invalidate()
        self.cursorPosnDisplayer.invalidate()

    def setCursorPosn(self, x, y):
        self.cursor.setPosn(x, y)

    def setBattleMenuShowing(self, showing):
        self._battleMenu.setShowing(showing)

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
        
        lightIndex = GL_LIGHT0
        for l in self.lightEnv.lights():
            if lightIndex > GL_LIGHT7:
                break
            glLightfv(lightIndex, GL_POSITION, l.position())
            lightIndex += 1

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
        cameraRotation = self.camera.get()
        if cameraRotation != self.lastCameraRotation:
            self.lastCameraRotation = cameraRotation
            squares = []
            for j in xrange(0, m.height):
                for i in xrange(0, m.width):
                    squares.append(m.squares[i][j])
            self.camera.sortSprites(squares)
            self.sortedMapSquares = squares
                
        glBindTexture(GL_TEXTURE_2D, 0)
        for s in self.sortedMapSquares:
            dx = s.x-self.cursor.x
            dy = s.y-self.cursor.y
            if dx*dx + dy*dy > self.lightEnv.fogEnd()*self.lightEnv.fogEnd():
                continue
            glPushMatrix()
            glTranslatef(1.0*s.x, -1.0*s.y, 0.0)
            if s.z != 0:
                glCallList(s.guiData["listID"])
            if (s.x,s.y) in self.highlights.keys():
                (r,g,b,a) = self.highlights[(s.x,s.y)]
                a = (a * self.highlightAlpha()
                     * self.cursorHighlightAlpha)
                glColor4f(r, g, b, a)
                glPolygonOffset(-1.0, -1.0)
                glCallList(s.guiData['topListID'])
                glPolygonOffset(0.0, 0.0)
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

        if self.textEntry.enabled:
            result = self.textEntry.result()
            if result != None:
                self.textEntry.setEnabled(False)
                if result != "":
                    self.client.remote('chat', result)

        # FIXME: remove this if possible, should really be in self.fsm
        if self.fsm.state == 'abilityTarget':
            self.showAbilityRange(self.unit,
                                  self.fsm.ability)
            self.showAbilityAOE(self.unit,
                                self.fsm.ability,
                                (self.cursor.x, self.cursor.y))

        # Move view smoothly if needed
        self.camera.adjustCamera(timeElapsed)

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
        glPolygonOffset(-5.0, -5.0)
        self.camera.sortSprites(self.unitDisplayers)
        for u in self.unitDisplayers:
            u.draw()

        # Draw the objects that have to be in front of the unit
        # sprites
        glPolygonOffset(1.0, 1.0)
        for obj in self.fgObjects:
            obj.draw()          

        # Update unit slide
        self._updateUnitSlide(timeElapsed)

    def unitDisplayer(self, unit):
        return self.unitDisplayersDict[unit]

    def handleEvent(self, event):
        if self.textEntry.enabled and event.type == pygame.KEYDOWN:
            self.textEntry.addEvent(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
            elif event.key == pygame.K_w:
                self.battle.playerGaveUp()

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
            
        elif event.type == Input.CURSOR_UP:
            if self.focusedElement == None:
                return
            Sound.cursorMove()
            if self.focusedElement == self.cursor:
                self.cursor.move(self.camera.cursorMovement(0, -1))
            else:
                self.focusedElement.moveUp()                
        elif event.type == Input.CURSOR_DOWN:
            if self.focusedElement == None:
                return
            Sound.cursorMove()
            if self.focusedElement == self.cursor:
                self.cursor.move(self.camera.cursorMovement(0, 1))
            else:
                self.focusedElement.moveDown()
        elif event.type == Input.CURSOR_LEFT:
            if self.focusedElement == None:
                return
            Sound.cursorMove()
            if self.focusedElement == self.cursor:
                self.cursor.move(self.camera.cursorMovement(-1, 0))
        elif event.type == Input.CURSOR_RIGHT:
            if self.focusedElement == None:
                return
            Sound.cursorMove()
            if self.focusedElement == self.cursor:
                self.cursor.move(self.camera.cursorMovement(1, 0))
        elif event.type == Input.CURSOR_ACCEPT:
            self.fsm.accept()
        elif event.type == Input.CURSOR_CANCEL:
            self.fsm.cancel()
        elif event.type == Input.ROTATE_CAMERA_CCW:
            self.camera.change(-1)
        elif event.type == Input.ROTATE_CAMERA_CW:
            self.camera.change(1)                   
        elif event.type == Input.PITCH_CAMERA:
            newPitch = self.camera.pitch() + event.amount
            self.camera.setPitch(newPitch)
        elif event.type == Input.START_CHAT:
            self.textEntry.setEnabled(True)


class ScenarioGUIFSM(FSM.FSM):
    def __init__(self, gui):
        self.gui = gui
        FSM.FSM.__init__(self, ['disabled',
                                'roaming',
                                'opponentTurn',
                                'battleMenu',
                                'specialMenu',
                                'abilityTarget',
                                'moveTarget',
                                'facing'])
        for s in self.states:
            self.addEntryHook(s, self.clearEverything)
            self.addEntryHook(s, getattr(self, "enter_" + s, self.doNothing))
        self.addExitHook(s, self.exit_facing)

    def checkMoveResult(self, result):
        if result:
            Sound.cursorClick()
            self.trans('disabled')
        else:
            Sound.cursorInvalid()

    def checkActResult(self, result):
        if result:
            self.trans('battleMenu')
        else:
            Sound.cursorInvalid()

    def checkFacingResult(self, result):
        if result:
            Sound.cursorClick()
            self.gui.clearTopText()
            self.trans('disabled')
        else:
            Sound.cursorInvalid()
            
    def accept(self):
        getattr(self, "accept_" + self.state, self.doNothing)()

    def cancel(self):
        getattr(self, "cancel_" + self.state, self.doNothing)()

    def doNothing(self, *args):
        Sound.cursorInvalid()

    def clearEverything(self, oldState, reason):
        self.gui.clearHighlights()

    def enter_disabled(self, oldState, reason):
        self.gui.focusedElement = None
        self.gui._battleMenu.setShowing(False)
        self.gui._specialMenu.setShowing(False)

    def enter_roaming(self, oldState, reason):
        self.gui.focusedElement = self.gui.cursor
        self.gui._battleMenu.setShowing(False)
        self.gui._specialMenu.setShowing(False)

    def cancel_roaming(self):
        Sound.cursorCancel()
        self.trans('battleMenu')

    def enter_opponentTurn(self, oldState, reason):
        self.gui.focusedElement = self.gui.cursor
        self.gui._battleMenu.setShowing(False)
        self.gui._specialMenu.setShowing(False)       

    def cancel_opponentTurn(self):
        Sound.cursorCancel()
        self.gui.scrollTo(self.gui.unit.posn())
        self.gui.cursor.setPosn(*self.gui.unit.posn())

    def accept_opponentTurn(self):
        Sound.cursorInvalid()
                                        
    def enter_battleMenu(self, oldState, reason):
        if oldState != 'specialMenu':
            self.gui._battleMenu.setSelectedOption(0)
        self.gui._battleMenu.setSelectedUnit(self.gui.unit)
        self.gui._specialMenu.setShowing(False)
        self.gui._battleMenu.setShowing(True)
        self.gui.cursor.setPosn(*self.gui.unit.posn())
        self.gui.focusedElement = self.gui._battleMenu
        self.gui.scrollTo(self.gui.unit.posn())
        
    def accept_battleMenu(self):
        choice = self.gui._battleMenu.getSelection()
        Sound.cursorClick()
        if choice == Sprite.BattleMenu.MOVE:
            self.trans('moveTarget')
        elif choice == Sprite.BattleMenu.ATTACK:
            self.trans('abilityTarget', self.gui.unit.attack())
        elif choice == Sprite.BattleMenu.SPECIAL:
            self.trans('specialMenu')
        elif choice == Sprite.BattleMenu.DONE:
            self.trans('facing')

    def cancel_battleMenu(self):
        Sound.cursorCancel()
        self.trans('roaming')

    def enter_specialMenu(self, oldState, reason):
        self.gui.focusedElement = self.gui._specialMenu
        self.gui.scrollTo(self.gui.unit.posn())
        self.gui._specialMenu.setSelectedUnit(self.gui.unit)
        self.gui._specialMenu.setSelectedOption(0)
        self.gui._specialMenu.setShowing(True)
        self.gui._battleMenu.setShowing(True)

    def accept_specialMenu(self):
        ability = self.gui._specialMenu.getSelection()
        if not ability:
            Sound.cursorInvalid()
            return
        Sound.cursorClick()
        self.trans('abilityTarget', ability)

    def cancel_specialMenu(self):
        Sound.cursorCancel()
        self.trans('battleMenu')

    def enter_abilityTarget(self, oldState, ability):
        self.ability = ability
        self.gui.focusedElement = self.gui.cursor
        self.gui.showAbilityRange(self.gui.unit, ability)

    def accept_abilityTarget(self):
        df = self.gui.client.remote('unitAct',
                                    self.ability.abilityID,
                                    self.gui.cursor.x,
                                    self.gui.cursor.y)
        df.addCallback(self.checkActResult)

    def cancel_abilityTarget(self):
        Sound.cursorCancel()
        self.trans('battleMenu')   
               
    def enter_moveTarget(self, oldState, reason):
        self.gui.focusedElement = self.gui.cursor
        self.gui.showMovementRange(self.gui.unit)

    def accept_moveTarget(self):
        df = self.gui.client.remote('unitMove',
                                    self.gui.cursor.x,
                                    self.gui.cursor.y)
        df.addCallback(self.checkMoveResult)

    def cancel_moveTarget(self):
        Sound.cursorCancel()
        self.trans('battleMenu')   

    def enter_facing(self, oldState, reason):
        self.gui.focusedElement = self.gui.cursor
        self.gui.cursor.setFacingMode(True)
        self.gui.setTopText(_("Choose unit facing..."))

    def accept_facing(self):
        df = self.gui.client.remote('unitFacing',
                                    self.gui.unit.facing())
        df.addCallback(self.checkFacingResult)

    def cancel_facing(self):
        self.trans('battleMenu')
        
    def exit_facing(self, newState, reason):
        self.gui.cursor.setFacingMode(False)
