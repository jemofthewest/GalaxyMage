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

import pygame
import gui.Sprite as Sprite
import gui.MainWindow as MainWindow
import gui.Input as Input
import Resources
import Main
import twistedmain
import FSM
import gui.MapEditorSprite
from OpenGL.GL import *

class ScenarioChooser(MainWindow.MainWindowDelegate):
    def __init__(self):
        MainWindow.MainWindowDelegate.__init__(self)
        glClearColor(0.0, 0.0, 0.25, 0.0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self._result = None
        self._gmVer = Sprite.TextDisplayer()
        self._gmVer.setText("GalaxyMage %s" % Main.__version__)
        self._gmVer.setFont(Resources.font(size=14, bold=False))
        self._label = Sprite.TextDisplayer()
        self._label.setFont(Resources.font(size=20, bold=True))
        self._menu = ScenarioChooserMenu()
        self._menu.setEnabled(True)
        self.addressEntry = Sprite.TextEntry()
        self.resize(MainWindow.get().size())
        self.fsm = ScenarioChooserFSM(self)
            
        self.scenario = None
        self.multiplayer = None
        self.serverAddress = None
        self.hostGame = None
        self.readyToStart = False

    def result(self):
        return self._result
    
    def update(self, timeElapsed):
        """Updates the ScenarioChooser GUI."""
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)      
        glLoadIdentity()
        for s in [self._menu, self._gmVer, self._label, self.addressEntry]:
            s.update(timeElapsed)
            s.draw()

    def handleEvent(self, event):
        """Takes in an event and returns True if the event was handled."""
        if self.fsm.state == 'serverAddress':
            if event.type == pygame.KEYDOWN:
                self.addressEntry.addEvent(event)
            if self.addressEntry.result() != None:
                self.serverAddress = self.addressEntry.result()
                self.readyToStart = True
                self.addressEntry.setEnabled(False)
        elif event.type == Input.CURSOR_UP:
            self._menu.moveUp()
        elif event.type == Input.CURSOR_DOWN:
            self._menu.moveDown()
        elif event.type == Input.CURSOR_ACCEPT:
            result = self._menu.result()
            if self.fsm.state == 'scenario':
                self.scenario = result
                self.readyToStart = True
            elif self.fsm.state == 'multiplayer':
                self.multiplayer = result
                if result:
                    self.fsm.trans('hostGame')
                else:
                    self.fsm.trans('scenario')
            elif self.fsm.state == 'hostGame':
                self.hostGame = result
                if result:
                    self.fsm.trans('scenario')
                else:
                    self.fsm.trans('serverAddress')
        else:
            return False

        if self.readyToStart:
            self.readyToStart = False
            self.fsm.trans('done')
            self._menu.setShowing(False)
            self._label.setText(("Waiting for game to begin..."))
            twistedmain.startGame(server=self.serverAddress,
                                  scenario=self.scenario,
                                  multiplayer=self.multiplayer)
        return True

    def resize(self, (width, height)):
        glViewport(0, 0, width, height)
        menuW, menuH = self._menu.size()
        menuX = width/2 - menuW/2
        menuY = height/2 - menuH/2
        self._menu.setPosn((menuX, menuY))
        self._menu.invalidate()
        self._label.setPosn((menuX, menuY - 30))
        self._label.invalidate()
        self._gmVer.setPosn((2, 2))
        self._gmVer.invalidate()
        self.addressEntry.setPosn((menuX, menuY))

class ScenarioChooserMenu(Sprite.TextMenu):   
    def __init__(self):
        Sprite.TextMenu.__init__(self, (0, 0), 350, 4)
        self.setOptions([])
        self.results = []
        self._showing = True

    def result(self):
        return self.results[self.selectedOption]
        
    def update(self, timeElapsed):
        pass

class ScenarioChooserFSM(FSM.FSM):
    def __init__(self, chooser):
        FSM.FSM.__init__(self, ['multiplayer',
                                'hostGame',
                                'scenario',
                                'serverAddress',
                                'done'])
        self.chooser = chooser
        for s in self.states:
            self.addEntryHook(s, getattr(self, "enter_" + s, self.doNothing))
        self.trans('multiplayer')

    def doNothing(self, *args):
        pass

    def enter_multiplayer(self, *args):
        self.chooser._label.setText(("Choose a game type:"))
        menu = self.chooser._menu
        menu.setOptions([("Single-player"), ("Multi-player")])
        menu.results = [False, True]       
    
    def enter_scenario(self, *args):
        self.chooser._label.setText(("Choose a scenario:"))
        menu = self.chooser._menu
        menu.setOptions([("Randomly Generated"), ("Hill & Ravine"),
                         ("Wall"), ("Castle")])
        menu.results = ["random", "hill-ravine", "wall", "castle"]

    def enter_hostGame(self, *args):
        self.chooser._label.setText(_("Host a game?"))
        menu = self.chooser._menu
        menu.setOptions([_("Host new game"), _("Join existing game")])
        menu.results = [True, False]
        
    def enter_serverAddress(self, *args):
        self.chooser.addressEntry.setEnabled(True)
        self.chooser._label.setText(_("Type in the server address:"))
        menu = self.chooser._menu
        menu.setShowing(False)
        Input.get().setInDialog(True)
