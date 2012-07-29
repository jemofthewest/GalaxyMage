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
import pygame
import Resources
import Clock
import Sprite
import Sound
from OpenGL.GL import *
from OpenGL.GLU import *
import logging
import platform
import gui.Input as Input
from twisted.internet import reactor
import Main

log = logging.getLogger("gui")

def get():
    """Returns the singleton MainWindow object."""
    return _mainWindow

_mainWindow = None


class MainWindow(object):
    def __init__(self, fullscreen, width):
        """Initializes the main window."""
        global _mainWindow
        _mainWindow = self

        self._input = Input.Input(0)

        self._limitFPS = True

        self._fullscreen = fullscreen
        self._fullscreenSize = self._chooseDisplaySize()
        self._defaultSize = (width, width*3/4)

        if fullscreen:
            self._size = self._fullscreenSize
        else:
            self._size = self._defaultSize
        
        self._fpsDisplayer = Sprite.FPSDisplayer()
        self._delegate = None
        self._soundEnabled = True

        pygame.display.set_icon(Resources.image("icon-32"))
        self._setDisplayMode()
        self._resize()
        self._initOpenGL()

        if self._fullscreen:
            pygame.mouse.set_pos((0, 0))

    def size(self):
        """@return: the size of the main window in pixels, as a pair
        (x, y)."""
        return self._size

    def fps(self):
        return Clock.get().getFPS()

    def update(self):
        self._update()
        reactor.callLater(0, self.update)

    def _update(self):
        """Updates the main window, causing a single new frame to be drawn."""
        # Handle events
        self._handleEvents()

        # If we're minimized or hidden, don't bother doing anything
        if not pygame.display.get_active():
            time.sleep(1.0 / 60.0)
            return

        # Call the FPS clock
        if self._limitFPS:
            Clock.get().tick(60)
        else:
            Clock.get().tick()
        timeElapsed = Clock.get().getTimeElapsed()

        self._input.update(timeElapsed)

        if self._delegate != None:
            self._delegate.update(timeElapsed)

        # Draw FPS on top, if enabled
        self._fpsDisplayer.draw()

        # Swap buffers
        pygame.display.flip()
        
    def setDelegate(self, delegate):
        """Sets the main window's delegate.

        @type delegate: MainWindowDelegate"""
        self._delegate = delegate
        self._delegate.resize(self._size)

    def _chooseDisplaySize(self):
        sizes = pygame.display.list_modes()
        usableSizes = []
        for s in sizes:
            if s not in usableSizes:
                usableSizes.append(s)
        usableSizes.sort()
        log.debug("Display sizes detected:")
        log.debug(usableSizes)
        return usableSizes[-1]

    def _setDisplayMode(self):
        videoFlags = pygame.OPENGL|pygame.DOUBLEBUF
        if self._fullscreen:
            videoFlags |= pygame.FULLSCREEN
        else:
            videoFlags |= pygame.RESIZABLE
        pygame.display.set_caption("GalaxyMage %s" % Main.__version__)
        self.screen = pygame.display.set_mode(self._size, videoFlags)
        log.debug("Using display driver %s" % pygame.display.get_driver())
        log.debug("Display info:")
        log.debug(pygame.display.Info())

    def _resize(self):
        (width, height) = self._size
        #pygame.mouse.set_visible(not self._fullscreen)
        if height == 0:
            height = 1
        videoFlags = pygame.OPENGL|pygame.DOUBLEBUF
        if self._fullscreen:
            videoFlags |= pygame.FULLSCREEN
        else:
            videoFlags |= pygame.RESIZABLE
        if platform.system() == "Linux":
            self.screen = pygame.display.set_mode(self._size, videoFlags)
        self._fpsDisplayer.invalidate()
        if self._delegate != None:
            self._delegate.resize(self._size)
        
    def _initOpenGL(self):
        log.debug('OpenGL version: ' + glGetString(GL_VERSION))
        log.debug('OpenGL renderer: ' + glGetString(GL_VENDOR) + " " +
                 glGetString(GL_RENDERER))
        log.debug('OpenGL extensions: ' + glGetString(GL_EXTENSIONS))
        
        glEnable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    def _handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                event = event.event
            if not self._handleEvent(event):
                if self._delegate != None:
                    self._delegate.handleEvent(event)

    def _handleEvent(self, event):
        if (event.type == pygame.QUIT):
            if reactor.running:
                reactor.stop()
            return True
        if (event.type == Input.FPS):
            self._fpsDisplayer.toggle()
            self._limitFPS = not self._limitFPS
            return True
        if (event.type == Input.TOGGLE_SOUND):
            Sound.toggleQuiet()
            return True
        if (event.type == Input.TOGGLE_FULLSCREEN):
            if platform.system() != "Linux":
                return True
            self._fullscreen = not self._fullscreen
            if self._fullscreen:
                self._size = self._fullscreenSize
            else:
                self._size = self._defaultSize
            self._resize()
            return True
        if (event.type == pygame.VIDEORESIZE):
            self._size = event.size
            self._defaultSize = event.size
            self._resize()
            return True
        return False

class MainWindowDelegate(object):
    def update(self, timeElapsed):
        """Update the delegate.

        timeElapsed is the approximate amount of time (in seconds)
        that has elapsed since the last time the delegate was updated.
        Typically, update() will cause the delegate to update any
        relevant game objects and then redraw the latest frame to the
        screen."""
        pass

    def handleEvent(self, event):
        """Takes in an event and returns True if the event was handled
        by the delegate."""
        return False
    
    def resize(self, size):
        """Tells the delegate that a resize event has occurred."""
        pass
    
