# Copyright (C) 2005 Jamie Macey <jamie.macey@gmail.com>
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

import unittest
import Resources

class ResourceLoadingLocationTestCase(unittest.TestCase):
    '''Verify that data files are all found in correct branches'''
    
    def testLoadsDataFromCore(self):
        '''Should load data from the 'data/core' folder'''
        data = Resources.class_('fighter')
        self.assertEqual(data.name, 'Fighter-c')
    
    def testLoadsDataFromExtra(self):
        '''Should load data from the 'data/extra' folder'''
        data = Resources.class_('bandit')
        self.assertEqual(data.name, 'Bandit-e')
    
    def testLoadsDataFromDemo(self):
        '''Should load data from the 'data/demo' folder'''
        # first, verify that the current campaign is demo
        self.assertEqual(Resources.campaign, 'demo')
        data = Resources.class_('ruffian')
        self.assertEqual(data.name, 'Ruffian-d')
    
    def testPrefersDataFromExtraOverCore(self):
        '''Should load data from 'data/extra' if that data also is in 'data/core'. '''
        data = Resources.class_('beggar')
        self.assertEqual(data.name, 'Beggar-e')
    
    def testPrefersDataFromDemoOverCore(self):
        '''Should load data from 'data/demo' if that data also is in 'data/core'. '''
        data = Resources.class_('thief')
        self.assertEqual(data.name, 'Thief-d')
    
    def testPrefersDataFromDemoOverExtra(self):
        '''Should load data from 'data/demo' if that data also is in 'data/extra'. '''
        data = Resources.class_('snitch')
        self.assertEqual(data.name, 'Snitch-d')
    
    def testShouldErrorIfDataDoesNotExist(self):
        '''Should return an error if trying to load missing data'''
        try:
            data = Resources.class_('missing')
        except Exception, e:
            self.assertEqual(str(e), 'Class file "None" not found')


class UnitRelatedResourceLoaderTestCase(unittest.TestCase):
    '''Verify all unit related data files are loaded correctly.'''
    
    def testNothing(self):
        pass
    
    def testClassLoader(self):
        '''Should load class data from file'''
        data = Resources.class_('fighter')
        self.assertEqual(data.name, 'Fighter-c')
    
#     def testAbilityLoader(self):
#     def testEquipmentLoader(self):
#     def testTextLoader(self):
#     def testUnitLoader(self):

class ScenarioRelatedResourceLoaderTestCase(unittest.TestCase):
    '''Verify all map related data files are loaded correctly.'''
    
    def testNothing(self):
        pass
#     def testMapLoader(self):
#     def testScenarioLoader(self):


class GraphicsRelatedResourceLoaderTestCase(unittest.TestCase):
    '''Verify all graphics related data files are loaded correctly.'''
    
    def testNothing(self):
        pass
#     def testImageLoader(self):
#     def testTextureLoader(self):
#     def testSpriteConfigLoader(self):
#     def testFontLoader(self):

class AudioRelatedResourceLoaderTestCase(unittest.TestCase):
    '''Verify all sound related data files are loaded correctly.'''
    
    def testNothing(self):
        pass
#     def testMusicLoader(self):
#     def testSoundLoader(self):


