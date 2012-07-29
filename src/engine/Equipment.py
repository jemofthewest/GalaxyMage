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

import Resources
from twisted.spread import pb

WEAPON = 0
ARMOR = 1

class Equipment(pb.Copyable, pb.RemoteCopy):
    def __init__(self, name, stats):
        self._name = name
        self._mhp = stats['mhp']
        self._msp = stats['msp']
        self._watk = stats['watk']
        self._wdef = stats['wdef']
        self._matk = stats['matk']
        self._mdef = stats['mdef']
        self._speed = stats['speed']
        self._move = stats['move']
        self._jump = stats['jump']

        # List of sprites
        self._sprites = []

    def name(self):
        return self._name

    def mhp(self):
        return self._mhp

    def msp(self):
        return self._msp
            
    def watk(self):
        return self._watk

    def wdef(self):
        return self._wdef

    def matk(self):
        return self._matk

    def mdef(self):
        return self._mdef  

    def move(self):
        return self._move

    def jump(self):
        return self._jump

    def speed(self):
        return self._speed

    def setSprites(self, sprites):
        self._sprites = sprites
        
    def getSprites(self, spriteName):
        return self._sprites[spriteName]

class Weapon(Equipment):
    HAND = 0
    SWORD = 1
    DAGGER = 2
    STAFF = 3
    MACE = 4
    BOW = 5
    
    def __init__(self, name, stats, type_):
        Equipment.__init__(self, name, stats)
        self._weaponType = type_
        if self._weaponType == Weapon.HAND:
            self._attack = Resources.ability('weapon-hand')
        if self._weaponType == Weapon.SWORD:
            self._attack = Resources.ability('weapon-sword')
        if self._weaponType == Weapon.DAGGER:
            self._attack = Resources.ability('weapon-dagger')
        if self._weaponType == Weapon.STAFF:
            self._attack = Resources.ability('weapon-staff')
        if self._weaponType == Weapon.MACE:
            self._attack = Resources.ability('weapon-mace')
        if self._weaponType == Weapon.BOW:
            self._attack = Resources.ability('weapon-bow')

    def weaponType(self):
        return self._weaponType
    
    def attack(self):
        return self._attack
       
class Armor(Equipment):
    pass

