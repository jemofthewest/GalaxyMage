# Copyright (C) 2005-2006 Colin McMillen and GalaxyMage contributors.
# See http://www.galaxymage.org/index.php/Credits for full credits.
#
# This file is part of GalaxyMage.
#
# GalaxyMage is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
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

import copy
from twisted.spread import pb

class Range(pb.Copyable, pb.RemoteCopy):
    def __init__(self):
        self._zdiff = 8
    
    def __call__(self, map, unit, (x, y, z)):
        result = self.affectedSquares(map, unit, (x, y, z))
        result = [(x,y) for (x,y) in result
                  if (map.squareExists(x, y) and
                      abs(map.squares[x][y].z - z) <= self._zdiff)]
        return result

    def affectedSquares(self, map, unit, (x, y, z)):
        return []

class Line(Range):
    def __init__(self, length, zdiff=8):
        self._length = length
        self._zdiff = zdiff

    def affectedSquares(self, map, unit, (x, y, z)):
        result = []
        if ((x - unit.x()) < 0 and (y - unit.y()) == 0):
            for i in xrange(0, self._length):
                result.append((x-i, y))
        elif ((x - unit.x()) > 0 and (y - unit.y()) == 0):
            for i in xrange(0, self._length):
                result.append((x+i, y))
        elif ((x - unit.x()) == 0 and (y - unit.y()) < 0):
            for i in xrange(0, self._length):
                result.append((x, y-i))
        elif ((x - unit.x()) == 0 and (y - unit.y()) > 0):
            for i in xrange(0, self._length):
                result.append((x, y+i))
        return result

class Cross(Range):
    def __init__(self, min, max, zdiff=8):
        self._min = min
        self._max = max
        self._zdiff = zdiff

    def affectedSquares(self, map, unit, (x, y, z)):
        result = {}
        for i in xrange(self._min, self._max+1):
            result[(x+i, y)] = True
            result[(x-i, y)] = True
            result[(x, y+i)] = True
            result[(x, y-i)] = True
        result = result.keys()
        return result

class Diamond(Range):
    def __init__(self, min, max, zdiff=8):
        self._min = min
        self._max = max
        self._zdiff = zdiff
        
    def affectedSquares(self, map, unit, (x, y, z)):
        result = {}
        for i in xrange(0, self._max+1):
            for j in xrange(0, self._max+1-i):
                if self._min <= (i+j) <= self._max:
                    result[(x+j,y+i)] = True
                    result[(x+j,y-i)] = True
                    result[(x-j,y+i)] = True
                    result[(x-j,y-i)] = True
        result = result.keys()
        return result

    def __str__(self):
        return "Diamond(%d,%d)" % (self._min, self._max)

class DiamondExtend(Diamond):
    def __init__(self, amount):
        self._amount = amount
        self._zdiff = 0

    def affectedSquares(self, map, unit, (x, y, z)):
        r = copy.copy(unit.attack().rangeObject())
        r._max += self._amount
        self._zdiff = r._zdiff
        return r.affectedSquares(map, unit, (x, y, z))

class Single(Range):
    def affectedSquares(self, map, unit, (x, y, z)):
        return [(x,y)]
        
