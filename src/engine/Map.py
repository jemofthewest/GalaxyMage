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
import cPickle
import gzip
import re
import random
import Faction
from OpenGL.GL import *
from twisted.spread import pb

class MapSquare(pb.Copyable, pb.RemoteCopy):
    def __init__(self, x, y, zBase, cornerHeights, color, smooth,
                 tag, waterHeight, waterColor):
        # Find our z offset
        self.cornerHeights = cornerHeights
        self.x = x
        self.y = y
        self.z = zBase
        self.unit = None
        self.guiData = {}
#        self.texture = texture
        self.color = color
        self.cornerColors = [[color[0], color[0], color[0], color[0]],
                             [color[1], color[1], color[1], color[1]],
                             [color[2], color[2], color[2], color[2]],
                             [color[3], color[3], color[3], color[3]],
                             [color[4], color[4], color[4], color[4]]]
        self.smooth = smooth
        self.tag = tag
        self.waterHeight = waterHeight
        self.waterColor = waterColor
        self.smoothed = []
        self.search = None

    def minHeight(self):
        return min(self.z,
                   self.z + self.cornerHeights[0],
                   self.z + self.cornerHeights[1],
                   self.z + self.cornerHeights[2],
                   self.z + self.cornerHeights[3])

    def maxHeight(self):
        return max(self.z,
                   self.z + self.cornerHeights[0],
                   self.z + self.cornerHeights[1],
                   self.z + self.cornerHeights[2],
                   self.z + self.cornerHeights[3])

    def setUnit(self, u):
        if self.unit != None:
            raise Exception("Unit was moved into a map square that " + 
                            "already has a unit!")
        self.unit = u
        u.setPosn(self.x, self.y, self.z)

    def posn2d(self):
        return (self.x, self.y)

    def posn(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return "(%d,%d,%d)" % (self.x, self.y, self.z)
    
    # Added for GuiMapEditor
#    def texture(self):
#        return self.guiData['texture']
    
#    def color(self):
#        return self.guiData['color']
    
    def height(self):
        return self.z
   
    def texture(self):
        if self.tag.has_key('texture'):
            tex = self.tag['texture']
            if type(tex) == type(''):
                return [tex,tex,tex,tex,tex]
            elif type(tex) == type([]):
                if len(tex) == 1:
                    return [tex[0],tex[0],tex[0],tex[0],tex[0]]
                elif len(tex) == 2:
                    return [tex[0],tex[1],tex[1],tex[1],tex[1]]
                elif len(tex) ==5:
                    return [tex[0],tex[1],tex[2],tex[3],tex[4]]
                else:
                    pass #log? raise exception?
            else:
                return "none"

#    def color(self):
#        return self.tag['color']
    
    def tagName(self):
        if self.tag.has_key('texture'):
            return self.tag['name']
        return ''


    # FIXME: do smoothing here so we don't have to
    #         smooth the entire map on edits
    def setTag(self,tag = None):
        if tag == None:
            tag = self.tag
        else:
            self.tag = tag

        #color list: Top, Left, Back, Right, Front.
        [(tr, tg, tb, ta),
         (lr, lg, lb, la),
         (br, bg, bb, ba),
         (rr, rg, rb, ra),
         (fr, fg, fb, fa)] = [(1.0, 1.0, 1.0, 1.0),
                              (1.0, 1.0, 1.0, 1.0),
                              (1.0, 1.0, 1.0, 1.0),
                              (1.0, 1.0, 1.0, 1.0),
                              (1.0, 1.0, 1.0, 1.0)]
        #variance list: Top, Left, Back, Right, Front
        [(vtr, vtg, vtb, vta),
         (vlr, vlg, vlb, vla),
         (vbr, vbg, vbb, vba),
         (vrr, vrg, vrb, vra),
         (vfr, vfg, vfb, vfa)] = [(0.0, 0.0, 0.0, 0.0),
                                  (0.0, 0.0, 0.0, 0.0),
                                  (0.0, 0.0, 0.0, 0.0),
                                  (0.0, 0.0, 0.0, 0.0),
                                  (0.0, 0.0, 0.0, 0.0)]

         
        if tag.has_key("color"):
            c = tag["color"]
            if type(c) == type(()): #check for old format
                if len(c) == 3:
                    [(tr, tg, tb),
                     (lr, lg, lb),
                     (br, bg, bb),
                     (rr, rg, rb),
                     (fr, fg, fb)] = [c,c,c,c,c]
                elif len(c) == 4:
                    [(tr, tg, tb, ta),
                     (lr, lg, lb, la),
                     (br, bg, bb, ba),
                     (rr, rg, rb, ra),
                     (fr, fg, fb, fa)] = [c,c,c,c,c]
                        
            elif type(c) == type([]): #under the new format, Top, Left, Back, Right, Front.
                if len(c[0]) == 3:
                    if len(c) == 1:
                        [(tr, tg, tb),
                         (lr, lg, lb),
                         (br, bg, bb),
                         (rr, rg, rb),
                         (fr, fg, fb)] = [c[0],c[0],c[0],c[0],c[0]] #only one member makes all sides that color
                    if len(c) == 2:
                        [(tr, tg, tb),
                         (lr, lg, lb),
                         (br, bg, bb),
                         (rr, rg, rb),
                         (fr, fg, fb)] = [c[0],c[1],c[1],c[1],c[1]] #two members makes the top the first
                    if len(c) == 5:                                 #and the rest the second color
                        [(tr, tg, tb),
                         (lr, lg, lb),
                         (br, bg, bb),
                         (rr, rg, rb),
                         (fr, fg, fb)] = [c[0],c[1],c[2],c[3],c[4]] #the other option is to specify all 5.
                elif len(c[0]) == 4:
                    if len(c) == 1:
                        [(tr, tg, tb, ta),
                         (lr, lg, lb, la),
                         (br, bg, bb, ba),
                         (rr, rg, rb, ra),
                         (fr, fg, fb, fa)] = [c[0],c[0],c[0],c[0],c[0]] #same as above
                    if len(c) == 2:
                        [(tr, tg, tb, ta),
                         (lr, lg, lb, la),
                         (br, bg, bb, ba),
                         (rr, rg, rb, ra),
                         (fr, fg, fb, fa)] = [c[0],c[1],c[1],c[1],c[1]]
                    if len(c) == 5:
                        [(tr, tg, tb, ta),
                         (lr, lg, lb, la),
                         (br, bg, bb, ba),
                         (rr, rg, rb, ra),
                         (fr, fg, fb, fa)] = [c[0],c[1],c[2],c[3],c[4]]
                                
                                
            else:
                pass  #log? raise exception?

        if tag.has_key("colorVar"):
            c = tag["colorVar"]
            if type(c) == type(()): #check for old format
                if len(c) == 3:
                    [(vtr, vtg, vtb),
                     (vlr, vlg, vlb),
                     (vbr, vbg, vbb),
                     (vrr, vrg, vrb),
                     (vfr, vfg, vfb)] = [c,c,c,c,c]
                elif len(c) == 4:
                    [(vtr, vtg, vtb, vta),
                     (vlr, vlg, vlb, vla),
                     (vbr, vbg, vbb, vba),
                     (vrr, vrg, vrb, vra),
                     (vfr, vfg, vfb, vfa)] = [c,c,c,c,c]
                        
            elif type(c) == type([]): #under the new format, Top, Left, Back, Right, Front.  
                if len(c[0]) == 3:
                    if len(c) == 1:
                        [(vtr, vtg, vtb),
                         (vlr, vlg, vlb),
                         (vbr, vbg, vbb),
                         (vrr, vrg, vrb),
                         (vfr, vfg, vfb)] = [c[0],c[0],c[0],c[0],c[0]] #only one member makes all sides that variance
                    if len(c) == 2:
                        [(vtr, vtg, vtb),
                         (vlr, vlg, vlb),
                         (vbr, vbg, vbb),
                         (vrr, vrg, vrb),
                         (vfr, vfg, vfb)] = [c[0],c[1],c[1],c[1],c[1]] #two members makes the top the first
                    if len(c) == 5:                                    #and the rest the second variance
                        [(vtr, vtg, vtb),
                         (vlr, vlg, vlb),
                         (vbr, vbg, vbb),
                         (vrr, vrg, vrb),
                         (vfr, vfg, vfb)] = [c[0],c[1],c[2],c[3],c[4]] #the other option is to specify all 5.
                elif len(c[0]) == 4:
                    if len(c) == 1:
                        [(vtr, vtg, vtb, vta),
                         (vlr, vlg, vlb, vla),
                         (vbr, vbg, vbb, vba),
                         (vrr, vrg, vrb, vra),
                         (vfr, vfg, vfb, vfa)] = [c[0],c[0],c[0],c[0],c[0]] #same as above
                    if len(c) == 2:
                        [(vtr, vtg, vtb, vta),
                         (vlr, vlg, vlb, vla),
                         (vbr, vbg, vbb, vba),
                         (vrr, vrg, vrb, vra),
                         (vfr, vfg, vfb, vfa)] = [c[0],c[1],c[1],c[1],c[1]]
                    if len(c) == 5:
                        [(vtr, vtg, vtb, vta),
                         (vlr, vlg, vlb, vla),
                         (vbr, vbg, vbb, vba),
                         (vrr, vrg, vrb, vra),
                         (vfr, vfg, vfb, vfa)] = [c[0],c[1],c[2],c[3],c[4]]
                                
                                
            else:
                pass  #log? raise exception?

        self.color = [(tr - random.random() * vtr,tg - random.random() * vtg,tb - random.random() * vtb,ta - random.random() * vta),
                     (lr - random.random() * vlr,lg - random.random() * vlg,lb - random.random() * vlb,la - random.random() * vla),
                     (br - random.random() * vbr,bg - random.random() * vbg,bb - random.random() * vbb,ba - random.random() * vba),
                     (rr - random.random() * vrr,rg - random.random() * vrg,rb - random.random() * vrb,ra - random.random() * vra),
                     (fr - random.random() * vfr,fg - random.random() * vfg,fb - random.random() * vfb,fa - random.random() * vfa)]

        self.cornerColors = [[self.color[0], self.color[0], self.color[0], self.color[0]],
                             [self.color[1], self.color[1], self.color[1], self.color[1]],
                             [self.color[2], self.color[2], self.color[2], self.color[2]],
                             [self.color[3], self.color[3], self.color[3], self.color[3]],
                             [self.color[4], self.color[4], self.color[4], self.color[4]]]
        if tag.has_key('waterColor'):
            self.waterColor = tag['waterColor']
       
    def setTexture(self,texture):
        self.tag['texture'] = texture
            
    def setColor(self,color):
        self.tag['color'] = color
        
    def plusHeight(self,height=1):
        self.z += height
        for i in range(0,4):
            self.cornerHeights[i] -= height

    def minusHeight(self,height=1):
        self.z -= height
        for i in range(0,4):
            self.cornerHeights[i] += height
            
#    def setCornerHeight(self,corner,height):
#        self.cornerHeights[corner] = height
    # End added for GuiMapEditor
    
class Map(pb.Copyable, pb.RemoteCopy):
    def __init__(self, width, height, z, tileProperties,
                 globalWaterHeight, globalWaterColor, tags_):
        self._loadString = ""
        self.waterHeight = globalWaterHeight
        self.waterColor = globalWaterColor
        self.tags = tags_
        self.width = width
        self.height = height
        self.squares = []
        for x in xrange(0, width):
            self.squares.append([])
            for y in xrange(0, height):
                props = tileProperties[x,y]
                tag = {}
                if tags_.has_key(props['tag']):
                    tag = tags_[props['tag']]

                #color list: Top, Left, Back, Right, Front.
                [(tr, tg, tb, ta),
                 (lr, lg, lb, la),
                 (br, bg, bb, ba),
                 (rr, rg, rb, ra),
                 (fr, fg, fb, fa)] = [(1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0),
                                      (1.0, 1.0, 1.0, 1.0)]
                #variance list: Top, Left, Back, Right, Front
                [(vtr, vtg, vtb, vta),
                 (vlr, vlg, vlb, vla),
                 (vbr, vbg, vbb, vba),
                 (vrr, vrg, vrb, vra),
                 (vfr, vfg, vfb, vfa)] = [(0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0),
                                          (0.0, 0.0, 0.0, 0.0)]

                texture = "none"
                if tag.has_key("color"):
                    c = tag["color"]
                    if type(c) == type(()): #check for old format
                        if len(c) == 3:
                            [(tr, tg, tb),
                             (lr, lg, lb),
                             (br, bg, bb),
                             (rr, rg, rb),
                             (fr, fg, fb)] = [c,c,c,c,c]
                        elif len(c) == 4:
                            [(tr, tg, tb, ta),
                             (lr, lg, lb, la),
                             (br, bg, bb, ba),
                             (rr, rg, rb, ra),
                             (fr, fg, fb, fa)] = [c,c,c,c,c]
                        
                    elif type(c) == type([]): #under the new format, Top, Left, Back, Right, Front.  
                        if len(c[0]) == 3:
                            if len(c) == 1:
                                [(tr, tg, tb),
                                 (lr, lg, lb),
                                 (br, bg, bb),
                                 (rr, rg, rb),
                                 (fr, fg, fb)] = [c[0],c[0],c[0],c[0],c[0]] #only one member makes all sides that color
                            if len(c) == 2:
                                [(tr, tg, tb),
                                 (lr, lg, lb),
                                 (br, bg, bb),
                                 (rr, rg, rb),
                                 (fr, fg, fb)] = [c[0],c[1],c[1],c[1],c[1]] #two members makes the top the first
                            if len(c) == 5:                                 #and the rest the second color
                                [(tr, tg, tb),
                                 (lr, lg, lb),
                                 (br, bg, bb),
                                 (rr, rg, rb),
                                 (fr, fg, fb)] = [c[0],c[1],c[2],c[3],c[4]] #the other option is to specify all 5.
                        elif len(c[0]) == 4:
                            if len(c) == 1:
                                [(tr, tg, tb, ta),
                                 (lr, lg, lb, la),
                                 (br, bg, bb, ba),
                                 (rr, rg, rb, ra),
                                 (fr, fg, fb, fa)] = [c[0],c[0],c[0],c[0],c[0]] #same as above
                            if len(c) == 2:
                                [(tr, tg, tb, ta),
                                 (lr, lg, lb, la),
                                 (br, bg, bb, ba),
                                 (rr, rg, rb, ra),
                                 (fr, fg, fb, fa)] = [c[0],c[1],c[1],c[1],c[1]]
                            if len(c) == 5:
                                [(tr, tg, tb, ta),
                                 (lr, lg, lb, la),
                                 (br, bg, bb, ba),
                                 (rr, rg, rb, ra),
                                 (fr, fg, fb, fa)] = [c[0],c[1],c[2],c[3],c[4]]
                                
                                
                    else:
                        pass  #log? raise exception?

                if tag.has_key("colorVar"):
                    c = tag["colorVar"]
                    if type(c) == type(()): #check for old format
                        if len(c) == 3:
                            [(vtr, vtg, vtb),
                             (vlr, vlg, vlb),
                             (vbr, vbg, vbb),
                             (vrr, vrg, vrb),
                             (vfr, vfg, vfb)] = [c,c,c,c,c]
                        elif len(c) == 4:
                            [(vtr, vtg, vtb, vta),
                             (vlr, vlg, vlb, vla),
                             (vbr, vbg, vbb, vba),
                             (vrr, vrg, vrb, vra),
                             (vfr, vfg, vfb, vfa)] = [c,c,c,c,c]
                        
                    elif type(c) == type([]): #under the new format, Top, Left, Back, Right, Front.  
                        if len(c[0]) == 3:
                            if len(c) == 1:
                                [(vtr, vtg, vtb),
                                 (vlr, vlg, vlb),
                                 (vbr, vbg, vbb),
                                 (vrr, vrg, vrb),
                                 (vfr, vfg, vfb)] = [c[0],c[0],c[0],c[0],c[0]] #only one member makes all sides that variance
                            if len(c) == 2:
                                [(vtr, vtg, vtb),
                                 (vlr, vlg, vlb),
                                 (vbr, vbg, vbb),
                                 (vrr, vrg, vrb),
                                 (vfr, vfg, vfb)] = [c[0],c[1],c[1],c[1],c[1]] #two members makes the top the first
                            if len(c) == 5:                                    #and the rest the second variance
                                [(vtr, vtg, vtb),
                                 (vlr, vlg, vlb),
                                 (vbr, vbg, vbb),
                                 (vrr, vrg, vrb),
                                 (vfr, vfg, vfb)] = [c[0],c[1],c[2],c[3],c[4]] #the other option is to specify all 5.
                        elif len(c[0]) == 4:
                            if len(c) == 1:
                                [(vtr, vtg, vtb, vta),
                                 (vlr, vlg, vlb, vla),
                                 (vbr, vbg, vbb, vba),
                                 (vrr, vrg, vrb, vra),
                                 (vfr, vfg, vfb, vfa)] = [c[0],c[0],c[0],c[0],c[0]] #same as above
                            if len(c) == 2:
                                [(vtr, vtg, vtb, vta),
                                 (vlr, vlg, vlb, vla),
                                 (vbr, vbg, vbb, vba),
                                 (vrr, vrg, vrb, vra),
                                 (vfr, vfg, vfb, vfa)] = [c[0],c[1],c[1],c[1],c[1]]
                            if len(c) == 5:
                                [(vtr, vtg, vtb, vta),
                                 (vlr, vlg, vlb, vla),
                                 (vbr, vbg, vbb, vba),
                                 (vrr, vrg, vrb, vra),
                                 (vfr, vfg, vfb, vfa)] = [c[0],c[1],c[2],c[3],c[4]]
                                
                                
                    else:
                        pass  #log? raise exception?
                    
                if tag.has_key("texture"):
                    texture = tag["texture"]
                waterHeight = globalWaterHeight
                waterColor = globalWaterColor
                if props.has_key('waterHeight'):
                    waterHeight = props['waterHeight']
                elif tag.has_key('waterHeight'):
                    waterHeight = tag['waterHeight']
                if tag.has_key('waterColor'):
                    waterColor = tag['waterColor']
                smooth = False
                if tag.has_key("smooth"):
                    smooth = tag["smooth"]
                smoothed = False
                if props.has_key("cornerHeights"):
                    cornerHeights = list(props["cornerHeights"])
                    smooth = False
                elif tag.has_key("cornerHeights"):
                    cornerHeights = list(tag["cornerHeights"])
                else:
                    cornerHeights = [0,0,0,0]
                    if smooth and y-1 >= 0:
                        up = self.squares[x][y-1]
                        if up.smooth:
                            smoothed = True
                            cornerHeights[0] = up.z+up.cornerHeights[2]-z[x,y]
                            cornerHeights[1] = up.z+up.cornerHeights[3]-z[x,y]
                    if smooth and x-1 >= 0:
                        left = self.squares[x-1][y]
                        if left.smooth:
                            cornerHeights[2] = left.z+left.cornerHeights[3]-z[x,y]
                            if not smoothed:
                                cornerHeights[0] = left.z+left.cornerHeights[1]-z[x,y]
                            smoothed = True
#                     for i in xrange(4):
#                        if cornerHeights[i] < -8 or cornerHeights[i] > 8:
#                            cornerHeights[i] = 0 # make a step


                c = [(tr - random.random() * vtr,tg - random.random() * vtg,tb - random.random() * vtb,ta - random.random() * vta),
                     (lr - random.random() * vlr,lg - random.random() * vlg,lb - random.random() * vlb,la - random.random() * vla),
                     (br - random.random() * vbr,bg - random.random() * vbg,bb - random.random() * vbb,ba - random.random() * vba),
                     (rr - random.random() * vrr,rg - random.random() * vrg,rb - random.random() * vrb,ra - random.random() * vra),
                     (fr - random.random() * vfr,fg - random.random() * vfg,fb - random.random() * vfb,fa - random.random() * vfa)]
                self.squares[x].append(MapSquare(x, y, z[x,y],
                                                 cornerHeights,
                                                 c,
                                                 smooth, tag,
                                                 waterHeight,
                                                 waterColor))
                
        # Normalize z-heights of smoothed squares a bit, so that the
        # middle of the square is has a z-height in the middle of the
        # corner heights.
        for x in xrange(0, width):
            for y in xrange(0, height):
                sq = self.squares[x][y]
                if not sq.smooth:
                    continue
                ch = list(sq.cornerHeights)
                ch.sort()
                zDiff = (ch[0] + ch[1] + ch[2] + ch[3] + 3) / 4
                sq.z += zDiff
                for i in xrange(0, 4):
                    sq.cornerHeights[i] -= zDiff

        self.smoothColors()
                    
        # If a square doesn't have a water height, but one of its
        # neighbors does, and this square was smoothed, inherit the
        # water height of its neighbor.
        for x in xrange(0, width):
            for y in xrange(0, height):
                sq = self.squares[x][y]
                if sq.waterHeight != 0: # or not sq.smoothed:
                    continue
                highestWater = 0
                waterColor = None
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.waterHeight > highestWater:
                        waterColor = up.waterColor
                        highestWater = up.waterHeight
                if y+1 < self.height:
                    down = self.squares[x][y+1]
                    if down.waterHeight > highestWater:
                        waterColor = down.waterColor
                        highestWater = down.waterHeight
                if x-1 >= 0:
                    left = self.squares[x-1][y]
                    if left.waterHeight > highestWater:
                        waterColor = left.waterColor
                        highestWater = left.waterHeight
                if x+1 < self.width:
                    right = self.squares[x+1][y]
                    if right.waterHeight > highestWater:
                        waterColor = right.waterColor
                        highestWater = right.waterHeight
                if highestWater > 0 and sq.minHeight() < highestWater:
                    sq.waterHeight = highestWater
                    sq.waterColor = waterColor

    def smoothColors(self):
        # Smooth colors between squares with the same tag. The idea is
        # to make the colorVar smooth instead of on a per-square basis.
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                sq = self.squares[x][y]
                #smooth topsides
                smoothedUp = False 
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.tag == sq.tag:
                        smoothedUp = True
                        sq.cornerColors[0][0] = up.cornerColors[0][2]
                        sq.cornerColors[0][1] = up.cornerColors[0][3]
                if x-1 >= 0:
                    left = self.squares[x-1][y]
                    if left.tag == sq.tag:
                        sq.cornerColors[0][2] = left.cornerColors[0][3]
                        if not smoothedUp:
                            sq.cornerColors[0][0] = left.cornerColors[0][1]
                #smooth leftsides
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.tag == sq.tag:
                        sq.cornerColors[1][0] = up.cornerColors[1][1]
                        sq.cornerColors[1][3] = up.cornerColors[1][2]
                #smooth backsides
                if x-1 >= 0:
                    up = self.squares[x-1][y]
                    if up.tag == sq.tag:
                        sq.cornerColors[2][1] = up.cornerColors[2][0]
                        sq.cornerColors[2][2] = up.cornerColors[2][3]
                #smooth rightsides
                if y-1 >= 0:
                    up = self.squares[x][y-1]
                    if up.tag == sq.tag:
                        sq.cornerColors[3][1] = up.cornerColors[3][0]
                        sq.cornerColors[3][2] = up.cornerColors[3][3]
                #smooth backsides
                if x-1 >= 0:
                    up = self.squares[x-1][y]
                    if up.tag == sq.tag:
                        sq.cornerColors[4][0] = up.cornerColors[4][1]
                        sq.cornerColors[4][3] = up.cornerColors[4][2]
        
    def save(self, filename):
        f = open(filename, 'w')
        f.write(self.loadString())

    def getStateToCopy(self):
        return self.loadString()

    def setCopyableState(self, state):
        m = MapIO.loadString("remote map", state)
        self.__dict__.update(m.__dict__)
        
    def setLoadString(self, text):
        self._loadString = text
        
    def loadString(self):
        r = ("VERSION = 1\n\n"
            +"WIDTH = %s\n" % self.width
            +"HEIGHT = %s\n\n" % self.height
            +"WATER_HEIGHT = %d\n" % self.waterHeight
            +"WATER_COLOR = %s\n\n" % repr(self.waterColor)
            +"TILE_PROPERTIES = {\n")
        for tagName in self.tags.keys():
            tag = self.tags[tagName]
            r += "    '%s':\t{\n" % tagName
            for k,v in tag.iteritems():
                if k != "name":
                    r += "\t\t    '%s': %s,\n" % (k, repr(v))
            r = r[:-2] + "\n    },\n"
        r += "}\n\nLAYOUT = '''\n"
        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                sq = self.squares[x][y]
                s = "%d" % sq.height()
                if (((not sq.tag.has_key('cornerHeights')) and
                     sq.cornerHeights != [0, 0, 0, 0]) or
                    (sq.tag.has_key('cornerHeights') and
                     sq.cornerHeights != sq.tag['cornerHeights'])):
                    s += repr(sq.cornerHeights)
                if ((not sq.tag.has_key('waterHeight')) or
                    sq.waterHeight != sq.tag['waterHeight']):
                    s += "wh" + repr(sq.waterHeight)
                s += sq.tagName()
                r += "%-30s" % s
            r += "\n"
        r += "'''\n"
        return r        

    def squareExists(self, x, y):
        return (x >= 0 and y >= 0 and x < self.width and y < self.height)

    def resetSearchCosts(self):
        sq = self.squares
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                sq[x][y].search = None

    def getPotentialConnections(self, square):
        result = []
        (x, y) = (square.x, square.y)
        if x > 0:
            result.append(self.squares[x-1][y])
        if x < self.width - 1:
            result.append(self.squares[x+1][y])
        if y > 0:
            result.append(self.squares[x][y-1])
        if y < self.height - 1:
            result.append(self.squares[x][y+1])
        return result

    def bfs(self, start, expand, visitPredicate, resultPredicate):
        startX = start[0]
        startY = start[1]
        self.resetSearchCosts()
        sq = self.squares
        result = []
        q = [sq[startX][startY]]
        q[0].search = (0, None)
        while len(q) > 0:
            s = q.pop(0)
            if resultPredicate(s):
                result.append(s)
            for newS in expand(s):
                if newS.search == None:
                    newS.search = (s.search[0] + 1, s)
                    if visitPredicate(newS):
                        q.append(newS)
                    else:
                        newS.search = None
        return result

    # FIXME: don't use faction() directly?
    # FIXME: this should be in the AI code, not here
    def closestUnits(self, unit, faction):
        def visit(s):
            connectedOK = (s.search[1] == None or
                           connected(s.search[1], s, unit))
            return connectedOK
        def resultp(s):
            for neighbor in self.getPotentialConnections(s):
                if (neighbor.unit != None and
                    neighbor.unit.faction() == faction and
                    neighbor.unit.alive()):
                    return True
            return False
        start = (unit.x(), unit.y())
        expand = lambda s: self.getPotentialConnections(s)
        result = self.bfs(start, expand, visit, resultp)
        return result
    
    def reachable(self, unit):
        def visit(s):
            costOK = s.search[0] <= unit.move()
            connectedOK = (s.search[1] == None or
                           connected(s.search[1], s, unit))
            return costOK and connectedOK
        start = (unit.x(), unit.y())
        resultp = lambda s: s.unit == None
        expand = lambda s: self.getPotentialConnections(s)
        result = self.bfs(start, expand, visit, resultp)
        return [(s.x, s.y) for s in result]

    def fillDistances(self, unit, posn):
        def visit(s):
            connectedOK = (s.search[1] == None or
                           connectedIgnoringUnits(s.search[1], s, unit))
            return connectedOK
        start = posn
        resultp = lambda s: s.unit == None
        expand = lambda s: self.getPotentialConnections(s)
        self.bfs(start, expand, visit, resultp)

    def shortestPath(self, targetX, targetY):
        sq = self.squares
        result = [sq[targetX][targetY]]
        while result[-1].search[0] != 0:
            (cost, prev) = result[-1].search
            result.append(prev)
        return result

    def changeCorner(self, x, y, corner, change):
        sq = self.squares[x][y]
        getDiag = False
        
        if sq.tag.has_key('smooth') and sq.tag['smooth'] == True:
            # find the corner's neighbors: (x,y),(x,y+dy),(x+dx,y),(x+dx,y+dy)
            dx = 1
            dy = 1
            if corner < 2:
                dy = -1
            if corner % 2 == 0:
                dx = -1
                    
            # move them along with us if they match up (same tag, height)
            if self.squareExists(x,y+dy):
                nb = self.squares[x][y+dy]
                if (nb.tag == sq.tag and
                    nb.cornerHeights[corner-2*dy] + nb.height() ==
                    sq.cornerHeights[corner] + sq.height()):
                    getDiag = True
                    nb.cornerHeights[corner-2*dy] += change
            if self.squareExists(x+dx,y):
                nb = self.squares[x+dx][y]
                if (nb.tag == sq.tag and
                    nb.cornerHeights[corner-dx] + nb.height() ==
                    sq.cornerHeights[corner] + sq.height()):
                    getDiag = True
                    nb.cornerHeights[corner-dx] += change
            if getDiag == True and self.squareExists(x+dx,y+dy):
                nb = self.squares[x+dx][y+dy]
                if (nb.tag == sq.tag and
                    nb.cornerHeights[3-corner] + nb.height() ==
                    sq.cornerHeights[corner] + sq.height()):
                    nb.cornerHeights[3-corner] += change
        sq.cornerHeights[corner] += change

    def index(self, x, y):
        return y * self.width + x

    def __repr__(self):
	result = ''
        sq = self.squares
        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                result = result + '%s ' % sq[x][y].z
            result = result + '\n'
	return result
   
class MapIO(object):

    def load(mapname):
        mapfile = file(mapname, 'rU')
        text = mapfile.read()
        mapfile.close()
        return MapIO.loadString(mapname, text)
    
    def loadString(mapname, text):
        compiled = compile(text, mapname, 'exec')
        localVars = {}
        eval(compiled, {}, localVars)
        mapData = localVars

        if mapData["VERSION"] != 1:
            raise "Map version %d not supported" % mapData["VERSION"]
        width = mapData['WIDTH']
        height = mapData['HEIGHT']
#        tilePropertiesTemplate = {}
        waterHeight = 0
        waterColor = [0.3, 0.3, 0.6]
        if mapData.has_key('WATER_HEIGHT'):
            waterHeight = mapData['WATER_HEIGHT']
        if mapData.has_key('WATER_COLOR'):
            waterColor = mapData['WATER_COLOR']
        if mapData.has_key('TILE_PROPERTIES'):
            tags = mapData['TILE_PROPERTIES']
            for k in tags.keys():
                tags[k]['name'] = k
                if not tags[k].has_key('waterColor'):
                    tags[k]['waterColor'] = waterColor
                if not tags[k].has_key('waterHeight'):
                    tags[k]['waterHeight'] = waterHeight
        else:
            tags = {}
        layoutLines = mapData['LAYOUT'].split('\n')
        layoutLines.pop(0)
        zdata = Numeric.zeros((width, height))
        tileProperties = Numeric.zeros((width, height), Numeric.PyObject)
        y = 0
        for line in layoutLines:
            if re.match(re.compile(r'^\s*$'), line):
                continue
            tiles = re.split(re.compile(r'\s+(?!-?\d+,)(?!-?\d+\])'), line)
            for x in xrange(0, width):
                tileData = tiles[x]
                tileProperties[x,y] = {}
                m = re.match(re.compile(
                    r'(\d+)(\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\])?(wh(\d+))?(\w*)'), tileData)
                zdata[x,y] = int(m.group(1))
                tileProperties[x,y]['tag'] = m.group(9)
                if m.group(2) != None:
                    tileProperties[x,y]['cornerHeights'] = [int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6))]
                if m.group(7) != None:
                    tileProperties[x,y]['waterHeight'] = int(m.group(8))
            y += 1
        m = Map(width, height, zdata, tileProperties, waterHeight, waterColor, tags)
        m.setLoadString(text)
        return m

    load = staticmethod(load)
    loadString = staticmethod(loadString)

def connectedIgnoringUnits(sq1, sq2, unit):
    return connected(sq1, sq2, unit, True)

def connected(sq1, sq2, unit, ignoreUnits=False):
    if not ignoreUnits:
        if (sq2.unit != None and
            sq2.unit.alive() and
            not Faction.friendly(unit.faction(), sq2.unit.faction())):
            return False
    if sq1 is sq2:
        return False
    if sq1.z == 0 or sq2.z == 0:
        return False
    if sq1.z + 4 < sq1.waterHeight or sq2.z + 4 < sq2.waterHeight:
        return False
#    if sq1.maxHeight() - sq1.minHeight() > 16:
#        return False
#    if sq2.maxHeight() - sq2.minHeight() > 16:
#        return False
    result = abs(sq1.z - sq2.z) <= unit.jump()
    return result

