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

PLAYER_FACTION = 0
NPC_HOSTILE_FACTION = 1
NPC_FRIENDLY_FACTION = 2

class Faction(object):
    def __init__(self, id, units):
        self._faction = id
        self._units = units

    def faction(self):
        return self._faction

    def units(self):
        return self._units

def color(factionID):
    if factionID == 0:
        return (0.0, 0.0, 1.0)
    elif factionID == 1:
        return (1.0, 0.0, 0.0)
    else:
        return (0.0, 1.0, 0.0)

def friendly(f1, f2):
    if f1 == PLAYER_FACTION or f1 == NPC_FRIENDLY_FACTION:
        return f2 == PLAYER_FACTION or f2 == NPC_FRIENDLY_FACTION
    else:
        return f2 != PLAYER_FACTION and f2 != NPC_FRIENDLY_FACTION

def hostile(f1, f2):
    if f1 == PLAYER_FACTION or f1 == NPC_FRIENDLY_FACTION:
        return f2 != PLAYER_FACTION and f2 != NPC_FRIENDLY_FACTION
    else:
        return f2 == PLAYER_FACTION or f2 == NPC_FRIENDLY_FACTION

def playerControlled(factionID):
    return factionID == PLAYER_FACTION

def aiControlled(factionID):
    return factionID != PLAYER_FACTION




