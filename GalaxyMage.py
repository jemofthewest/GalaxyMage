#!/usr/bin/env python2

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

# Add src/ to our module path
import os, sys
if os.path.isdir(sys.path[0]):
    os.chdir(sys.path[0])
sys.path.append("src")

import Main

Main.main()

# import hotshot, hotshot.stats
# prof = hotshot.Profile("gm.prof")
# prof.runcall(Main.main)
# prof.close()
# stats = hotshot.stats.load("gm.prof")
# stats.strip_dirs()
# stats.sort_stats('time', 'calls')
# stats.print_stats()

