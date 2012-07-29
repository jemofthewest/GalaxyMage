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

import Faction
import engine.Equipment as Equipment
from twisted.spread import pb

# FIXME: move these variables into Faction?
FRIENDLY = 0
HOSTILE = 1
FRIENDLY_AND_HOSTILE = 2

# Ability types -- right now there are only action abilities
ACTION = 0

# If an ability's sound is set to WEAPON_SOUND, it will use the sound
# of the user's weapon.
WEAPON_SOUND = 0

class Ability(pb.Copyable, pb.RemoteCopy):
    nextID = 0
    get = {}

    def setCopyableState(self, state):
        pb.RemoteCopy.setCopyableState(self, state)
        Ability.get[self.abilityID] = self
    
    def __init__(self, name, description, cost, targetType,
                 requiredWeapons,
                 range, aoe, effects, sound):
        self.abilityID = Ability.nextID
        Ability.nextID += 1
        Ability.get[self.abilityID] = self
        self._name = name
        self._cost = cost
        self._range = range
        self._aoe = aoe
        self._targetType = targetType
        self._effects = effects
        self._sound = sound
        self._description = description
        self._requiredWeapons = requiredWeapons

    def description(self):
        return self._description

    def sound(self, weaponAbility):
        if self._sound == WEAPON_SOUND:
            return weaponAbility.sound(weaponAbility)
        return self._sound

    def targetType(self):
        return self._targetType

    def range(self, map, sourceUnit):
        return self._range(map, sourceUnit, sourceUnit.posn3d())

    def rangeObject(self):
        return self._range

    def requiredWeapons(self):
        return self._requiredWeapons

    def aoe(self, map, sourceUnit, posn):
        if len(posn) == 2:
            (x, y) = posn
            z = map.squares[x][y].z
        else:
            (x, y, z) = posn
        return self._aoe(map, sourceUnit, (x, y, z))

    def correctWeapon(self, weapon):
        if not self._requiredWeapons:
            return True
        return weapon.weaponType() in self._requiredWeapons
    
    def hasEffect(self, map, sourceUnit, posn):
        return len(self.affectedUnits(map, sourceUnit, posn)) > 0

    def affectedUnits(self, map, sourceUnit, posn):
        if sourceUnit.sp() < self._cost:
            return []
        if not self.correctWeapon(sourceUnit.weapon()):
            return []
            
        if len(posn) == 2:
            (x, y) = posn
            z = map.squares[x][y].z
        else:
            (x, y, z) = posn
        affectedSquares = self._aoe(map, sourceUnit, (x, y, z))
        result = []
        for (x, y) in affectedSquares:
            sq = map.squares[x][y]
            t = sq.unit
            if t != None:
                if self._targetType == FRIENDLY_AND_HOSTILE:
                    result.append(t)
                elif (self._targetType == FRIENDLY and
                      Faction.friendly(sourceUnit.faction(), t.faction())):
                    result.append(t)
                elif (self._targetType == HOSTILE and
                      Faction.hostile(sourceUnit.faction(), t.faction())):
                    result.append(t)                    
        return result
    
    def effects(self):
        return self._effects

    def cost(self):
        return self._cost

    def name(self):
        return self._name
    
    def __str__(self):
        return self.name()

    def __repr__(self):
        return self.name()

