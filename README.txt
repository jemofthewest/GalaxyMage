GalaxyMage: an open-source tactical RPG.
http://www.galaxymage.org

Copyright (C) 2005 Colin McMillen <mcmillen@cs.cmu.edu> and
contributors.  See the CREDITS.txt file for more information. 

See http://www.galaxymage.org/index.php/Changelog to find out what's
new in this version.


INSTALLATION

GalaxyMage is written in Python, so you'll need a Python interpreter
to get anything working. It also depends on several Python modules;
see the DEPENDENCIES section below if you have any problems.  If you
do have all the dependencies, you should be able to run the current
demo just by running the main GalaxyMage script with a Python
interpreter. From a shell, the following command should do the trick:

$ python GalaxyMage.py

Users of graphical file managers can probably double-click the
GalaxyMage script to achieve the same effect.


DEPENDENCIES

You'll need a Python interpreter for your platform. See
http://www.python.org for more details. GalaxyMage is officially
developed for Python version 2.4. However, it should also work with
Python 2.3, and possibly earlier versions.

In addition to the standard Python distribution, you'll also need the
following Python libraries:

* Numeric
  http://sourceforge.net/project/showfiles.php?group_id=1369&package_id=1351

* PyOpenGL
  http://sourceforge.net/project/showfiles.php?group_id=5988&package_id=6035

* PyGame
  http://pygame.org/download.shtml

* Twisted
  http://twistedmatrix.com

If you are using a Unix-like operating system, the easiest way to
install these dependencies is probably through your package management
system. On Debian GNU/Linux (or derivatives such as Ubuntu), these are
the names of the packages you'll need:

python python-numeric python-opengl python-pygame python-twisted

Using an old version of PyOpenGL might cause GalaxyMage to crash, with
the following error message: "(pygame parachute) Segmentation
Fault". If you experience this error, please update to a more recent
version of PyOpenGL.

For Windows users, you can download the needed packages directly at
the following links (up-to-date as of 2005-Nov-26):

* Python 2.4
  http://python.org/ftp/python/2.4.2/python-2.4.2.msi

* Numeric
  http://prdownloads.sourceforge.net/numpy/Numeric-24.2.win32-py2.4.exe

* PyOpenGL
  http://prdownloads.sourceforge.net/pyopengl/PyOpenGL-2.0.2.01.py2.4-numpy23.exe

* PyGame
  http://www.pygame.org/ftp/pygame-1.7.1release.win32-py2.4.exe

* Twisted
  http://tmrc.mit.edu/mirror/twisted/Twisted/2.2/Twisted_NoDocs-2.2.0.win32-py2.4.exe


OPTIONAL PACKAGE: PSYCO

If you have the "psyco" just-in-time Python compiler, GalaxyMage will
auto-detect it, and use it to speed up execution.  If you don't have
psyco, no problem -- GalaxyMage will still work correctly.  It'll just
run a bit more slowly.

To install psyco in Linux, get a package with a name like
"python-psyco".

To install psyco in Windows, grab the following installer:

* http://prdownloads.sourceforge.net/psyco/psyco-1.5.win32-py2.4.exe


PLAYING THE GAME

See the file doc/controls.txt for a quick primer on the game
controls. Run GalaxyMage with the -h option for help with command-line
options:

$ python GalaxyMage.py -h


LICENSE

The GalaxyMage source code is copyright (C) 2005 Colin McMillen.

GalaxyMage is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

GalaxyMage is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with GalaxyMage; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

See COPYRIGHT.txt for more information.

The data files used by GalaxyMage (all under the directory data/) are
copyright their individual authors. These files are redistributed with
their authors' permission, typically under a Creative Commons or GPL
license. To see the licensing terms for each of these files, see the
COPYRIGHT.txt file in that file's directory.
