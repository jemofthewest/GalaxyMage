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

#import GLUtil
import Resources
#import Clock
#from OpenGL.GL import *
#from OpenGL.GLU import *
import MapEditorGUI as GUI
#import engine.Faction as Faction
#import engine.Effect as Effect
#import math
import Sprite
import pygame
import Input

from OpenGL.GL import *
from OpenGL.GLU import *


class TileDataDisplayer(Sprite.TextDisplayer):
    def __init__(self, cursor):
        Sprite.TextDisplayer.__init__(self)
        self.cursor = cursor

    def getFont(self):
        return Resources.font(size=16, bold=True)

    def getBorder(self):
        return False

    
class TileColorDisplayer(TileDataDisplayer):
    def getText(self):
        color = self.cursor.mapSquare().color
        # FIXME: what do we do if the different sides of the map
        # square are different colors? For now, we'll just choose
        # color[0] as the one to display...
        if type(color) == list:
            color = color[0]
        return "TopColor: (%1.2f, %1.2f, %1.2f)" % (color[0], color[1], color[2])
    
class TileTextureDisplayer(TileDataDisplayer):
    def getText(self):
        texture = self.cursor.mapSquare().texture()
        # FIXME: what do we do if the different sides of the map
        # square are different colors? For now, we'll just choose
        # texture[0] as the one to display
        texture = texture[0]
        return "TopTexture: " + str(texture)

    
class TileTagDisplayer(TileDataDisplayer):
    def getText(self):
        tagName = self.cursor.mapSquare().tagName()
        return "Tag: " + tagName
    

class FirstHeightDisplayer(TileDataDisplayer):
    def __init__(self, cursor, camera, enabled=True):
        TileDataDisplayer.__init__(self,cursor)
        self._camera = camera
    def getText(self):
        height = self.cursor.mapSquare().height()
        cornerHeights = self.cursor.mapSquare().cornerHeights
        return "    %2d" % (cornerHeights[self._camera.getCorner(0)]+height)
    

class SecondHeightDisplayer(TileDataDisplayer):
    def __init__(self, cursor, camera, enabled=True):
        TileDataDisplayer.__init__(self,cursor)
        self._camera = camera
    def getText(self):
        height = self.cursor.mapSquare().height()
        cornerHeights = self.cursor.mapSquare().cornerHeights
        return "%2d   %2d   %2d" % (cornerHeights[self._camera.getCorner(2)]+height, height, cornerHeights[self._camera.getCorner(1)]+height)
    

class ThirdHeightDisplayer(TileDataDisplayer):
    def __init__(self, cursor, camera, enabled=True):
        TileDataDisplayer.__init__(self,cursor)
        self._camera = camera
    def getText(self):
        height = self.cursor.mapSquare().height()
        cornerHeights = self.cursor.mapSquare().cornerHeights
        return "         %2d" % (cornerHeights[self._camera.getCorner(3)]+height)

    
class TopMenu(Sprite.TextMenu):
    TILE_INFO = 0
    SET_TAG = 1
    EDIT_TAG = 2
    NEW_TAG = 3
    SAVE = 4
    
    def __init__(self, posn):
        Sprite.TextMenu.__init__(self, posn , 180, 8)
        self.setOptions(["Tile Info", "Set Terrain Tag", "Edit Terrain Tag", "New Terrain Tag", "Save"])
        self.setOptionEnabled(0, True)
        self.setOptionEnabled(1, True)
        self.selectedSquare = None
        self._showing = False
        self._enabled = True
        
    def setEnabled(self, enabled=True):
        raise Exception("MapEditorTopMenu cannot be enabled or disabled")
                
    def handleEvent(self, event):
        if event.type == Input.CURSOR_ACCEPT:
            choice = self.getSelection()
            if choice == TopMenu.TILE_INFO:
                self.setShowing(False)
                self.setSelectedOption(0)
                GUI.get().tileInfoDisplayer().setShowing(True)
                Input.get().setInDialog(True)
                return 'tileInfo'
            elif choice == TopMenu.SET_TAG:
                GUI.get().tagMenu().setShowing(True)
                return 'setTag'
            elif choice == TopMenu.EDIT_TAG:
                GUI.get().chooseTagMenu().setShowing(True)
                return 'chooseTag'
            elif choice == TopMenu.NEW_TAG:
                self.setShowing(False)
                self.setSelectedOption(0)
                GUI.get().addTagDialog().setShowing(True)
                Input.get().setInDialog(True)
                return 'addTag'
            elif choice == TopMenu.SAVE:
                self.setShowing(False)
                self.setSelectedOption(0)
                GUI.get().saveDialog().setShowing(True)
                Input.get().setInDialog(True)
                return 'save'
        elif event.type == Input.CURSOR_CANCEL:
            self.setShowing(False)
            return 'cursor'
        elif event.type == Input.CURSOR_UP:
            self.moveUp()
        elif event.type == Input.CURSOR_DOWN:
            self.moveDown()


class TagMenu(Sprite.TextMenu):
    def __init__(self, posn):
        Sprite.TextMenu.__init__(self, posn , 100, 8)
        self.setOptions([])
        self.selectedSquare = None
        self._showing = False
        self._enabled = True
        
    def setEnabled(self, enabled=True):
        raise Exception("MapEditorTagMenu cannot be enabled or disabled")
                
    def handleEvent(self, event):
        if event.type == Input.CURSOR_ACCEPT:
            tagNum = self.getSelection()
            tags = GUI.get().m.tags
            tagName = self.options[tagNum]
            GUI.get().cursor.mapSquare().setTag(tags[tagName])
            GUI.get().updateMap()
            self.setShowing(False)
            GUI.get().topMenu().setShowing(False)
            return 'cursor'
        elif event.type == Input.CURSOR_CANCEL:
            self.setShowing(False)
            return 'topMenu'
        elif event.type == Input.CURSOR_UP:
            self.moveUp()
        elif event.type == Input.CURSOR_DOWN:
            self.moveDown()


class TagMenu2(Sprite.TextMenu):
    def __init__(self, posn):
        Sprite.TextMenu.__init__(self, posn , 100, 8)
        self.setOptions([])
        self.selectedSquare = None
        self._showing = False
        self._enabled = True
        
    def setEnabled(self, enabled=True):
        raise Exception("MapEditorTagMenu cannot be enabled or disabled")
                
    def handleEvent(self, event):
        if event.type == Input.CURSOR_ACCEPT:
            tagNum = self.getSelection()
            tagName = self.options[tagNum]
            self.setSelectedOption(0)
            self.setShowing(False)
            GUI.get().topMenu().setSelectedOption(0)
            GUI.get().topMenu().setShowing(False)
            GUI.get().editTagDialog().setShowing(True, tagName)
            Input.get().setInDialog(True)
            return 'editTag'
        elif event.type == Input.CURSOR_CANCEL:
            self.setShowing(False)
            return 'topMenu'
        elif event.type == Input.CURSOR_UP:
            self.moveUp()
        elif event.type == Input.CURSOR_DOWN:
            self.moveDown()

            
class TileInfoDisplayer(Sprite.TextDisplayerBox):
    def __init__(self, posn, width, height = None):
        self.title = Sprite.TextDisplayer()
        self.title.setText("Tile Info")
        self.displayers = [self.title]
        
        self.numBoxes = 8
        self.outputBoxes = [Sprite.TextDisplayer() for i in xrange(0,self.numBoxes)]
        self.outputTitles = [Sprite.TextDisplayer() for i in xrange(0,self.numBoxes)]
        self.outputTitles[0].setText("Tag:")
        self.outputTitles[1].setText("Top Texture:")
        self.outputTitles[2].setText("Top Color:")
        self.outputTitles[3].setText("Side Textures:")
        self.outputTitles[4].setText("Side Colors:")
        self.outputTitles[5].setText("")
        self.outputTitles[6].setText("")
        self.outputTitles[7].setText("")
        
        for i in xrange(0,len(self.outputBoxes)):
            if len(self.outputTitles[i].getText()) > 0:
                self.displayers.append(self.outputTitles[i])
            self.displayers.append(self.outputBoxes[i])
        
        self.posn = posn
        self.width = width
        self.height = height
        self.borderListID = -1 
        self.borderTexture = -1
        self._showing = False
        
    def update(self, timeElapsed):
        pass
    
    def evalResult(self):
        pass
    
    def draw(self):
        if self._showing:
            Sprite.TextDisplayerBox.draw(self)
            
    def setShowing(self, show):
        self._showing = show
        if show == True:
            sq = GUI.get().cursor.mapSquare()
            self.outputBoxes[0].setText(sq.tagName())
            tag = GUI.get().m.tags[sq.tagName()]
            
            textures = tag['texture']
            sidetextures = []
            if type(textures) == type([]):
                sidetextures = textures[1:]
                textures = textures[0]
            self.outputBoxes[1].setText(str(textures))
            self.outputBoxes[3].setText(str(sidetextures))
            
            topcolorstr = "(%1.2f, %1.2f, %1.2f)" % (sq.color[0][0],sq.color[0][1],sq.color[0][2])
            self.outputBoxes[2].setText(topcolorstr)
            for i in xrange(1,5):
                sidecolorstr = ("(%1.2f, %1.2f, %1.2f)" % (sq.color[i][0],sq.color[i][1],sq.color[i][2]))
                self.outputBoxes[3+i].setText(sidecolorstr)
            
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or
           event.key == pygame.K_ESCAPE):
            self.setShowing(False)
            Input.get().setInDialog(False)
            return 'cursor'
        
        
class Dialog(Sprite.TextDisplayerBox):
    def __init__(self, title, inputBoxes, inputTitles,
                 posn, width, height = None):
        self.title = title
        self.inputBoxes = inputBoxes
        self.inputTitles = inputTitles
        self.displayers = [title]
        for i in xrange(0,len(inputBoxes)):
            if len(inputTitles[i].getText()) > 0:
                self.displayers.append(inputTitles[i])
            self.displayers.append(inputBoxes[i])
        self.posn = posn
        self.width = width
        self.height = height
        self.borderListID = -1 
        self.borderTexture = -1
        self._showing = False

    def update(self, timeElapsed):
        pass
    
    def evalResult(self):
        pass
    
    def draw(self):
        if self._showing:
            Sprite.TextDisplayerBox.draw(self)
            
    def setShowing(self, show):
        self._showing = show
        
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.state += 1                
            if self.state >= len(self.inputBoxes):
                self.state = 0
                self.evalResult()
                self.setShowing(False)
                Input.get().setInDialog(False)
                for b in self.inputBoxes:
                    b.setText('')
                GUI.get().topMenu().setShowing(False)
                return 'cursor'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state > 0:
                #self.inputBoxes[self.state].setText('')
                self.state -= 1
            else:
                self.setShowing(False)
                Input.get().setInDialog(False)
                for b in self.inputBoxes:
                    b.setText('')
                return 'cursor'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.inputBoxes[self.state].delChar()
            if ((event.key >= pygame.K_0 and event.key <= pygame.K_9) or
                (event.key >= pygame.K_a and event.key <= pygame.K_z) or
                event.key == pygame.K_PERIOD or event.key == pygame.K_MINUS):
                self.inputBoxes[self.state].append(chr(event.key))

                
class AddTagDialog(Dialog):
    def __init__(self, posn, width):
        self.numBoxes = 8
        title = Sprite.TextDisplayer()
        title.setText("Add Tag Dialog")
        inputBoxes = [InputBox() for i in xrange(0,self.numBoxes)]
        inputTitles= [Sprite.TextDisplayer() for i in xrange(0,self.numBoxes)]
        inputTitles[0].setText("Name:")
        inputTitles[1].setText("Texture:")
        inputTitles[2].setText("Color:")
        inputTitles[3].setText("")
        inputTitles[4].setText("")
        inputTitles[5].setText("ColorVar:")
        inputTitles[6].setText("")
        inputTitles[7].setText("")
        Dialog.__init__(self, title, inputBoxes, inputTitles, posn, width)
        self.state = 0
        
    def evalResult(self):
        tags = GUI.get().m.tags
        tagName = self.inputBoxes[0].getText()
        texture = self.inputBoxes[1].getText()
        color = (float(self.inputBoxes[2].getText()),
                 float(self.inputBoxes[3].getText()),
                 float(self.inputBoxes[4].getText()))
        colorVar = (float(self.inputBoxes[5].getText()),
                    float(self.inputBoxes[6].getText()),
                    float(self.inputBoxes[7].getText()))
        if not tags.has_key(tagName):
            tags[tagName] = {}
        tag = tags[tagName]
        tag['name'] = tagName
        tag['texture'] = texture
        tag['color'] = color
        tag['colorVar'] = colorVar
        GUI.get().updateMap()

        
class EditTagDialog(Dialog):
    def __init__(self, posn, width):
        self.numBoxes = 7
        title = Sprite.TextDisplayer()
        title.setText("Edit Tag Dialog")
        inputBoxes = [InputBox() for i in xrange(0,self.numBoxes)]
        inputTitles= [Sprite.TextDisplayer() for i in xrange(0,self.numBoxes)]
        inputTitles[0].setText("Texture:")
        inputTitles[1].setText("Color:")
        inputTitles[2].setText("")
        inputTitles[3].setText("")
        inputTitles[4].setText("ColorVar:")
        inputTitles[5].setText("")
        inputTitles[6].setText("")
        Dialog.__init__(self, title, inputBoxes, inputTitles, posn, width)
        self.state = 0
        self.tagName = None
        
    def setShowing(self, show, tagName=None):
        self._showing = show
        if show == True and tagName != None:
            self.title.setText("Edit Tag Dialog: " + str(tagName))
            tag = GUI.get().m.tags[tagName]
            self.tag = tag
            texture = tag['texture']
            if type(texture) == type([]):
                texture = texture[0]
            self.inputBoxes[0].setText(texture)
            color = tag['color']
            if type(color) == type([]):
                color = color[0]
            print str(color)
            self.inputBoxes[1].setText(str(color[0]))
            self.inputBoxes[2].setText(str(color[1]))
            self.inputBoxes[3].setText(str(color[2]))
            colorVar = tag['colorVar']
            if type(colorVar) == type([]):
                colorVar = colorVar[0]
            print str(colorVar)
            self.inputBoxes[4].setText(str(colorVar[0]))
            self.inputBoxes[5].setText(str(colorVar[1]))
            self.inputBoxes[6].setText(str(colorVar[2]))
            
            
    def evalResult(self):
        texture = self.inputBoxes[0].getText()
        color = (float(self.inputBoxes[1].getText()),
                 float(self.inputBoxes[2].getText()),
                 float(self.inputBoxes[3].getText()))
        colorVar = (float(self.inputBoxes[4].getText()),
                    float(self.inputBoxes[5].getText()),
                    float(self.inputBoxes[6].getText()))
        tag = self.tag
        if type(tag['texture']) == type([]):
            tag['texture'][0] = texture            
        else:
            tag['texture'] = texture
        if type(tag['color']) == type([]):
            tag['color'][0] = color
        else:
            tag['color'] = color
        if type(tag['colorVar']) == type([]):
            tag['colorVar'][0] = colorVar
        else:
            tag['colorVar'] = colorVar
        GUI.get().updateMap()
        
        
class SaveDialog(Dialog):
    def __init__(self, posn, width):
        self.numBoxes = 1
        title = Sprite.TextDisplayer()
        title.setText("Add Tag Dialog")
        inputBoxes = [InputBox() for i in xrange(0,self.numBoxes)]
        inputTitles= [Sprite.TextDisplayer() for i in xrange(0,self.numBoxes)]
        inputTitles[0].setText("Filename:")
        Dialog.__init__(self, title, inputBoxes, inputTitles, posn, width)
        self.state = 0
        
    def evalResult(self):
        GUI.get().saveMap(self.inputBoxes[0].getText())
        
class InputBox(Sprite.TextDisplayer):
    def __init__(self):
        Sprite.TextDisplayer.__init__(self)
    
    def append(self, c):
        self.text += c
    
    def delChar(self, ):
        self.text = self.text[0:-1]
