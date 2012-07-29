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
import logging

logger = logging.getLogger("gui")

CURSOR_UP = pygame.USEREVENT + 1
CURSOR_DOWN = pygame.USEREVENT + 2
CURSOR_LEFT = pygame.USEREVENT + 3
CURSOR_RIGHT = pygame.USEREVENT + 4
CURSOR_ACCEPT = pygame.USEREVENT + 5
CURSOR_CANCEL = pygame.USEREVENT + 6
LOWER_CAMERA = pygame.USEREVENT + 7
RAISE_CAMERA = pygame.USEREVENT + 8
ROTATE_CAMERA_CW = pygame.USEREVENT + 9
ROTATE_CAMERA_CCW = pygame.USEREVENT + 10
ROTATE_CAMERA = pygame.USEREVENT + 11
PITCH_CAMERA = pygame.USEREVENT + 12
TRANSLATE_CAMERA = pygame.USEREVENT + 13
RAISE_TILE = pygame.USEREVENT + 14
LOWER_TILE = pygame.USEREVENT + 15
RAISE_CENTER = pygame.USEREVENT + 16
LOWER_CENTER = pygame.USEREVENT + 17
RAISE_B_BL_CORNER = pygame.USEREVENT + 18
RAISE_L_FL_CORNER = pygame.USEREVENT + 20
RAISE_F_FR_CORNER = pygame.USEREVENT + 21
RAISE_R_BR_CORNER = pygame.USEREVENT + 19
LOWER_B_BL_CORNER = pygame.USEREVENT + 22
LOWER_L_FL_CORNER = pygame.USEREVENT + 24
LOWER_F_FR_CORNER = pygame.USEREVENT + 25
LOWER_R_BR_CORNER = pygame.USEREVENT + 23
RAISE_WATER = pygame.USEREVENT + 26
LOWER_WATER = pygame.USEREVENT + 27
FPS = pygame.USEREVENT + 28
TOGGLE_SOUND = pygame.USEREVENT + 29
TOGGLE_FULLSCREEN = pygame.USEREVENT + 30
UNDO = pygame.USEREVENT + 31
START_CHAT = pygame.USEREVENT + 32

_input = None

def get():
    return _input

class Event(object):
    def __init__(self, type_, data):
        self.type = type_
        self.__dict__.update(data)

def postUserEvent(type_, data={}):
    e = Event(type_, data)
    pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                         {'event': e}))

class Input(object):

    def __init__(self, joystickID):
        global _input
        _input = self
        
        self._repeatDelay = 0.5     # seconds
        self._repeatInterval = 0.05 # seconds

        self.inDialog = False
        self._eventRepeatTime = {}
        self._joystick = None
        if pygame.joystick.get_count() > joystickID:
            self._joystick = pygame.joystick.Joystick(joystickID)
            self._joystick.init()
            logger.debug(("Initialized joystick %d " +
                          "(buttons: %d, hats: %d, axes: %d)")
                         % (self._joystick.get_id(),
                            self._joystick.get_numbuttons(),
                            self._joystick.get_numhats(),
                            self._joystick.get_numaxes()))


    def joyButton(self, number):
        if self._joystick == None or self._joystick.get_numbuttons() <= number:
            return False
        return self._joystick.get_button(number)

    def joyHat(self, number, axis):
        if self._joystick == None or self._joystick.get_numhats() <= number:
            return 0
        hat = self._joystick.get_hat(number)
        return hat[axis]

    def joyAxis(self, number):
        if self._joystick == None or self._joystick.get_numaxes() <= number:
            return 0.0
        return self._joystick.get_axis(number)
    
    def setInDialog(self, inDialog):
        self.inDialog = inDialog
        if inDialog:
            pygame.key.set_repeat(300,100)
        else:
            pygame.key.set_repeat()
            for button in self._eventRepeatTime:
                self._eventRepeatTime[button] = self._repeatDelay

    def update(self, timeElapsed):
        if not self.inDialog:
            self.updateGuiEvents(timeElapsed)
        
    def updateGuiEvents(self, timeElapsed):
        keysPressed = pygame.key.get_pressed()
        mousePressed = pygame.mouse.get_pressed()
        mouseMotion = pygame.mouse.get_rel()
        
        # Generate events that are subject to repeat
        self.buttonPressed(timeElapsed,
                           START_CHAT,
                           keysPressed[pygame.K_t])        
        self.buttonPressed(timeElapsed,
                           FPS,
                           keysPressed[pygame.K_f])
        self.buttonPressed(timeElapsed,
                           TOGGLE_SOUND,
                           keysPressed[pygame.K_s])
        self.buttonPressed(timeElapsed,
                           TOGGLE_FULLSCREEN,
                           keysPressed[pygame.K_F12])
        self.buttonPressed(timeElapsed,
                           CURSOR_UP,
                           keysPressed[pygame.K_UP] or
                           self.joyAxis(5) < -0.8 or
                           self.joyHat(0, 1) == 1)
        self.buttonPressed(timeElapsed,
                           CURSOR_DOWN,
                           keysPressed[pygame.K_DOWN] or
                           self.joyAxis(5) > 0.8 or
                           self.joyHat(0, 1) == -1)
        self.buttonPressed(timeElapsed,
                           CURSOR_LEFT,
                           keysPressed[pygame.K_LEFT] or
                           self.joyAxis(4) < -0.8 or
                           self.joyHat(0, 0) == -1)
        self.buttonPressed(timeElapsed,
                           CURSOR_RIGHT,
                           keysPressed[pygame.K_RIGHT] or
                           self.joyAxis(4) > 0.8 or
                           self.joyHat(0, 0) == 1)
        self.buttonPressed(timeElapsed,
                           CURSOR_ACCEPT,
                           keysPressed[pygame.K_RETURN] or
                           self.joyButton(1))
        self.buttonPressed(timeElapsed,
                           CURSOR_CANCEL,
                           keysPressed[pygame.K_ESCAPE] or
                           self.joyButton(2))
        self.buttonPressed(timeElapsed,
                           LOWER_CAMERA,
                           keysPressed[pygame.K_PAGEUP] or
                           self.joyButton(6))
        self.buttonPressed(timeElapsed,
                           RAISE_CAMERA,
                           keysPressed[pygame.K_PAGEDOWN] or
                           self.joyButton(7))
        self.buttonPressed(timeElapsed,
                           ROTATE_CAMERA_CCW,
                           keysPressed[pygame.K_LEFTBRACKET] or
                           keysPressed[pygame.K_HOME] or
                           self.joyButton(4))
        self.buttonPressed(timeElapsed,
                           ROTATE_CAMERA_CW,
                           keysPressed[pygame.K_RIGHTBRACKET] or
                           keysPressed[pygame.K_END] or
                           self.joyButton(5))
        self.buttonPressed(timeElapsed,
                           RAISE_TILE,
                           keysPressed[pygame.K_EQUALS])
        self.buttonPressed(timeElapsed,
                           LOWER_TILE,
                           keysPressed[pygame.K_MINUS])
        self.buttonPressed(timeElapsed,
                           RAISE_CENTER,
                           (keysPressed[pygame.K_s] and not
                            (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT])))
        self.buttonPressed(timeElapsed,
                           LOWER_CENTER,
                           (keysPressed[pygame.K_s] and
                            (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT])))
        self.buttonPressed(timeElapsed,
                           RAISE_B_BL_CORNER,
                           keysPressed[pygame.K_w] and not
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           RAISE_L_FL_CORNER,
                           keysPressed[pygame.K_a] and not
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           RAISE_F_FR_CORNER,
                           keysPressed[pygame.K_x] and not
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           RAISE_R_BR_CORNER,
                           keysPressed[pygame.K_d] and not
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           LOWER_B_BL_CORNER,
                           keysPressed[pygame.K_w] and
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           LOWER_L_FL_CORNER,
                           keysPressed[pygame.K_a] and
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           LOWER_F_FR_CORNER,
                           keysPressed[pygame.K_x] and
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           LOWER_R_BR_CORNER,
                           keysPressed[pygame.K_d] and
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           RAISE_WATER,
                           keysPressed[pygame.K_e] and not
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           LOWER_WATER,
                           keysPressed[pygame.K_e] and
                           (keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RSHIFT]))
        self.buttonPressed(timeElapsed,
                           UNDO,
                           keysPressed[pygame.K_BACKSPACE])

                          
        # Generate misc events

        # Quit
        if keysPressed[pygame.K_q] or self.joyButton(9):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Rotate camera smoothly
        if mousePressed[2] and mouseMotion[0] != 0:
            postUserEvent(ROTATE_CAMERA,
                          {'amount': mouseMotion[0]})
        if abs(self.joyAxis(0)) > 0.8:
            amount = self.joyAxis(0) * timeElapsed * 180.0
            postUserEvent(ROTATE_CAMERA,
                          {'amount': amount})

        # Pitch camera
        if mousePressed[2]:
            postUserEvent(PITCH_CAMERA,
                          {'amount': mouseMotion[1]/3.0})
        if abs(self.joyAxis(1)) > 0.8:
            amount = self.joyAxis(1) * timeElapsed * 90.0
            postUserEvent(PITCH_CAMERA,
                          {'amount': amount})

        # Translate view
        if mousePressed[0]:
            x = mouseMotion[0] / 750.0
            y = mouseMotion[1] / 750.0
            postUserEvent(TRANSLATE_CAMERA,
                          {'amount': (x, y)})
        
        if abs(self.joyAxis(2)) > 0.2 or abs(self.joyAxis(3)) > 0.2:
            (x, y) = (0.0, 0.0)
            if abs(self.joyAxis(2)) > 0.2:
                x = -self.joyAxis(2) * timeElapsed * 0.75
            if abs(self.joyAxis(3)) > 0.2:
                y = -self.joyAxis(3) * timeElapsed * 0.75
            postUserEvent(TRANSLATE_CAMERA,
                          {'amount': (x, y)})


    def buttonPressed(self, timeElapsed, button, pressed):
        if not self._eventRepeatTime.has_key(button):
            self._eventRepeatTime[button] = -1.0
        if pressed:
            generateEvent = False
            oldTime = self._eventRepeatTime[button]
            if oldTime == -1.0:
                generateEvent = True
                self._eventRepeatTime[button] = self._repeatDelay
            elif oldTime <= 0.0:
                generateEvent = True
                self._eventRepeatTime[button] = self._repeatInterval
            else:
                self._eventRepeatTime[button] -= timeElapsed
            if generateEvent:
                postUserEvent(button)
        else:
            self._eventRepeatTime[button] = -1.0
            
