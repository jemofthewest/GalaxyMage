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

import Resources
import Light
import Battle
import random
from Faction import PLAYER_FACTION, NPC_FRIENDLY_FACTION, NPC_HOSTILE_FACTION
import engine.Map
from twisted.spread import pb

class Scenario(pb.Copyable, pb.RemoteCopy):
    def __init__(self, map, units, lightEnv, battle, ai, music):
        self._map = map
        self._units = units
        self._lightEnv = lightEnv
        self._battle = battle
        self._ai = ai
        self._music = music

    def map(self):
        return self._map

    def units(self):
        return self._units

    def lightEnvironment(self):
        return self._lightEnv

    def battle(self):
        return self._battle

    def ai(self):
        return self._ai

    def music(self):
        return self._music

    def unitFromID(self, unitID):
        for u in self.units():
            if u.unitID == unitID:
                return u
        return None

def blankMap(map):
    return Scenario(map, [], Light.defaultEnvironment(),
                    Battle.Battle([Battle.NEVER_ENDING], [], map),
                    None,
                    '')

def generateRandom(additionalAIUnits):
    def generateUnit(faction):
        unitTemplates = ['archer1', 'fighter1', 'defender1',
                         'rogue1', 'healer1', 'mage1']
        unitTemplate = random.choice(unitTemplates)
        u = Resources.unit(unitTemplate)
        u.setFaction(faction)
        #u.setFaction(0)
        return u

    def generateMapAndUnits():
        map_ = Resources.map('random')
        units = []
        nUnits = random.randint(4, 8)
        startColumn = random.randint(0, map_.width - (nUnits + 1) / 2)
        for i in xrange(0, nUnits):
            u = generateUnit(PLAYER_FACTION)
            if i < nUnits / 2:
                row = map_.height-1
                column = startColumn + i
            else:
                row = map_.height-2
                column = startColumn + (i - nUnits/2)
            map_.squares[column][row].setUnit(u)
            units.append(u)
        nUnits += additionalAIUnits
        startColumn = random.randint(0, map_.width - (nUnits + 1) / 2)
        for i in xrange(0, nUnits):
            u = generateUnit(NPC_HOSTILE_FACTION)
            if i < nUnits / 2:
                row = 0
                column = startColumn + i
            else:
                row = 1
                column = startColumn + (i - nUnits/2)
            map_.squares[column][row].setUnit(u)
            units.append(u)
        return (map_, units)

    def verifyMap(map_, units):
        for unit in units:
            map_.fillDistances(unit, unit.posn())
            for other in units:
                (x, y) = other.posn()
                if map_.squares[x][y].search == None:
                    return False
        return True

    validMap = False
    while not validMap:
        (map_, units) = generateMapAndUnits()
        validMap = verifyMap(map_, units)

    endingConditions = [Battle.PLAYER_DEFEATED,
                        Battle.DEFEAT_ALL_ENEMIES]
    battle = Battle.Battle(endingConditions, units, map_)

    lighting = Light.randomEnvironment(map_.width, map_.height)

    music = random.choice(['barbieri-lyta',
                           'barbieri-battle',
                           'barbieri-army-march'])
    
    return Scenario(map_, units, lighting,
                    battle, None, music)

class ScenarioIO(object):
    def load(scenarioFilename):
        scenarioFile = file(scenarioFilename, "rU")
        scenarioText = scenarioFile.read()
        scenarioFile.close()

        globalVars = {}
        localVars = {}

        module = compile("from engine.Unit import numpy.oldnumeric.ma as MALE, FEMALE, NEUTER",
                         "Unit.py", "exec")
        eval(module, globalVars)
        module = compile("from engine.Faction import Faction",
                         "Faction.py", "exec")
        eval(module, globalVars)
        
        for m in ["Light", "Battle"]:
            module = compile("import engine.%s as %s" % (m, m), m, "exec")
            eval(module, globalVars)       
        compiled = compile(scenarioText, scenarioFilename, 'exec')

        eval(compiled, globalVars, localVars)
        scenarioData = localVars
        
        if scenarioData['VERSION'] != 1:
            raise Exception("Scenario version %d not supported" %
                            scenarioData["VERSION"])

        # Required fields: map 
        m = Resources.map(scenarioData['MAP'])

        # Load ending conditions
        endingConditions = [Battle.NEVER_ENDING]
        if scenarioData.has_key('ENDING_CONDITIONS'):
            endingConditions = scenarioData['ENDING_CONDITIONS']

        # Load lights
        if scenarioData.has_key('LIGHTING'):
            lightEnv = scenarioData['LIGHTING']
        else:
            lightEnv = Light.defaultEnvironment()

        # Load units
        units = []
        if scenarioData.has_key('FACTIONS'):
            for f in scenarioData['FACTIONS']:
                faction = f.faction()
                for u in f.units():
                    (unitFile, (x, y)) = u
                    u = Resources.unit(unitFile)
                    m.squares[x][y].setUnit(u)
                    u.setFaction(faction)
                    units.append(u)

        # Music
        music = 'barbieri-battle'
        if scenarioData.has_key('MUSIC'):
            music = scenarioData['MUSIC']

        # Create battle
        battle = Battle.Battle(endingConditions, units, m)
   
        return Scenario(m, units, lightEnv, battle, None, music)

    load = staticmethod(load)

