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

import os
import sys
import logging
import platform
import optparse

"""Version number is MAJOR.MINOR.REVISION, optionally followed by a
hyphen and some free-form text, like 'alpha' or 'prerelease'."""
__version__ = "0.3.0"

def dependencyCheck():
    """Check to make sure that external dependencies can be loaded
    properly."""
    logging.debug('Platform: ' + platform.platform())
    logging.debug('Python version ' + sys.version)
    try:
        import numpy.oldnumeric as Numeric
        logging.debug('Numeric version ' + Numeric.__version__)
    except ImportError, err:
        logging.error('Loading dependency "Numeric" failed: ' + str(err))
        sys.exit(1)

    try:
        import pygame
        logging.debug('pygame version ' + pygame.version.ver)
    except ImportError, err:
        logging.error('Loading dependency "pygame" failed: ' + str(err))
        sys.exit(1)

    try:
        import OpenGL.GL
        logging.debug('PyOpenGL version ' + OpenGL.__version__)
    except ImportError, err:
        logging.error('Loading dependency "OpenGL.GL" failed: ' + str(err))
        sys.exit(1)

    try:
        import OpenGL.GLU
    except ImportError, err:
        logging.error('Loading dependency "OpenGL.GLU" failed: ' + str(err))
        sys.exit(1)

    try:
        import twisted
        logging.debug('Twisted version ' + twisted.__version__)
    except ImportError, err:
        logging.error('Loading dependency "twisted" failed: ' + str(err))
        sys.exit(1)
        
def main():
    """Parse options and run the program accordingly."""
    print 'GalaxyMage', __version__

    import Translate   
    # init translate 
    translateConfig = Translate.Translate()
       
    # Parse command-line options
    parser = optparse.OptionParser(description="Cross-platform, open-source tactical RPG.")
    parser.add_option("--fullscreen", "-f",
                      action="store_true", default=False,
                      help="start in fullscreen mode")
    parser.add_option("--quiet", "-q", action="store_true", default=False,
                      help="disable sounds and music")
    parser.add_option("--disable-jit", "-j",
                      dest="useJIT", action="store_false", default=True,
                      help='disable "psyco" just-in-time compiler')
    parser.add_option("--verbose", "-v", action="count", default=0,
                      help='increase logging verbosity')
    parser.add_option("-w", dest="width", type="int",
                      default=800, metavar="WIDTH",
                      help='initial window width [default: %default]')
    parser.add_option("--edit-map", "-e", action="store", default=None,
                      metavar="MAPNAME",
                      help='start the map editor')
    parser.add_option("--port", "-P", type='int', default=22222,
                      help='game server port [default: %default]')
    parser.add_option("--lang", "-l", default="en",
                      help="set language")
    parser.add_option("--user", default=os.environ.get('USER', 'Player'),
                      help="set username for multiplayer")
    (options, args) = parser.parse_args()

    # Enable logging
    import Log
    logLevel = logging.INFO - options.verbose * 10
    logLevel = max(logLevel, 1)
    Log.setUpLogging(logLevel)

    #translateConfig.setLanguage(options.lang)

    # Check to make sure we can load dependencies
    dependencyCheck()
              
    # Import Psyco if available
    if False and options.useJIT: # FIXME: re-enable psyco
        try:
            import psyco
            logging.debug('Enabled "psyco" just-in-time Python compiler')
            psyco.full()
        except ImportError:
            logging.debug('"psyco" just-in-time Python compiler not found')
   
    # Set up PyGame
    import pygame
    pygame.display.init()
    pygame.font.init()
    pygame.joystick.init()
 
    try:
        pygame.mixer.init(48000, -16, True, 4096)
    except pygame.error, e:
        options.quiet = True
        logging.warn("Couldn't initialize sound: " + str(e))

    # Import our own modules
    import Resources
    import Sound
    import twistedmain

    # Set texture size
    Resources.texture.setTextureSize(64)

    # Initialize Sound
    Sound.setQuiet(options.quiet)

    twistedmain.run(options)
    
