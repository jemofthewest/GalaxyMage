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

import gettext,os

class Translate:
       
    def getLanguageDict(self,lang):
        return gettext.translation('GalaxyMage',os.path.join(os.getcwd(),'locale'), languages=[lang])
    
    def __init__(self):       
        #fill our language dictionnary with each language
        #self.langDict= { 'sp': self.getLanguageDict('sp'),
	    #             'fr': self.getLanguageDict('fr'),
		#         'en': self.getLanguageDict('en'),
        #                 'nl': self.getLanguageDict('nl')}
        
        #and install current langauge
        #gettext.install('GalaxyMage', unicode=1)
        pass
        
    def setLanguage(self,lang = None):
        #look if we have this language
        if lang != None and self.langDict.has_key(lang):
            self.langDict[lang].install(unicode=1)
        else: # install default language
            gettext.install('GalaxyMage', unicode=1)
