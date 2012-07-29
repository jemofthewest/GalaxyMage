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

def setUpLogging(loglevel):
    # Add custom "debug2" level
    logging.setLoggerClass(CustomLogger)
    logging.addLevelName(9, "DEBUG2")
    
    # Create our stream handler
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-4s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
        
    # Set up all the logging streams
    for logger in ['', 'ai', 'gui', 'reso', 'batt', 'gsrv', 'gcli']:
        logging.getLogger(logger).setLevel(loglevel)
        logging.getLogger(logger).addHandler(console)
        logging.getLogger(logger).propagate = False

class CustomLogger(logging.Logger):
    def debug2(self, msg):
        self.log(9, msg)
