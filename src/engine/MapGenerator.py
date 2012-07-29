## Automatically adapted for numpy.oldnumeric Jul 22, 2012 by 

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

import numpy.oldnumeric as Numeric
import random
import math
import Util
import engine.Map as Map

m = None
mt = None
t = ''

def foreach(filter, op):
    global m, mt
    (w, h) = m.shape
    for i in xrange(0, w):
        for j in xrange(0, h):
            if filter(i, j, m[i,j]):
                old = m[i,j]
                m[i,j] = op(m[i,j])
                if t != None and m[i,j] != old:
                    mt[i,j] = t

def properties(properties):
    global t
    t = properties

# Filter functions
def OutlinedRect(x, y, w, h):
    return lambda sx,sy,sz: ((x <= sx < x+w and (sy == y or sy == y+h-1)) or
                             (y <= sy < y+h and (sx == x or sx == x+w-1)))

def All():
    return lambda sx,sy,sz: True

def FilledRect(x, y, w, h):
    return lambda sx,sy,sz: x <= sx < x+w and y <= sy < y+h

def OutlinedCircle(x, y, radius):
    return lambda sx,sy,sz: abs(x-sx) + abs(y-sy) == radius

def FilledCircle(x, y, radius):
    return lambda sx,sy,sz: (x-sx)*(x-sx) + (y-sy)*(y-sy) <= radius*radius

def Single(x, y):
    return lambda sx,sy,sz: sx == x and sy == y

# Map-transformation functions
def newMap(width, height):
    global m, mt
    m = Numeric.zeros((width, height))     
    mt = Numeric.zeros((width, height), 'O')
    (w, h) = m.shape
    for i in xrange(0, w):
        for j in xrange(0, h):
            mt[i,j] = t
            
def raiseBy(amount, shape):
    foreach(shape, lambda z: z+amount)
   
def raiseTo(height, shape):
    foreach(shape, lambda z: max(height, z))

def lowerTo(height, shape):
    foreach(shape, lambda z: min(height, z))

def setTo(height, shape):
    foreach(shape, lambda z: height)

def erode(amount, minZ, shape):
    foreach(shape, lambda z: max(z - random.randint(0, amount), minZ))

def normalize():
    global m, t
    minval = 1000000
    (w, h) = m.shape
    for i in xrange(0, w):
        for j in xrange(0, h):
            if m[i,j] < minval:
                minval = m[i,j]
    oldT = t
    t = None
    raiseBy(-minval + 4, All())
    t = oldT
    return -minval + 4

def hill(height, steepness, x, y, radius):
    global m
    for r in xrange(0, radius):
        raiseTo(height, FilledCircle(x, y, r))
        height -= steepness

def valley(depth, steepness, x, y, radius):
    global m
    for r in xrange(0, radius):
        lowerTo(depth, OutlinedCircle(x, y, r))
        depth += steepness

def ridge(height, steepness, startX, startY, endX, endY, radius):
    global m
    x = startX
    y = startY
    while x != endX or y != endY:
        hill(height, steepness, x, y, radius)
        dx = endX - x
        dy = endY - y
        if dy == 0:
            moveX = True
        else:
            moveX = random.random() < 1.0*dx/dy
        if moveX:
            x = int(x + Util.sign(dx))
        else:
            y = int(y + Util.sign(dy))

def canyon(height, steepness, startX, startY, endX, endY, radius):
    global m
    x = startX
    y = startY
    while x != endX or y != endY:
        valley(height, steepness, x, y, radius)
        dx = endX - x
        dy = endY - y
        if dy == 0:
            moveX = True
        else:
            moveX = random.random() < 1.0*dx/dy
        if moveX:
            x = int(x + Util.sign(dx))
        else:
            y = int(y + Util.sign(dy))

def river(startX, startY, depth):
    global m, mt, t
    x = startX
    y = startY
    (w, h) = m.shape
    riverSquares = [(startX, startY)]
    direction = None
    while x != 0 and x != w-1 and y != 0 and y != h-1:
        if (x, y-1) in riverSquares:
            pn = 0
        else:
            pn = max(0, m[x, y] - m[x, y-1] + 1)
            if pn > 0:
                pn += 1
        if (x, y+1) in riverSquares:
            ps = 0
        else:
            ps = max(0, m[x, y] - m[x, y+1] + 1)
            if ps > 0:
                ps += 1
        if (x+1, y) in riverSquares:
            pe = 0
        else:
            pe = max(0, m[x, y] - m[x+1, y] + 1)
            if pe > 0:
                pe += 1
        if (x-1, y) in riverSquares:
            pw = 0
        else:
            pw = max(0, m[x, y] - m[x-1, y] + 1)
            if pw > 0:
                pw += 1
        m[x, y] -= depth
        mt[x, y] = t
        riverSquares.append((x, y))
        probs = []
        probs.extend(['n'] * pn)
        probs.extend(['s'] * ps)
        probs.extend(['e'] * pe)
        probs.extend(['w'] * pw)
        if len(probs) == 0:
            break
        direction = random.choice(probs)
        if direction == 'n':
            y -= 1
        elif direction == 's':
            y += 1
        elif direction == 'e':
            x += 1
        elif direction == 'w':
            x -= 1
    if x == 0 or x == w-1 or y == 0 or y == h-1:
        m[x,y] -= depth
    mt[x,y] = t

def save():
    (w, h) = m.shape
    raiseAmount = normalize()
    r = """
VERSION = 1

WIDTH = %d
HEIGHT = %d

WATER_HEIGHT = %d
WATER_COLOR = (0.3, 0.3, 0.7, 0.5)

TILE_PROPERTIES = {
    'grass':  { 'color': (0.5, 0.7, 0.5),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'grass',
                'smooth': True },
    'rock':   { 'color': (0.7, 0.5, 0.3),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'stone',
                'smooth': True,
              },
    'stone':  { 'color': (0.8, 0.8, 0.8),
                'colorVar': (0.1, 0.1, 0.1),
                'texture': 'stone',
                'smooth': False
              },
    'wood':   { 'color': (0.7, 0.7, 0.5),
                'colorVar': (0.05, 0.05, 0.05),
                'texture': 'wood-1',
                'smooth': True },
    'marble': { 'color': (0.6, 0.6, 0.6),
                'colorVar': (0.05, 0.05, 0.05),
                'texture': 'marble-slight',
                'smooth': False},
    }
    
LAYOUT = '''
""" % (w, h, max(0, raiseAmount-random.randint(1,8)))
    for j in xrange(0, h):
        for i in xrange(0, w):
            s = "%d%s " % (m[i,j], mt[i,j])
            r += "%-10s" % s
        r += "\n"
    r += "'''"
    return r


def generateRandom():    
    def addHill(result, (w,h)):
        steepness = random.randint(3, 8)
        radius = random.randint(3, 10)
        height = steepness * radius

        x = random.randrange(0, w)
        y = random.randrange(0, h)
       
        result += "properties('grass')\n"
        result += "hill(height=%d, steepness=%d, x=%d, y=%d, radius=%d)\n" % (
            height, steepness, x, y, radius)
        return result
    
    def addRiver(result, (w,h)):
        depth = random.randint(2, 12)
        x = random.randrange(0, w)
        y = random.randrange(0, h)
        
        result += "properties('grass')\n"
        result += "river(startX=%d, startY=%d, depth=%d)\n" % (
            x, y, depth)
    
        return result
    
    def addBuilding(result, (w,h)):
        zHeight = random.randint(4, 12)
        width = random.randint(2, 4)
        height = random.randint(2, 4)
        x = random.randint(0, w-width)
        y = random.randint(0, h-height)
    
        result += "properties('wood')\n"
        result += "raiseTo(height=%d, shape=FilledRect(%d, %d, %d, %d))\n" % (
            zHeight, x, y, width, height)
    
        return result
    
    def addCastle(result, (w,h)):
        
        zHeight = random.randint(8, 24)
        width = random.randint(5, 10)
        height = random.randint(5, 10)
        x = random.randint(-3, w-3)
        y = random.randint(-3, h-3)
    
        result += "properties('stone')\n"
        # Main walls
        result += "setTo(height=%d, shape=OutlinedRect(%d, %d, %d, %d))\n" % (
            zHeight-1, x, y, width, height)
        result += "setTo(height=%d, shape=OutlinedRect(%d, %d, %d, %d))\n" % (
            zHeight, x, y, width, height)
        # Add higher corners
        result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
            zHeight + 6, x, y)
        result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
            zHeight + 6, x+width-1, y)
        result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
            zHeight + 6, x, y+height-1)
        result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
            zHeight + 6, x+width-1, y+height-1)
        # Make a door
        result += "properties('marble')\n"
        doorChance = 0.5
        if random.random() < doorChance: # north
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+width/2, y)
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+(width-1)/2, y)
        if random.random() < doorChance: # east
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+width-1, y+height/2)
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+width-1, y+(height-1)/2)
        if random.random() < doorChance: # south
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+width/2, y+height-1)
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+(width-1)/2, y+height-1)
        if random.random() < doorChance: # west
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+width-1, y+height/2)      
            result += "setTo(height=%d, shape=Single(%d, %d))\n" % (
                0, x+width-1, y+(height-1)/2)      
            
        # Make the floor marble
        result += "lowerTo(height=%d, shape=FilledRect(%d, %d, %d, %d))\n" % (
            -1, x+1,y+1, width-2, height-2)
        result += "setTo(height=%d, shape=FilledRect(%d, %d, %d, %d))\n" % (
            0, x+1,y+1, width-2, height-2)
    
    
        return result
    
    def makeMap():
        size = (mapWidth, mapHeight) = (random.randint(15,25),
                                        random.randint(15,25))
        #size = (mapWidth, mapHeight) = (8, 8)
        squares = mapWidth * mapHeight
        nHills = random.randint(0, squares / 150 + 1)
        nRivers = random.randint(0, squares / 50 + 1)
        #nRivers = 0
        #nBuildings = random.randint(0, squares / 100 + 1)
        nBuildings = 0
        nCastles = random.randint(0, squares / 600 + 1)
    
    #     print "hills:", nHills
    #     print "rivers:", nRivers
    #     print "buildings:", nBuildings
    #     print "castles:", nCastles
    
        result = ""
        result += "properties('grass')\n"
        result += "newMap(%d,%d)\n" % (mapWidth, mapHeight)
        
        for i in xrange(0, nHills):
            result = addHill(result, size)
    
        result += "properties(None)\n"
        result += "erode(%d, 0, All())\n" % random.randint(2,4)
    
        for i in xrange(0, nRivers):
            result = addRiver(result, size)
    
        for i in xrange(0, nBuildings):
            result = addBuilding(result, size)
    
        for i in xrange(0, nCastles):
            result = addCastle(result, size)
    
        result += "MAP = save()\n"
        return result
    
    data = makeMap()

    globalvars = {}
    localvars = {}
    module = compile("from engine.MapGenerator import *",
                     "MapGenerator.py", "exec")
    eval(module, globalvars)

    compiled = compile(data, "random map", 'exec')
    eval(compiled, globalvars, localvars)

    output = localvars['MAP']

    return Map.MapIO.loadString('random', output)

