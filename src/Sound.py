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


# You may import this module only after the pygame mixer module has
# been initialized.

import Resources
import pygame

_quiet = False
_mixerInit = pygame.mixer.get_init() != None

if _mixerInit:
    _cursorChannel = pygame.mixer.Channel(0)
    _actionChannel = pygame.mixer.Channel(1)
else:
    _quiet = True
    _cursorChannel = None 
    _actionChannel = None

def _play(channel, sound):
    if not _mixerInit:
        return
    if not _quiet and sound != None:
        channel.play(sound)

def setQuiet(quiet):
    global _quiet

    if not _mixerInit:
        return

    _quiet = quiet

    if _quiet:
        pygame.mixer.pause()
        pygame.mixer.music.pause()
    else:
        pygame.mixer.unpause()
        pygame.mixer.music.unpause()


def toggleQuiet():
    setQuiet(not _quiet)


def playMusic(musicName):
    """Changes background music."""
    if not _mixerInit:
        return
    if not _quiet:
        Resources.music(musicName)

def playTune(tuneName):
    """Plays a short tune. Returns whether it was actually played."""
    if _mixerInit and not _quiet:
        Resources.music(tuneName, loop=False)
        return True
    else:
        return False

def cursorClick():
    s = Resources.sound("cursor-click")
    _play(_cursorChannel, s)

def cursorCancel():
    s = Resources.sound("cursor-cancel")
    _play(_cursorChannel, s)

def cursorMove():
    s = Resources.sound("cursor-move")
    _play(_cursorChannel, s)

def cursorInvalid():
    s = Resources.sound("cursor-invalid")
    _play(_cursorChannel, s)

def action(sound):
    s = Resources.sound(sound)
    _play(_actionChannel, s)
    
