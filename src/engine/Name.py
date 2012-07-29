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
import Unit
import random as random_
import re

def random(gender):
    if not _loaded:
        _load()
    name = ''
    # We loop here just in case the names file has a blank line or
    # something... don't want to return an empty name
    while re.search('\w+', name) == None:
        if gender == Unit.MALE:
            name = random_.choice(_maleNames)
        elif gender == Unit.FEMALE:
            name = random_.choice(_femaleNames)
        else:
            name = random_.choice(_neuterNames)
    return name

# Gathered manually from http://www.ssa.gov/cgi-bin/popularnames.cgi
def _load():
    global _maleNames, _femaleNames, _neuterNames, _loaded
    _loaded = True
    _maleNames = Resources.text("names-male")
    _femaleNames = Resources.text("names-female")
    # FIXME: maintain a neuter file at some point
    _neuterNames = Resources.text("names-male")
    for n in [_maleNames, _femaleNames, _neuterNames]:
        for i in xrange(0, len(n)):
            n[i] = n[i].strip()

_loaded = False
_femaleNames = None   
_maleNames = None
_neuterNames = None
