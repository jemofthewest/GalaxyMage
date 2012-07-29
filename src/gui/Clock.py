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

# FIXME: rename fields
class Clock(object):
    def __init__(self):
        self.previousFrameTime = time.time()
        self.fps = 0
        self.nFrames = 0
        self.lastFPSUpdate = 0.0
        self.fpsUpdateInterval = 1.0
        self.time = 0.0
        
    def tick(self, frameRate = None):
        if frameRate != None:
            now = time.time()
            timeElapsed = now - self.previousFrameTime
            sleepTime = max(0.0, 1.0 / frameRate - timeElapsed)
            time.sleep(sleepTime)
        now = time.time()
        timeElapsed = now - self.previousFrameTime
        self.nFrames += 1
        if now - self.lastFPSUpdate > self.fpsUpdateInterval:
            self.lastFPSUpdate = now
            self.fps = self.nFrames / self.fpsUpdateInterval
            self.nFrames = 0
        self.previousFrameTime = now
        self.timeElapsed = timeElapsed
        self.time = now
        return self.timeElapsed

    def getFPS(self):
        return self.fps

    def getTime(self):
        return self.time

    def getTimeElapsed(self):
        return self.timeElapsed

_clock = Clock()

def get():
    return _clock
