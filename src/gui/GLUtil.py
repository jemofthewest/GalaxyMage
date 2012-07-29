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

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import ScenarioGUI
import MainWindow
import math
from Constants import Z_HEIGHT
import logging
import Resources
import time

logger = logging.getLogger("gui")
maxTextureID = -1

def mapTrans(x, y, z):
    z *= Z_HEIGHT
    glTranslate(1.0 * x, -1.0 * y, z)

def cross((ux, uy, uz), (vx, vy, vz)):
    x = uy * vz - uz * vy
    y = uz * vx - ux * vz
    z = ux * vy - uy * vx
    dist = math.sqrt(x*x + y*y + z*z)
    x /= dist
    y /= dist
    z /= dist

    if (x, y, z) != (0.0, 0.0, 1.0):
        (x, y, z) = (x, y, z) # FIXME: why do we need to do this?

    return (x, y, z)



def makeCube(z, cornerHeights, texture, cornerColors, waterHeight, waterColor,
             minHeight):
    if texture[1] != None:
        glBindTexture(GL_TEXTURE_2D, texture[1])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    cc = cornerColors

    ulz = (z+cornerHeights[0]) * Z_HEIGHT
    urz = (z+cornerHeights[1]) * Z_HEIGHT
    llz = (z+cornerHeights[2]) * Z_HEIGHT
    lrz = (z+cornerHeights[3]) * Z_HEIGHT
    z = z * Z_HEIGHT

    # Enable backface culling
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glBegin(GL_QUADS)

    # Left
    glNormal3f(-1.0, 0.0, 0.0)
    glColor4f(cc[1][0][0], cc[1][0][1], cc[1][0][2], cc[1][0][3])
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, 0.5, 0.0)
    glColor4f(cc[1][1][0], cc[1][1][1], cc[1][1][2], cc[1][1][3])
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, 0.0)
    glColor4f(cc[1][2][0], cc[1][2][1], cc[1][2][2], cc[1][2][3])
    glTexCoord2f(0.0, llz); glVertex3f(-0.5, -0.5, llz)
    glColor4f(cc[1][3][0], cc[1][3][1], cc[1][3][2], cc[1][3][3])
    glTexCoord2f(1.0, ulz); glVertex3f(-0.5, 0.5, ulz)
    
    glEnd()
    
    if texture[2] != None:
        glBindTexture(GL_TEXTURE_2D, texture[2])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
	
	glBegin(GL_QUADS)
    # Back
    glNormal3f(0.0, 1.0, 0.0)
    glColor4f(cc[2][0][0], cc[2][0][1], cc[2][0][2], cc[2][0][3])
    glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, 0.5, 0.0)
    glColor4f(cc[2][1][0], cc[2][1][1], cc[2][1][2], cc[2][1][3])
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.5, 0.0)
    glColor4f(cc[2][2][0], cc[2][2][1], cc[2][2][2], cc[2][2][3])
    glTexCoord2f(0.0, ulz); glVertex3f(-0.5, 0.5, ulz)
    glColor4f(cc[2][3][0], cc[2][3][1], cc[2][3][2], cc[2][3][3])
    glTexCoord2f(1.0, urz); glVertex3f( 0.5, 0.5, urz)

    # Bottom
#     glNormal3f(0.0, 0.0, 1.0)
#     glColor4f(cc[0][0], cc[0][1], cc[0][2], 1.0)
#     glTexCoord2f(1.0, 0.0); glVertex3f( 0.5,  0.5, 0.0)	
#     glColor4f(cc[0][0], cc[0][1], cc[0][2], 1.0)
#     glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, 0.0)	
#     glColor4f(cc[0][0], cc[0][1], cc[0][2], 1.0)
#     glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5, 0.0)
#     glColor4f(cc[0][0], cc[0][1], cc[0][2], 1.0)
#     glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, -0.5, 0.0)

    glEnd()
   
    if texture[3] != None:
        glBindTexture(GL_TEXTURE_2D, texture[3])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
        
    glCullFace(GL_FRONT)
    
    glBegin(GL_QUADS)
    # Right
    glNormal3f(1.0, 0.0, 0.0)
    glColor4f(cc[3][0][0], cc[3][0][1], cc[3][0][2], cc[3][0][3])
    glTexCoord2f(0.0, 0.0); glVertex3f( 0.5,-0.5, 0.0)
    glColor4f(cc[3][3][0], cc[3][3][1], cc[3][3][2], cc[3][3][3])
    glTexCoord2f(0.0, lrz); glVertex3f( 0.5,-0.5, lrz)
    glColor4f(cc[3][2][0], cc[3][2][1], cc[3][2][2], cc[3][2][3])
    glTexCoord2f(1.0, urz); glVertex3f( 0.5, 0.5, urz)
    glColor4f(cc[3][1][0], cc[3][1][1], cc[3][1][2], cc[3][1][3])
    glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, 0.5, 0.0)		

    glEnd()
    
    if texture[4] != None:
        glBindTexture(GL_TEXTURE_2D, texture[4])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
    
    glBegin(GL_QUADS)
      
    # Front
    glNormal3f(0.0, -1.0, 0.0)
    glColor4f(cc[4][1][0], cc[4][1][1], cc[4][1][2], cc[4][1][3])
    glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5, 0.0)
    glColor4f(cc[4][0][0], cc[4][0][1], cc[4][0][2], cc[4][0][3])
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, 0.0)
    glColor4f(cc[4][3][0], cc[4][3][1], cc[4][3][2], cc[4][3][3])
    glTexCoord2f(0.0, llz); glVertex3f(-0.5, -0.5, llz)
    glColor4f(cc[4][2][0], cc[4][2][1], cc[4][2][2], cc[4][2][3])
    glTexCoord2f(1.0, lrz); glVertex3f( 0.5, -0.5, lrz)
    
    glEnd()
    
    if texture[0] != None:
        glBindTexture(GL_TEXTURE_2D, texture[0])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 


    # Top

    # Calculate normals for each vertex
    # First find the normals for each of the 4 triangles
    (nux, nuy, nuz) = cross((-0.5, 0.5, ulz-z), (-0.5, -0.5, z-urz))
    (nrx, nry, nrz) = cross((0.5, 0.5, urz-z), (-0.5, 0.5, z-lrz))
    (ndx, ndy, ndz) = cross((0.5, -0.5, lrz-z), (0.5, 0.5, z-llz))
    (nlx, nly, nlz) = cross((-0.5, -0.5, llz-z), (0.5, -0.5, z-ulz))

    # To find the normal of each of the four corners, average the
    # normals of the two triangles that touch that corner.
    (nulx, nuly, nulz) = (nux+nlx, nuy+nly, nuz+nlz)
    (nurx, nury, nurz) = (nux+nrx, nuy+nry, nuz+nrz)
    (nllx, nlly, nllz) = (ndx+nlx, ndy+nly, ndz+nlz)
    (nlrx, nlry, nlrz) = (ndx+nrx, ndy+nry, ndz+nrz)

    # To find the normal of the center, average all four corner
    # normals.
    (nmx, nmy, nmz) = (nulx+nurx+nllx+nlrx,
                       nuly+nury+nlly+nlry,
                       nulz+nurz+nllz+nlrz)

    # Now, find the color for the center vertex -- the average of all
    # four corners
    (mr, mg, mb, ma) = ((cc[0][0][0]+cc[0][1][0]+cc[0][2][0]+cc[0][3][0]) / 4,
                        (cc[0][0][1]+cc[0][1][1]+cc[0][2][1]+cc[0][3][1]) / 4,
                        (cc[0][0][2]+cc[0][1][2]+cc[0][2][2]+cc[0][3][2]) / 4,
                        (cc[0][0][3]+cc[0][1][3]+cc[0][2][3]+cc[0][3][3]) / 4)
    
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(nmx, nmy, nmz); glColor4f(mr, mg, mb, ma)
    glTexCoord2f(0.5, 0.5); glVertex3f( 0.0,  0.0, z)
    glNormal3f(nulx, nuly, nulz)
    glColor4f(cc[0][0][0], cc[0][0][1], cc[0][0][2], cc[0][0][3])
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, ulz)
    glNormal3f(nurx, nury, nurz)
    glColor4f(cc[0][1][0], cc[0][1][1], cc[0][1][2], cc[0][1][3])
    glTexCoord2f(1.0, 0.0); glVertex3f( 0.5,  0.5, urz)
    glNormal3f(nlrx, nlry, nlrz)
    glColor4f(cc[0][3][0], cc[0][3][1], cc[0][3][2], cc[0][3][3])
    glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, -0.5, lrz)
    glNormal3f(nllx, nlly, nllz)
    glColor4f(cc[0][2][0], cc[0][2][1], cc[0][2][2], cc[0][2][3])
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5, llz)
    glNormal3f(nulx, nuly, nulz)
    glColor4f(cc[0][0][0], cc[0][0][1], cc[0][0][2], cc[0][0][3])
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, ulz)
    glEnd()

    if waterHeight != 0 and minHeight < waterHeight:
        waterHeight -= 0.5
        waterHeight *= Z_HEIGHT
        glBindTexture(GL_TEXTURE_2D, Resources.texture('none'))
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)
        glColor4f(waterColor[0], waterColor[1], waterColor[2], waterColor[3])
        glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5, waterHeight)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, waterHeight)
        glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5, waterHeight)
        glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5, waterHeight)
        glEnd()
    
#     (nx, ny, nz) = cross((1.0, 0.0, ulz - urz), (0.0, 1.0, urz-lrz))
#     if (nx, ny, nz) != (0.0, 0.0, 1.0):
#         (nx, ny, nz) = (-nx, ny, nz) # FIXME: why do we need to do this?
#     glNormal3f(nx, ny, nz)
#     maxZ = max(ulz, urz, llz, lrz)
#     if maxZ == ulz or maxZ == lrz:
#         glCullFace(GL_FRONT)
#         glBegin(GL_QUADS)
#         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, ulz)
#         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5,  0.5, urz)
#         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, -0.5, lrz)
#         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5, llz)
#         glEnd()
#     else:
#         glCullFace(GL_BACK)
#         glBegin(GL_QUADS)
#         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5, llz)
#         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, -0.5, lrz)
#         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5,  0.5, urz)
#         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, ulz)
#         glEnd()


    glDisable(GL_CULL_FACE)



def makeCubeTop(z, cornerHeights):
    z *= Z_HEIGHT
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glTranslate(0.0, 0.0, z)

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f( 0.0,   0.0, 0.0)
    glVertex3f( 0.5,   0.5, cornerHeights[1] * Z_HEIGHT)
    glVertex3f(-0.5,   0.5, cornerHeights[0] * Z_HEIGHT)
    glVertex3f(-0.5,  -0.5, cornerHeights[2] * Z_HEIGHT)   
    glVertex3f( 0.5,  -0.5, cornerHeights[3] * Z_HEIGHT)
    glVertex3f( 0.5,   0.5, cornerHeights[1] * Z_HEIGHT)
    glEnd()
    glPopMatrix()
    glEnable(GL_LIGHTING)

def drawAt((posx, posy), texture, image):
    (width, height) = MainWindow.get().size()
    dx = image.get_width()
    dy = image.get_height()
    switchToOrthographicMode()
    glTranslate(posx, height-posy, 0.0)
    makeRect(texture, dx, -dy)
    switchFromOrthographicMode()

def switchToOrthographicMode():
    # Set up orthographic projection for drawing to screen
    (width, height) = MainWindow.get().size()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0 * width, 0.0, 1.0 * height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

def switchFromOrthographicMode():
    # Undoes the matrix transformations that are done by
    # switchToOrthographicMode()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)

def drawBar(leftColor, rightColor, barWidth, barHeight, (posx, posy)):
    (width, height) = MainWindow.get().size()
    
    # If you want to draw to a specific (x,y) position on screen,
    # instead of drawing inside the actual 3D world, you need to
    # switch to orthographic mode first.
    switchToOrthographicMode()

    # Actual drawing code begins here
    glTranslate(posx, height-posy, 0.0)
    glBindTexture(GL_TEXTURE_2D, Resources.texture('none'))
    glBegin(GL_QUADS)

    # Draw the colored bar
    leftColor[3] = 0.0
    glColor4f(*leftColor)
    glVertex3f(0.0, 0.0, 0.0)
    leftColor[3] = 0.9
    glColor4f(*leftColor)
    glVertex3f(0.0, -barHeight, 0.0)
    rightColor[3] = 0.9
    glColor4f(*rightColor)
    glVertex3f(barWidth, -barHeight, 0.0)
    rightColor[3] = 0.0
    glColor4f(*rightColor)
    glVertex3f(barWidth, 0.0, 0.0)
    glEnd()

    # When we're done drawing to the screen, we switch back into
    # "normal" (perspective projection) mode
    switchFromOrthographicMode()

def createBorder(width, height, image = None):
    borderWidth = 3
    borderPadding = 10
    bordered = pygame.Surface(
        (width + borderPadding*2,
         height + borderPadding*2)).convert_alpha()
    bordered.fill((0,0,255,180))
    pygame.draw.rect(bordered,
                     (255,255,255,210),
                     pygame.Rect((1,1), (bordered.get_width()-2,
                                         bordered.get_height()-2)),
                     borderWidth)
    pygame.draw.rect(bordered,
                     (0,0,0,180),
                     pygame.Rect((0,0), (bordered.get_width(),
                                         bordered.get_height())),
                     1)
    if image != None:
        bordered.blit(image, (borderPadding, borderPadding))
    return bordered

def renderTextToTexture(font, color, text, border, backgroundColor):
    image = font.render(text, True, color)
    if border:
        image = createBorder(image.get_width(), image.get_height(), image)
    imageSize = image.get_size()
    (texture, image) = makeTexture(image, backgroundColor)
    return (texture, image, imageSize)

def drawText(font, color, text, (posx, posy), border, backgroundColor,
             centerx=False, centery=False):
    (texture, image, imageSize) = renderTextToTexture(font, color, text,
                                                      border, backgroundColor)
    if centerx:
        posx -= imageSize[0]/2
    if centery:
        posy -= imageSize[1]/2
        
    listID = glGenLists(1)
    glNewList(listID, GL_COMPILE_AND_EXECUTE)
    drawAt((posx, posy), texture, image)
    glEndList()
    return texture, listID, imageSize
    
def makeRect(texture, width = 1.0, height = 1.0):
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glBegin(GL_QUADS)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(width, height, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(0, height, 0.0)		
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 0, 0.0)		
    glTexCoord2f(1.0, 1.0); glVertex3f(width, 0, 0.0)
    glEnd()

def makeTexture(textureSurface, backgroundColor = None, textureID = -1):
    global maxTextureID
    powersOf2 = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    needToCopy = False
    if width not in powersOf2:
        for i in xrange(0, len(powersOf2)):
            if powersOf2[i] > width:
                needToCopy = True
                width = powersOf2[i]
                break
    if height not in powersOf2:
        for i in xrange(0, len(powersOf2)):
            if powersOf2[i] > height:
                needToCopy = True
                height = powersOf2[i]
                break
    if needToCopy:
        newSurface = pygame.Surface((width, height)).convert_alpha()
        if backgroundColor == None:
            newSurface.fill((0,0,0,0))
        else:
            newSurface.fill(backgroundColor)
        newSurface.blit(textureSurface, (0, 0))
        textureSurface = newSurface
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    if textureID == -1:
        textureID = glGenTextures(1)
        if textureID > maxTextureID:
            maxTextureID = textureID
            logger.debug("Max texture ID: " + str(textureID))
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 textureSurface.get_width(), textureSurface.get_height(),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData);
    return (textureID, textureSurface)

def drawFloatingText(texture, aspectRatio, height, alpha):
    scale = 0.5
    glPushMatrix()
    glTranslatef(0, 0, height)
    glScale(scale, scale, scale)
    glRotatef(-ScenarioGUI.get().camera.mapRotation(), 0.0, 0.0, 1.0)
    glRotatef(-ScenarioGUI.get().camera.pitch(), 1.0, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glBegin(GL_QUADS)
    glColor4f(1.0, 1.0, 1.0, alpha)
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 0.5*aspectRatio, 1.0, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5*aspectRatio, 1.0, 0.0)		
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5*aspectRatio, 0.0, 0.0)		
    glTexCoord2f(1.0, 0.0); glVertex3f( 0.5*aspectRatio, 0.0, 0.0)		
    glEnd()
    glPopMatrix()


# FIXME: depends on GUI code - shouldn't be here
def makeUnit(texture, wtexture=None, otexture=None, color=(1.0, 1.0, 1.0, 1.0),
             unitHand=None, weaponGrip=None):
    (r, g, b, a) = color
    scale = 1.4
    
    glPushMatrix()
    glScale(scale, scale, scale)
    glRotatef(-ScenarioGUI.get().camera.mapRotation(), 0.0, 0.0, 1.0)
    glRotatef(-ScenarioGUI.get().camera.pitch(), 1.0, 0.0, 0.0)
    #glRotatef(-90.0, 1.0, 0.0, 0.0)
    
    #glRotatef(-GUI.get().camera.pitch()/2.0, 1.0, 0.0, 0.0)
    #glRotatef(90.0, 1.0, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glBegin(GL_QUADS)
    glColor4f(r, g, b, a)
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, 1.0, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 1.0, 0.0)		
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.0, 0.0)		
    glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, 0.0, 0.0)		
    glEnd()
    glPopMatrix()

    if wtexture != None:
        if unitHand == None:
            unitHand = (32, 45, -45, False)
        if weaponGrip == None:
            weaponGrip = (32, 32, -45, False)
        (gripx, gripy, gripr, weaponOrientation) = weaponGrip
        (handx, handy, handr, handOrientation) = unitHand
        
        # Change coordinates (move origin from top left to bottom center and flip y-axis)
        gripx -= 32.0
        gripy = 64.0 - gripy
        handy = 64.0 - handy
        handx -= 32.0
        zoff = 0.001
        if handOrientation != weaponOrientation:# flip coords if needed
            #handx = - handx
            gripr = - gripr
            zoff = - zoff
            
        # Find the necessary rotation for the weapon
        rot = handr - gripr
        rad = math.radians(rot)
        
        # Get the hand postion in the rotated coordinates
        #if handOrientation != weaponOrientation:# flip coords if needed
        #    r_handy = handy * math.cos(rad) + handx * math.sin(rad)
        #    r_handx = handx * math.cos(rad) - handy * math.sin(rad)
        r_handy = handy * math.cos(rad) + handx * math.sin(rad)
        r_handx = handx * math.cos(rad) - handy * math.sin(rad)
        if handOrientation != weaponOrientation:# flip coords if needed
            r_handx = - r_handx
            
        # Get the offsets for adjusting weapon position
        xoff = (r_handx - gripx) / 64.0
        yoff = (r_handy - gripy) / 64.0
        
        glPushMatrix()
        glScale(scale, scale, scale)
        glRotatef(-ScenarioGUI.get().camera.mapRotation(), 0.0, 0.0, 1.0)
        glRotatef(-ScenarioGUI.get().camera.pitch(), 1.0, 0.0, 0.0)
        
        # Match hand and weapon direction
        glRotatef(rot, 0.0, 0.0, -1.0)
        if  handOrientation != weaponOrientation:# flip weapon if needed
            glRotatef(180, 0.0, 1.0, 0.0)

        glBindTexture(GL_TEXTURE_2D, wtexture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glBegin(GL_QUADS)
        glColor4f(r, g, b, a)
        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 0.5 + xoff, 1.0 + yoff, zoff)
        glTexCoord2f(0.0, 1.0); glVertex3f(-0.5 + xoff, 1.0 + yoff, zoff)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5 + xoff, 0.0 + yoff, zoff)
        glTexCoord2f(1.0, 0.0); glVertex3f( 0.5 + xoff, 0.0 + yoff, zoff)
        glEnd()
        glPopMatrix()

        if otexture != None:
            glPushMatrix()
            glScale(scale, scale, scale)
            glRotatef(-ScenarioGUI.get().camera.mapRotation(), 0.0, 0.0, 1.0)
            glRotatef(-ScenarioGUI.get().camera.pitch(), 1.0, 0.0, 0.0)
            #glRotatef(-90.0, 1.0, 0.0, 0.0)
            
            #glRotatef(-GUI.get().camera.pitch()/2.0, 1.0, 0.0, 0.0)
            #glRotatef(90.0, 1.0, 0.0, 0.0)
            glBindTexture(GL_TEXTURE_2D, otexture)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glBegin(GL_QUADS)
            glColor4f(r, g, b, a)
            glNormal3f(0.0, 0.0, 1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, 1.0, 0.002)
            glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 1.0, 0.002)		
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.0, 0.002)		
            glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, 0.0, 0.002)		
            glEnd()
            glPopMatrix()

# FIXME: get rid of global variables
# These are global variables for the following animation function
# The last time we updated the animation
lastTime = None
# coordinates of the texture to show
# 1.0, 1.0 is the top left frame and 2.0, 2.0 is the bottom right
s, t = 1.0, 1.0 

def makeStatus(texture, color = (1.0, 1.0, 1.0, 1.0) ):
    global s, t, lastTime
    (r, g, b, a) = color
    glPushMatrix()
    
    glRotatef(-ScenarioGUI.get().camera.mapRotation(), 0.0, 0.0, 1.0)
    glRotatef(-ScenarioGUI.get().camera.pitch(), 1.0, 0.0, 0.0)
    
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    glTranslatef(0.3, 0.5, 0.0)

    glBegin(GL_QUADS)
    glColor4f(r, g, b, a)
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.5*s,  1.0/t); glVertex3f( 0.5, 1.0, 0.0)
    glTexCoord2f(0.5*s - 0.5, 1.0/t); glVertex3f(-0.5, 1.0, 0.0)
    glTexCoord2f(0.5*s - 0.5, 1.0/t - 0.5); glVertex3f(-0.5, 0.0, 0.0)		
    glTexCoord2f(0.5*s, 1.0/t - 0.5); glVertex3f( 0.5, 0.0, 0.0)
    glEnd()

    glPopMatrix()

    # The frame change after enough time
    if lastTime == None:
        lastTime = time.time()
    elif time.time() - lastTime > 0.15:
        lastTime = time.time()
        if s == 1.0:
            s = 2.0
        else:
            if t == 2.0:
                s, t = 1.0, 1.0
            else:
                s, t = 1.0, 2.0
                
