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

import logging
import pygame
import os
import gui.GLUtil
import re
import engine.Effect as Effect
import engine.Range as Range
import random

logger = logging.getLogger('reso')

# getFilename("images", "arch-mage.png") ->
# "campaigns/common/images/arch-mage.png"
def _getFilename(base, name):
    logger.debug('finding file for (%s, %s)' % (str(base), str(name)))
    sep = os.path.sep
    if sep == '\\':
        sep = r'\\'
    base = re.sub(r'/', sep, base)
    name = re.sub(r'/', sep, name)   
    result = os.path.join("data", campaign, base, name)
    if os.path.exists(result):
        logger.debug('found ' + result)
        return result
    result = os.path.join("data", "extra", base, name)
    if os.path.exists(result):
        logger.debug('found ' + result)
        return result
    result = os.path.join("data", "core", base, name)
    if os.path.exists(result):
        logger.debug('found ' + result)
        return result
    logger.debug('no suitable file found')
    return None

class FontLoader(object):   
    def __init__(self):
        self.fonts = {}
        self.files = { "sans": { False: "vera/Vera.ttf",
                                 True: "vera/VeraBd.ttf"},
                       "serif": { False: "vera/VeraSe.ttf",
                                  True: "vera/VeraSeBd.ttf"},
                       "mono": { False: "vera/VeraMono.ttf",
                                 True: "vera/VeraMoBd.ttf"}}

    def __call__(self, family="sans", size=16, bold=True):
        key = (family, size, bold)
        if not self.fonts.has_key(key):
            if not self.files.has_key(family):
                raise Exception('Font family should be "sans", "serif"' +
                                ', or "mono"')
            filename = self.files[family][bold]
            fontFile = _getFilename("fonts", filename)
            if fontFile == None:
                raise Exception('Font file "%s" not found' % filename)
            f = pygame.font.Font(fontFile, size)
            self.fonts[key] = f
        return self.fonts[key]

class MapLoader(object):
    def __call__(self, mapName):
        import engine.Map as Map
        if mapName == 'random':
            import engine.MapGenerator as MapGenerator
            return MapGenerator.generateRandom()
        if (not '/' in mapName) and (not '.' in mapName):
            filename = mapName + ".py"
            mapName = _getFilename("maps", filename)
        if mapName == None:
            raise Exception('Map file "%s" not found' % filename)
        return Map.MapIO.load(mapName)

class ImageLoader(object):
    def __init__(self):
        self.cache = {}
    
    def __call__(self, imageName, dirName="images"):
        if not self.cache.has_key(imageName):
            filename = imageName + ".png"
            fileName = _getFilename(dirName, filename)
            if fileName == None:
                raise Exception('Image file "%s/%s" not found' % (dirName,
                                                                  filename))
            self.cache[imageName] = pygame.image.load(fileName)
            if pygame.display.get_surface() != None:
                self.cache[imageName] = self.cache[imageName].convert_alpha()
        return self.cache[imageName]

class TextureLoader(object):
    def __init__(self):
        self.cache = {}
        self._textureSize = 64

    def setTextureSize(self, textureSize):
        self._textureSize = textureSize
        self.cache = {}

    def __call__(self, textureName):
        if not self.cache.has_key(textureName):
            i = image(textureName, "textures")
            i = pygame.transform.scale(i, (self._textureSize,
                                           self._textureSize))
            # FIXME: delete these textures when the cache is cleared
            # (and/or in __del__), or we get a memory leak
            textureID = gui.GLUtil.makeTexture(i)[0]
            self.cache[textureName] = textureID
        return self.cache[textureName]


class ScenarioLoader(object):
    def __call__(self, scenarioName):
        import engine.Scenario
        if scenarioName == 'random':
            return engine.Scenario.generateRandom(0)
        if scenarioName == 'random-1':
            return engine.Scenario.generateRandom(1)
        if scenarioName == 'random-2':
            return engine.Scenario.generateRandom(2)
        filename = scenarioName + ".py"
        scenarioFilename = _getFilename("scenarios", filename)
        if scenarioFilename == None:
            raise Exception('Scenario file "%s" not found' % filename)
        return engine.Scenario.ScenarioIO.load(scenarioFilename)


class AbilityLoader(object):
    def __init__(self):
        self.cache = {}
    
    def __call__(self, abilityName):
        if not self.cache.has_key(abilityName):
            import engine.Ability as Ability
            filename = abilityName + ".py"
            f = _getFilename("abilities", filename)
            if f == None:
                raise Exception('Ability file "%s" not found' % f)
            abilityFile = file(f, "rU")

            abilityText = abilityFile.read()
            abilityFile.close()

            globalVars = {}
            localVars = {}

            module = compile("from engine.Equipment import Weapon",
                             "Equipment.py", "exec")
            eval(module, globalVars)

            module = compile("from engine.Range import *",
                             "Range.py", "exec")
            eval(module, globalVars)
            module = compile("from engine.Ability import ACTION, FRIENDLY, HOSTILE, " +
                             "FRIENDLY_AND_HOSTILE, WEAPON_SOUND",
                             "Ability.py", "exec")
            eval(module, globalVars)
            module = compile("from engine.Effect import *",
                             "Effect.py", "exec")
            eval(module, globalVars)
                       
            compiled = compile(abilityText, abilityName + ".py", 'exec')
            eval(compiled, globalVars, localVars)
            abilityData = localVars
            
            if abilityData['VERSION'] != 1:
                raise Exception("Ability version not recognized")

            if abilityData['ABILITY_TYPE'] != Ability.ACTION:
                raise Exception("Only action abilities are supported")
            

            name = _(abilityData['NAME'])
            targetType = abilityData['TARGET_TYPE']
            range_ = abilityData['RANGE']
            aoe = abilityData['AOE']
            effects = abilityData['EFFECTS']

            requiredWeapons = []
            if abilityData.has_key('REQUIRED_WEAPONS'):
                requiredWeapons = abilityData['REQUIRED_WEAPONS']

            cost = 0
            if abilityData.has_key('COST'):
                cost = abilityData['COST']

            sound = None
            if abilityData.has_key('SOUND'):
                sound = abilityData['SOUND']

            description = _(abilityData['DESCRIPTION'])
                
            ability = Ability.Ability(name, description, cost, targetType,
                                      requiredWeapons,
                                      range_, aoe, effects, sound)
            self.cache[abilityName] = ability
        return self.cache[abilityName]
        

class ClassLoader(object):
    def __init__(self):
        self.cache = {}

    def _loadClass(self, className):
        import engine.Class as Class_
        filename = _getFilename("classes", className + ".py")
        if filename == None:
            raise Exception('Class file "%s" not found' % filename)
        classFile = file(filename, "rU")
        classText = classFile.read()
        classFile.close()

        globalVars = {}
        localVars = {}

        compiled = compile(classText, className + ".py", 'exec')

        eval(compiled, globalVars, localVars)
        classData = localVars
        if classData['VERSION'] != 1:
            print "Class version not recognized"

        abilities = []
        if classData.has_key('ABILITIES'):
            abilities = classData['ABILITIES']

        spriteRoot = classData['SPRITE_ROOT']

        self.cache[className] = Class_.Class(_(classData['NAME']),
                                             abilities,
                                             spriteRoot,
                                             classData['MOVE'],
                                             classData['JUMP'],
                                             classData['HP_BASE'],
                                             classData['HP_GROWTH'],
                                             classData['HP_MULT'],
                                             classData['SP_BASE'],
                                             classData['SP_GROWTH'],
                                             classData['SP_MULT'],
                                             classData['WATK_BASE'],
                                             classData['WATK_GROWTH'],
                                             classData['WATK_MULT'],
                                             classData['WDEF_BASE'],
                                             classData['WDEF_GROWTH'],
                                             classData['WDEF_MULT'],
                                             classData['MATK_BASE'],
                                             classData['MATK_GROWTH'],
                                             classData['MATK_MULT'],
                                             classData['MDEF_BASE'],
                                             classData['MDEF_GROWTH'],
                                             classData['MDEF_MULT'],
                                             classData['SPEED_BASE'],
                                             classData['SPEED_GROWTH'],
                                             classData['SPEED_MULT'])

    def __call__(self, classname):
        if not self.cache.has_key(classname):
            self._loadClass(classname)
        return self.cache[classname]

class UnitLoader(object):
    def __call__(self, unitName):
        import engine.Unit as Unit
        import engine.Equipment as Equipment
        filename = unitName + ".py"
        unitFilename = _getFilename("units", filename)
        if unitFilename == None:
            raise Exception('Unit file "%s" not found' % filename)
        unitFile = file(unitFilename, "rU")
        unitText = unitFile.read()
        unitFile.close()

        globalVars = {}
        localVars = {}

        # Load required modules
        module = compile("from engine.Unit import numpy.oldnumeric.ma as MALE, FEMALE, NEUTER, " +
                         "FEMALE_OR_MALE",
                         "Unit.py", "exec")
        eval(module, globalVars)

        # Load actual unit
        compiled = compile(unitText, unitFilename, 'exec')
        eval(compiled, globalVars, localVars)
        unitData = localVars

        # Process fields
        if unitData['VERSION'] != 1:
            print "Unit version not recognized"

        # Gender
        gender = Unit.NEUTER
        if unitData.has_key('GENDER'):
            gender = unitData['GENDER']
            if gender == Unit.FEMALE_OR_MALE:
                if random.random() < 0.5:
                    gender = Unit.FEMALE
                else:
                    gender = Unit.MALE

        # Required field: classes
        classes = unitData['CLASSES']
        (initialClassName, initialClassLevels) = classes[0]
        initialClass = class_(initialClassName)
        unit = initialClass.createUnit(gender)
        latestClass = initialClass
        for i in xrange(1, initialClassLevels):
            initialClass.levelUp(unit)
        for i in xrange(1, len(classes)):
            (className, classLevels) = classes[i]
            class__ = class_(className)
            latestClass = class__
            for j in xrange(0, classLevels):
                class__.levelUp(unit)

        # Weapon (if specified)
        if unitData.has_key('WEAPON'):
            weapon = equipment(Equipment.WEAPON, unitData['WEAPON'])
            unit.equipWeapon(weapon)
        if unitData.has_key('ARMOR'):
            armor = equipment(Equipment.ARMOR, unitData['ARMOR'])
            unit.equipArmor(armor)


        # Sprites (if specified)
        spriteRoot = latestClass.spriteRoot()
        if unitData.has_key('SPRITE_ROOT'):
            spriteRoot = unitData['SPRITE_ROOT']
        unit._spriteRoot = spriteRoot

        return unit

class EquipmentLoader(object):
    def __init__(self):
        self.cache = {}

    def __call__(self, type_, equipmentName):
        if not self.cache.has_key(equipmentName):
            import engine.Equipment as Equipment

            if type_ == Equipment.WEAPON:
                subdir = 'weapons'
            elif type_ == Equipment.ARMOR:
                subdir = 'armor'
            
            filename = equipmentName + ".py"
            equipmentFilename = _getFilename("items/" + subdir, filename)
            if equipmentFilename == None:
                raise Exception('Equipment file "%s" not found' % filename)
            equipmentFile = file(equipmentFilename, "rU")
            equipmentText = equipmentFile.read()
            equipmentFile.close()

            globalVars = {}
            localVars = {}

            # Load required modules
            module = compile("from engine.Equipment import Weapon",
                             "Equipment.py", "exec")
            eval(module, globalVars)

            # Load actual equipment
            compiled = compile(equipmentText, equipmentFilename, 'exec')
            eval(compiled, globalVars, localVars)
            equipmentData = localVars

            name = equipmentData['NAME']
            stats = {}
            stats['mhp'] = equipmentData.get('MHP', 0)
            stats['msp'] = equipmentData.get('MSP', 0)
            stats['watk'] = equipmentData.get('WATK', 0)
            stats['wdef'] = equipmentData.get('WDEF', 0)
            stats['matk'] = equipmentData.get('MATK', 0)
            stats['mdef'] = equipmentData.get('MDEF', 0)
            stats['move'] = equipmentData.get('MOVE', 0)
            stats['jump'] = equipmentData.get('JUMP', 0)
            stats['speed'] = equipmentData.get('SPEED', 0)

            if type_ == Equipment.WEAPON:
                weaponType = equipmentData['TYPE']            
                self.cache[equipmentName] = Equipment.Weapon(name,
                                                             stats,
                                                             weaponType)
            elif type_ == Equipment.ARMOR:
                self.cache[equipmentName] = Equipment.Armor(name, stats)
    
            #Sprites (if specified)
            #spriteRoot = latestClass.spriteRoot()
            spriteName = None
            if equipmentData.has_key('SPRITE_ROOT'):
                spriteRoot = equipmentData['SPRITE_ROOT']
                #spriteName = "%s-%s-%s-%d" % (spriteRoot, genderStr, "standing", 1)
                spriteName = spriteRoot
            if spriteName != None and not _getFilename("images", spriteName + ".png"):
                spriteName = None
                #spriteName = "%s-%s-%s-%d" % (spriteRoot, "unisex", "standing", 1)
            self.cache[equipmentName].setSprites({'standing': [spriteName]})
            


    
        return self.cache[equipmentName]
    

class MusicLoader(object):
    def __call__(self, musicName, loop=True):
        if musicName == None or musicName == '':
            return
        musicFile = _getFilename("music", musicName + ".ogg")
        if musicFile == None:
            return
        try:
            pygame.mixer.music.load(musicFile)
            pygame.mixer.music.set_volume(0.4)
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play(0)
        except pygame.error, e:
            return

class TextLoader(object):
    def __call__(self, textName):
        filename = textName + ".txt"
        textFile = _getFilename("text", filename)
        if textFile == None:
            raise Exception('Text file "%s" not found' % filename)
        f = file(textFile, "rU")
        text = f.readlines()
        f.close()
        return text

class SoundLoader(object):
    def __init__(self):
        self.cache = {}
    
    def __call__(self, soundName):
        if soundName == None:
            return None
        if not self.cache.has_key(soundName):
            soundFile = _getFilename("sounds", soundName + ".ogg")
            if soundFile == None:
                soundFile = _getFilename("sounds", soundName + ".wav")
            try:                
                s = pygame.mixer.Sound(soundFile)
            except pygame.error, e:
                return None
            self.cache[soundName] = s
        return self.cache[soundName]

class SpriteConfigLoader(object):
    def __init__(self):
        self._hand = {}
        self._grip = {}
        spriteConfigFilename = _getFilename("images", "spriteconfig.py")
        if spriteConfigFilename != None:
            spriteConfigFile = file(spriteConfigFilename, "rU")
            spriteConfigText = spriteConfigFile.read()
            spriteConfigFile.close()
            
            localVars = {}
            
            compiled = compile(spriteConfigText, spriteConfigFilename, 'exec')
            eval(compiled, localVars)
            
            self._hand = {}
            self._grip = {}
            self._spriteTypes = None
            
            if localVars.has_key('HAND'):
                self._hand = localVars['HAND']
            if localVars.has_key('GRIP'):
                self._grip = localVars['GRIP']
            if localVars.has_key('SPRITE_TYPES'):
                self._spriteTypes = localVars['SPRITE_TYPES']
        
    def spriteTypes(self):
        return self._spriteTypes
            
    def hand(self, sprite):
        if self._hand.has_key(sprite):
            return self._hand[sprite]
        else:
            return None
        
    def grip(self, sprite):
        if self._grip.has_key(sprite):
            return self._grip[sprite]
        else:
            return None
    
def setCampaign(c):
    global campaign, font, map, image, texture, scenario, class_, ability, weapon, spriteConfig
    logger.debug('Set campaign to "%s"' % c)
    campaign = c
    font = FontLoader()
    map = MapLoader()
    image = ImageLoader()
    texture = TextureLoader()
    scenario = ScenarioLoader()
    class_ = ClassLoader()
    ability = AbilityLoader()
    music = MusicLoader()
    text = TextLoader()
    unit = UnitLoader()
    sound = SoundLoader()
    equipment = EquipmentLoader()
    spriteConfig = SpriteConfigLoader()
    
campaign = 'demo'
font = FontLoader()
map = MapLoader()
image = ImageLoader()
texture = TextureLoader()
scenario = ScenarioLoader()
class_ = ClassLoader()
ability = AbilityLoader()
music = MusicLoader()
text = TextLoader()
unit = UnitLoader()
sound = SoundLoader()
equipment = EquipmentLoader()
spriteConfig = SpriteConfigLoader()
