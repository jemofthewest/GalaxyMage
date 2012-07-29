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

import GLUtil
import Resources
import Clock
from OpenGL.GL import *
from OpenGL.GLU import *
import ScenarioGUI
import engine.Faction as Faction
import engine.Effect
import math
import time
import Constants
import pygame
import gui.Input
import string

class Sprite(object):
    def __init__(self):
        pass

    def draw(self):
        pass
    
    def update(self, time):
        pass

class UnitDisplayer(Sprite):
    def __init__(self, unit):
        Sprite.__init__(self)
        self.__unit = unit
        
        imageName = unit.getSprites('standing')[0]
        self.__texture = GLUtil.makeTexture(Resources.image(imageName))[0]
        wimageName = None
        self.__otexture = None
        self.__wtexture = None
        self.__weaponGrip = None
        self.__unitHand = None
        
        if unit.weapon() != None:
            wimageName = unit.weapon().getSprites('standing')[0]
            self.__weaponGrip = Resources.spriteConfig.grip(wimageName)
            self.__unitHand = Resources.spriteConfig.hand(imageName)
            
        if wimageName != None:
            self.__wtexture = GLUtil.makeTexture(Resources.image(wimageName))[0]
            oimageName = unit.getOverSprites('standing')
            if oimageName != []:
                oimageName = oimageName[0]
                self.__otexture = GLUtil.makeTexture(Resources.image(oimageName))[0]
        
        self.__offsetX = 0.0
        self.__offsetY = 0.0
        self.__offsetZ = 0.0
        self._animations = []
        self._color = (1.0, 1.0, 1.0, 1.0)

        # The number of color and Texture Status
        # and time for animation between Status
        self._colorStatus = -1
        self._textureStatus = -1
        self._textureTime = time.time()
        self._colorTime = time.time()

        self._unitStatusColor = (1.0, 1.0, 1.0, 1.0)

        self._isActing = False

    def isActing(self):
        return self._isActing

    def Acting(self):
        self._isActing = True

    def notActing(self):
        self._isActing = False
    
    def __del__(self):
        try:
            glDeleteTextures([self.__texture])
        except:
            pass

    def update(self, elapsedTime):
        (r, g, b, a) = (1.0, 1.0, 1.0, 1.0)
#         # Set statusEffectMult to the range [0.0, 1.0]
#         statusEffectMult = (math.sin(Clock.get().getTime() * 4.0) +
#                             1.0) / 2.0
#         # Scale to [0.2, 0.7]
#         statusEffectMult = statusEffectMult * 0.5 + 0.5

#         if self.__unit.statusEffects().has(Effect.Status.HASTE):
#             color = (1.0, 0.0, 0.0, 1.0)
#             (r, g, b, a) = (color[0] + statusEffectMult,
#                             color[1] + statusEffectMult,
#                             color[2] + statusEffectMult,
#                             color[3] + statusEffectMult)
        

            
        if not self.__unit.alive():
            (r, g, b, a) = (self._color[0] - elapsedTime,
                            self._color[1] - elapsedTime,
                            self._color[2] - elapsedTime,
                            self._color[3] - elapsedTime)
        self._color = (r, g, b, a)

        for a in self._animations:
            a.update(elapsedTime)
        for a in self._animations:
            if a.done():
                self._animations.remove(a)

    def draw(self):
        #glDisable(GL_DEPTH_TEST)
        if self._color[3] < 0.0:
            return
        
        glDisable(GL_LIGHTING)
        glDepthFunc(GL_LEQUAL)
        glPushMatrix()
        GLUtil.mapTrans(self.x, self.y, self.z)

        # Draw the circle around the unit's feet
        (r, g, b) = Faction.color(self.__unit.faction())
        none = Resources.texture("none")
        glBindTexture(GL_TEXTURE_2D, none)
        glPushMatrix()
        if self.__unit.facing() == Constants.E:
            glRotate(-90.0, 0.0, 0.0, 1.0)
        elif self.__unit.facing() == Constants.S:
            glRotate(180.0, 0.0, 0.0, 1.0)
        elif self.__unit.facing() == Constants.W:
            glRotate(90.0, 0.0, 0.0, 1.0)           
        glColor4f(r, g, b, 1.0 * self._color[3])
        glBegin(GL_TRIANGLES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(-0.15, 0.35, 0.0)
        glVertex3f(0.15, 0.35, 0.0)
        glEnd()
        glPopMatrix()
        quad = gluNewQuadric()
        gluDisk(quad, 0.3, 0.4, 32, 1)
        gluDeleteQuadric(quad)

        # Checking for texture and color status
        unitStatus = self.__unit.statusEffects()
        if len(unitStatus.texture()) == 0 :
            self._textureStatus = -1
        else:
            if time.time() > self._textureTime:
                self._textureTime = time.time() +1.1
                self._textureStatus += 1
                if self._textureStatus >= len(unitStatus.texture()):
                    self._textureStatus = 0
            try:
                if engine.Effect.Status.effectTextures[unitStatus.texture()[self._textureStatus]] != None:
                    GLUtil.makeStatus(engine.Effect.Status.effectTextures[unitStatus.texture()[self._textureStatus]], self._color)
            except:
                # when the status is over this can happen
                pass

        statuscolor = None
        if len(unitStatus.color()) == 0 :
            self._colorStatus = -1
        else:
            if time.time() > self._colorTime:
                self._colorTime = time.time() +1.3
                self._colorStatus += 1
                if self._colorStatus >= len(unitStatus.color()):
                    self._colorStatus = 0
            try:
                if engine.Effect.Status.effectTextures[unitStatus.color()[self._colorStatus]] != None:
                    statuscolor = engine.Effect.Status.effectTextures[unitStatus.color()[self._colorStatus]]
            except :
                pass

        if statuscolor == None :
            if self.isActing() == True:
                self._unitStatusColor = self._color
            else:
                GLUtil.makeUnit(texture = self.__texture,
                                wtexture = self.__wtexture,
                                otexture = self.__otexture, 
                                color = self._color,
                                weaponGrip = self.__weaponGrip,
                                unitHand = self.__unitHand)
        else:
            if self.isActing() == True:
                self._unitStatusColor = statuscolor
            else:
                GLUtil.makeUnit(texture = self.__texture,
                                wtexture = self.__wtexture,
                                otexture = self.__otexture, 
                                color = statuscolor,
                                weaponGrip = self.__weaponGrip,
                                unitHand = self.__unitHand)
                
        for a in self._animations:
            a.draw()

        glPopMatrix()
        glDepthFunc(GL_LESS)
        glEnable(GL_LIGHTING)
        #glEnable(GL_DEPTH_TEST)

    def addAnimation(self, animation):
        self._animations.append(animation)

    def resetSlide(self):
        self.__offsetX = 0.0
        self.__offsetY = 0.0
        self.__offsetZ = 0.0

    def slide(self, x, y, z):
        self.__offsetX += x
        self.__offsetY += y
        self.__offsetZ += z

    def setPosn(self, x, y, z):
        self.__offsetX = x - self.__unit.x()
        self.__offsetY = y - self.__unit.y()
        self.__offsetZ = z - self.__unit.z()
        
    def getX(self):
        return self.__unit.x() + self.__offsetX

    def getY(self):
        return self.__unit.y() + self.__offsetY

    def getZ(self):
        return self.__unit.z() + self.__offsetZ

    x = property(getX)
    y = property(getY)
    z = property(getZ)
    

class TextDisplayer(Sprite):
    def __init__(self, enabled=True):
        Sprite.__init__(self)
        self.enabled = enabled
        self.texture = -1
        self.renderedSize = (0,0)
        self.listID = -1
        self.posn = (0,0)
        self.color = (255,255,255)
        self.text = ""
        self.font = Resources.font(size=16, bold=True)
        self.lastColor = self.color
        self.lastText = self.text
        self.centerx = False
        self.centery = False
        self.border = False

    def __del__(self):
        if self.texture != -1:
            try:
                glDeleteTextures([self.texture])
            except:
                pass
        if self.listID != -1:
            try:
                glDeleteLists(self.listID,1)
            except:
                pass

    # Override this method to return the text you want to display
    def getText(self):
        return self.text

    # This method can be used to set the text you want to display
    # without overriding getText()
    def setText(self, text):
        self.text = text

    # Override this method to return the font you want to use
    def getFont(self):
        return self.font

    # This method can be used to set the font you want to use
    # without overriding getFont()
    def setFont(self, font):
        self.font = font

    # Override this method to return the color you want to use
    def getColor(self):
        return self.color

    # This method can be used to set the color you want to use
    # without overriding getColor()
    def setColor(self, color):
        self.color = color

    # Override this method if you want a border
    def getBorder(self):
        return self.border

    def setBorder(self, border):
        self.border = border

    # Override this method to return the position you want the text to
    # be drawn at
    def getPosn(self):
        return self.posn

    # This method can be used to set the position you want the text to
    # be drawn at without overriding getPosn()
    def setPosn(self, posn):
        self.posn = posn

    # Override this method if you want a non-transparent background
    def getBackgroundColor(self):
        return None

    def getCenterX(self):
        return self.centerx

    def getCenterY(self):
        return self.centery

    def setCenterX(self, centerx):
        self.centerx = centerx

    def setCenterY(self, centery):
        self.centery = centery

    def toggle(self):
        self.enabled = not self.enabled

    def setEnabled(self, enabled):
        self.enabled = enabled

    def invalidate(self):
        self.lastText = ''

    def draw(self):
        if not self.enabled:
            self.lastText = ""
            return
        text = self.getText()
        color = self.getColor()
        glDisable(GL_LIGHTING)
        if self.lastText != text or self.lastColor != color:
            self.lastText = text
            self.lastColor = color
            if self.texture != -1:
                glDeleteTextures([self.texture])
            if self.listID != -1:
                glDeleteLists(self.listID,1)
            (self.texture,
             self.listID,
             self.renderedSize) = GLUtil.drawText(self.getFont(),
                                                  color,
                                                  text,
                                                  self.getPosn(),
                                                  self.getBorder(),
                                                  self.getBackgroundColor(),
                                                  self.getCenterX(),
                                                  self.getCenterY())
        else:
            if self.listID > 0:
                glCallList(self.listID)
        glEnable(GL_LIGHTING)
        
class FPSDisplayer(TextDisplayer):
    def __init__(self):
        TextDisplayer.__init__(self, False)
        self.font = Resources.font(size=16, bold=True)

    def getText(self):
        return "FPS: %d" % Clock.get().getFPS()

    def getFont(self):
        return self.font

    def getPosn(self):
        return (0, 0)

    def getBackgroundColor(self):
        return (0,0,0,255)
    

class CursorPosnDisplayer(TextDisplayer):
    def __init__(self, cursor):
        TextDisplayer.__init__(self)
        self.cursor = cursor

    def getFont(self):
        return Resources.font(family="mono", size=16, bold=True)

    def getPosn(self):
        return (10, 10)

    def getText(self):
        posn = self.cursor.posn3d()
        return _("(%2d,%2d) h:%2d") % posn

    def getBorder(self):
        return True

    
class UnitStatsDisplayer(TextDisplayer):
    # Subclasses should override getPosn() and getText()
    def __init__(self, cursor):
        TextDisplayer.__init__(self)
        self.cursor = cursor

    def getFont(self):
        return Resources.font(size=16, bold=True)

    def getBorder(self):
        return False


class UnitNameDisplayer(UnitStatsDisplayer):
    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return unit.name()

class UnitBarDisplayer(Sprite):
    def __init__(self, w, h):
        self._width = w
        self._height = h
        self._leftColor = [1.0, 0.0, 0.0, 1.0]
        self._rightColor = [0.0, 1.0, 0.0, 1.0]
    
    def draw(self, width, posn):
        rightR = (self._rightColor[0] * width -
                  self._leftColor[0] * (1.0 - width))
        rightG = (self._rightColor[1] * width -
                  self._leftColor[1] * (1.0 - width))
        rightB = (self._rightColor[2] * width -
                  self._leftColor[2] * (1.0 - width))
        GLUtil.drawBar(self._leftColor,
                       [rightR, rightG, rightB, 1.0],
                       self._width*width, self._height,
                       posn)


class UnitHPDisplayer(UnitStatsDisplayer):
    def __init__(self, cursor):
        UnitStatsDisplayer.__init__(self, cursor)
        self._barDisplayer = UnitBarDisplayer(215, 10)
    
    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return _("HP: %d/%d") % (unit.hp(), unit.mhp())

    def draw(self):
        unit = self.cursor.hoveredUnit()
        width = 1.0 * unit.hp() / unit.mhp()
        self._barDisplayer.draw(width, (self.posn[0]+35, self.posn[1]+7))
        UnitStatsDisplayer.draw(self)

class UnitSPDisplayer(UnitStatsDisplayer):
    def __init__(self, cursor):
        UnitStatsDisplayer.__init__(self, cursor)
        self._barDisplayer = UnitBarDisplayer(215, 10)

    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return _("SP: %d/%d") % (unit.sp(), unit.msp())

    def draw(self):
        unit = self.cursor.hoveredUnit()
        width = 1.0 * unit.sp() / unit.msp()
        self._barDisplayer.draw(width, (self.posn[0]+35, self.posn[1]+7))
        UnitStatsDisplayer.draw(self)

class UnitMovementDisplayer(UnitStatsDisplayer):
    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return _("Move: %d  Jump: %d") % (unit.move(), unit.jump())


class UnitPhysicalDisplayer(UnitStatsDisplayer):
    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return _("W.Atk: %d  W.Def: %d") % (unit.watk(), unit.wdef())


class UnitMagicalDisplayer(UnitStatsDisplayer):
    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return _("M.Atk: %d  M.Def: %d") % (unit.matk(), unit.mdef())


class UnitClassDisplayer(UnitStatsDisplayer):
    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return _("Lv. %d %s") % (unit.level(), unit.className())


class UnitSpeedDisplayer(UnitStatsDisplayer):
    def getText(self):
        unit = self.cursor.hoveredUnit()
        if unit == None:
            return ""
        else:
            return _("Speed: %d") % unit.speed()

class TextDisplayerBox(Sprite):
    def __init__(self, textDisplayers, posn, width, height = None):
        self.displayers = textDisplayers
        self.posn = posn
        self.width = width
        self.height = height
        self.borderListID = -1 
        self.borderTexture = -1

    def __del__(self):
        if self.borderListID != -1:
            try:
                glDeleteLists(self.borderListID, 1)
            except:
                pass
        if self.borderTexture != -1:
            try:
                glDeleteTextures([self.borderTexture])
            except:
                pass

    def size(self):
        return (self.width, self.height)

    # FIXME: make this a generic method?
    def makeBorder(self):
        width = self.width
        height = self.height
        if height == None:
            height = len(self.displayers)
        height *= 20

        image = GLUtil.createBorder(width, height)

        (texture, image) = GLUtil.makeTexture(image, None)

        listID = glGenLists(1)
        glNewList(listID, GL_COMPILE_AND_EXECUTE)
        GLUtil.drawAt(self.posn, texture, image)
        glEndList()
        return (listID, texture)
    
    def draw(self):
        if self.borderListID == -1:
            (self.borderListID, self.borderTexture) = self.makeBorder()

        displaySomething = False
        for d in self.displayers:
            if d.getText() != "":
                displaySomething = True
        if not displaySomething:
            return

        glDisable(GL_LIGHTING)
        (x, y) = self.posn
        y += 10
        x += 10
        glCallList(self.borderListID)
        for d in self.displayers:
            d.setPosn((x, y))
            d.draw()
            y += 20
        glEnable(GL_LIGHTING)

    def setPosn(self, posn):
        self.posn = posn

    def invalidate(self):
        if self.borderListID != -1:
            glDeleteLists(self.borderListID, 1)
        if self.borderTexture != -1:
            glDeleteTextures([self.borderTexture])
        self.borderListID = -1
        for d in self.displayers:
           d.invalidate()

class TextMenu(Sprite):
    def __init__(self, posn, width, nOptions):
        self.displayers = []
        self.options = []
        self.enabledOptions = []
        self.posn = posn
        for i in xrange(nOptions):
            td = TextDisplayer()
            td.setText("")
            td.setFont(Resources.font(size=16, bold=True))
            self.displayers.append(td)
        self.box = TextDisplayerBox(self.displayers,
                                    posn,
                                    width,
                                    nOptions)
        self.selectedOption = 0
        self._showing = False

        (textureID,
         image,
         renderedSize) = GLUtil.renderTextToTexture(Resources.font(size=16,
                                                                   bold=True),
                                                    (255,255,255,255),
                                                    ">",
                                                    False,
                                                    None)
        self.cursorImage = image
        self.cursorTexture = textureID

    def size(self):
        return self.box.size()

    def __del__(self):
        try:
            glDeleteTextures([self.cursorTexture])
        except:
            pass

    def setSelectedOption(self, option):
        self.selectedOption = 0
        if len(self.options) > 0 and not self.enabledOptions[0]:
            self.moveDown(True)

    # FIXME: this should not make us enabled or showing
    def setOptions(self, options):
        self.selectedOption = 0
        self.options = options
        self.enabledOptions = [True for i in xrange(0, len(options))]
        for i in xrange(0, len(self.displayers)):
            text = ""
            if i < len(options):
                text = "    " + options[i]
                self.setOptionEnabled(i, True)
            self.displayers[i].setText(text)

    def setOptionEnabled(self, optionIndex, enabled):
        self.enabledOptions[optionIndex] = enabled
        if enabled:
            self.displayers[optionIndex].setColor((255, 255, 255))
        else:
            self.displayers[optionIndex].setColor((160, 160, 160))
            if optionIndex == self.selectedOption:
                self.moveDown(True)

    def clearOptions(self):
        self.setOptions([])
        self._showing = False

    def draw(self):
        if self._showing and len(self.options) > 0:
            glDisable(GL_LIGHTING)
            self.box.draw()
            cursorX, cursorY = self.posn
            cursorX += 12
            cursorY += 12 + 20 * self.selectedOption

            GLUtil.drawAt((cursorX, cursorY),
                          self.cursorTexture, self.cursorImage)

            glEnable(GL_LIGHTING)

    # FIXME: get rid of force arg
    def moveUp(self, force=False):
        self.moveUpHelper()       
        steps = 0
        while (steps < len(self.options) and
               not self.enabledOptions[self.selectedOption]):
            self.moveUpHelper()
            steps += 1

    def moveUpHelper(self):
        self.selectedOption -= 1
        if self.selectedOption < 0:
            self.selectedOption = len(self.options) - 1

    # FIXME: get rid of force arg
    def moveDown(self, force=False):
        self.moveDownHelper()
        steps = 0
        while (steps < len(self.options) and
               not self.enabledOptions[self.selectedOption]):
            self.moveDownHelper()
            steps += 1

    def moveDownHelper(self):
        self.selectedOption += 1
        if self.selectedOption >= len(self.options):
            self.selectedOption = 0

    def getSelection(self):
        return self.selectedOption

    def setEnabled(self, enabled):
        self._enabled = enabled

    def setShowing(self, showing):
        self._showing = showing

    def enabled(self):
        return self._enabled

    def showing(self):
        return self._showing

    def setPosn(self, posn):
        self.posn = posn
        self.box.setPosn(posn)

    def invalidate(self):
        self.box.invalidate()

class BattleMenu(TextMenu):
    MOVE = 0
    ATTACK = 1
    SPECIAL = 2
    DONE = 3
    
    def __init__(self, posn):
        TextMenu.__init__(self, posn , 100, 8)
        self.setOptions([_("Move"), _("Attack"), _("Special"), _("Done")])
        self.selectedUnit = None
        self._showing = False
        
    def setSelectedUnit(self, u):
        self.selectedUnit = u

    def moveActCancel(self, move, act, cancel):
        if self.selectedUnit != None:
            self.setOptionEnabled(0, move)
            self.setOptionEnabled(1, act)
            self.setOptionEnabled(2, act and self.selectedUnit.abilities())
            self.setOptionEnabled(3, True)
            self.selectedOption = 0
            while not self.enabledOptions[self.selectedOption]:
                self.selectedOption += 1

# FIXME: make sure this behaves OK even when all options are disabled
class SpecialMenu(TextMenu):
    def __init__(self, posn):
        TextMenu.__init__(self, posn, 140, 8)
        self.selectedUnit = None
        self._abilities = []
        self.setShowing(True)
        
    def setSelectedUnit(self, u):
        self.selectedUnit = u
        if u == None:
            self.setShowing(False)
            return
        self._abilities = u.abilities()
        self._abilities.sort(lambda x, y: cmp(x.name(), y.name()))
        self.setOptions([a.name() for a in self._abilities])
        self.setEnabled(False)
        self.setShowing(False)
        self.selectedOption = 0
        self.update(0.0)

    def getSelection(self):
        if not self.enabledOptions[self.selectedOption]:
            return None
        return self._abilities[self.selectedOption]
        
    def update(self, time):
        if self.selectedUnit != None:
            enabled = False
            for i in xrange(0, len(self.options)):
                enoughSP = (self.selectedUnit.sp() >=
                            self._abilities[i].cost())
                correctWeapon = self._abilities[i].correctWeapon(
                    self.selectedUnit.weapon())
                enable = enoughSP and correctWeapon
                self.setOptionEnabled(i, enable)
                if enable:
                    enabled = True
            if self._showing and enabled:
                ability = self.getSelection()
                ScenarioGUI.get().setTopText(ability.description() +
                                            _(" (%d SP)") % ability.cost())

class Animation(Sprite):
    def done(self):
        return True

RED = (255, 0, 0) # FIXME: rm 0-255 color tuple
GREEN = (128, 255, 128)
WHITE = (255, 255, 255)
BENEFICIAL = 0
NEUTRAL = 1
NEGATIVE = 2

class DamageDisplayer(Animation):
    def __init__(self, damageAmount, beneficial=NEUTRAL, delay=0.0):
        if beneficial == BENEFICIAL:
            color = GREEN
        elif beneficial == NEGATIVE:
            color = WHITE
        else:
            color = WHITE
        self._time = -delay
        (self._texture,
         i,
         isize) = GLUtil.renderTextToTexture(Resources.font(size=48),
                                             color,
                                             str(damageAmount),
                                             False, None)
        self._aspectRatio = float(isize[0]) / isize[1]
        
    def __del__(self):
        try:
            glDeleteTextures([self._texture])
        except:
            pass
        
    def update(self, elapsedTime):
        self._time += elapsedTime

    def draw(self):
        height = 0.5 + 1.0 * self._time
        if self._time < 0.0:
            alpha = 0.0
        elif self._time < 0.25:
            alpha = 4.0 * self._time
        elif self._time > 0.75:
            alpha = 1.0 - 4.0 * (self._time - 0.75)
        else:
            alpha = 1.0
        GLUtil.drawFloatingText(self._texture, self._aspectRatio,
                                height, alpha)
        
    def done(self):
        return self._time > 1.0

class AttackDisplayer(Animation):
    def __init__(self, unit, delay=0.0, attackStyle="melee"):
        # Number of frames of the attack animation
        self._maxFrame = unit.getSprites(attackStyle).__len__()
        if self._maxFrame == 0:
            attackStyle = 'standing'
            self._maxFrame = unit.getSprites(attackStyle).__len__()
        
        # Load the textures
        self._unitHand = []
        self._texture = []
        for image in unit.getSprites(attackStyle):
            self._texture.append(GLUtil.makeTexture(Resources.image(image))[0])
            self._unitHand.append(Resources.spriteConfig.hand(image))
        
        # Load the weapon textures
        self._wtexture = None
        self._weapGrip = None
        if unit.weapon() != None:
            wimage = unit.weapon().getSprites('standing')[0]
            if wimage != None:
                self._wtexture = GLUtil.makeTexture(Resources.image(wimage))[0]
                self._weapGrip = Resources.spriteConfig.grip(wimage)
        else:
            wimage = None
            
        # Load the over textures
        self._otexture = []
        if wimage != None:
            oimages = unit.getOverSprites(attackStyle)
            if len(oimages) < self._maxFrame:
                oimages = []
            for image in oimages:
                self._otexture.append(
                    GLUtil.makeTexture(Resources.image(image))[0])

            
        self._unitdisplayer = ScenarioGUI.get().unitDisplayer(unit)        
        self._unitdisplayer.Acting()
        self._time = -delay
        self._frame = 0
        
    def __del__(self):
        try:
            glDeleteTextures([self._texture])
        except:
            pass
        
    def update(self, elapsedTime):
        self._time += elapsedTime

    def draw(self):
        if self._time > 0.1 *self._frame:
            self._frame +=1
        if self._frame > self._maxFrame - 1:
            self._frame = self._maxFrame - 1
        if self._texture == []:
            return
        if self._otexture == []:
            GLUtil.makeUnit(self._texture[self._frame],
                            wtexture = self._wtexture,
                            weaponGrip = self._weapGrip,
                            unitHand = self._unitHand[self._frame],
                            color = self._unitdisplayer._unitStatusColor)
        else:
            GLUtil.makeUnit(self._texture[self._frame],
                            wtexture = self._wtexture,
                            otexture = self._otexture[self._frame], 
                            weaponGrip = self._weapGrip,
                            unitHand = self._unitHand[self._frame],
                            color = self._unitdisplayer._unitStatusColor)
        
    def done(self):
        if self._time > 0.8:
            self._unitdisplayer.notActing()
            return True
        else:
            return False


class TextEntry(TextDisplayer):
    def __init__(self):
        TextDisplayer.__init__(self)
        self.setEnabled(False)
        self.setText("> ")
        self._result = None
        self.events = []

    def setEnabled(self, enabled):
        TextDisplayer.setEnabled(self, enabled)
        if enabled:
            gui.Input.get().setInDialog(True)
        else:
            gui.Input.get().setInDialog(False)
            self.setText("> ")
            self._result = None
            
    def result(self):
        return self._result

    def addEvent(self, event):
        self.events.append(event)

    def update(self, timeElapsed):
        if not self.enabled:
            return
        for event in self.events:
            text = self.getText()
            if event.key == pygame.K_BACKSPACE:
                if len(text) > 2:
                    self.setText(text[:-1])
            elif event.key == pygame.K_RETURN:
                self._result = text[2:]
            elif event.key == pygame.K_ESCAPE:
                self._result = ''
            else:
                char = event.unicode
                if char in string.printable:
                    self.setText(text + char)
        self.events = []
