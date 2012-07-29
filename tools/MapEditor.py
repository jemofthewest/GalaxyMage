# MapEditor for GalaxyMage
	# author: jake b (ninmonkeys) ninmonkeys@gmail.com
	# last update: APP_VERSION_STRING

import sys, pygame

#soon:
	# user set map_max_height
	# 2nd image for groups

# todo:
	# (features)
		# optional scaling? (ie: some maps might prefer it off?)
		# images 2, 3
			# 2: tile groups data
			# 3: unit coord data (or don't need/want?)
		# if no command args, then force user input
		# output image template?
		# image with tiles_width > 1px
			# img.get_width() / TILE_WIDTH
			# and adjust getPixel(i*TILE_W,j*TILE_W)

	# (Classes)
		#Mapdata:
			# accessors? (int) getTile(x,y); OR (int) getData(x,y,'tile' OR 'group')

	# (bugs)


APP_VERSION_STRING = "MapEditor v0.2 (2006/01/02) for GalaxyMage"

class MapData:
	'''class for GalaxyMage map data'''
	#tiles = []	# map tile data
	#groups = []	#map groups data

	def __init__(self):
		self.tiles = [] # map tile data
		self.groups = [] # map tile groups data
		self.width = 0 # map width
		self.height = 0 # map height

	def Len(self):
		'''outputs dimensions'''
		#print w x h (of arrays)
		print "dimensions of: tiles[%d][%d] WxH:%dx%d" % (len(self.tiles),len(self.tiles[0]),self.width,self.height)
		#print "dimensions of: groups[%d][%d] WxH:%dx%d" % (len(self.groups),len(self.groups[0]),self.width,self.height)

	def size(self,width,height): # resize arrays
		'''size arrays to var[width][height]'''
		print "sizing array(s) to: %dx%d" % (width,height)
		# sizing: foo[x][y] is declared: [[0 for col in range(y)] for row in range(x)]
		self.tiles = [[0 for col in range(height)] for row in range(width)]
		self.groups =[[0 for col in range(height)] for row in range(width)]
		self.width = width
		self.height = height

		self.Len() #debug: print sizing since we just sized it

#globals
map_data = MapData()

# misc functions
def config_read(path):
	'''reads scripts config file'''
	# jake todo:
	# parse data, using regex for "a=b"

def normalize(value, value_max):
	'''"normalizes" the value, ie: converts it to the range of 0.0-1.0'''
	return value / value_max

# map_* functions
def map_write(path):
	'''writes the map to "path"'''
	print "map_write(path):",path # jake debug:
	#fout = open("map-data.py",'w')
	fout = open(path, 'w')

	# map file header: text, version, width, height
	#fout.write("# map generated with: MapEditor\n\nVERSION = 1\nWIDTH = %d\nHEIGHT = %d\n" % (img.get_width(), img.get_height() ))
	fout.write("# map generated with: MapEditor\n\nVERSION = 1\nWIDTH = %d\nHEIGHT = %d\n" % (map_data.width, map_data.height ))
	# tiles_header
	fout.write("# map tiles\nLAYOUT = \'\'\'\n")

    #write tiles data
	for j in xrange(0, map_data.height):
		for i in xrange(0, map_data.width):
			fout.write("%d " % map_data.tiles[i][j])

		#newline for next row of data
		fout.write("\n")

	# tiles_footer
	fout.write("\'\'\'\n")
	fout.close()

def map_scale():
	'''scales map based on users map max height'''
	# jake todo: steps? ie: prefer values 0,6,12 etc?
	map_height_max = 42.0 # user max map height set
	value_max = 1 # max pixel value
	map_scale = 1 # value to scale map by
	#get max pixel value
	for j in xrange(0, map_data.height):
		for i in xrange(0, map_data.width):
			if map_data.tiles[i][j] > value_max:
				value_max = map_data.tiles[i][j]

	# map set max / pixel max = scale value
		# multiply this to scale all tiles
	map_scale = normalize(map_height_max, value_max)
		#equal to: map_scale = map_height_max / value_max
	print "map_scale(): max pixel: %d, scale: %f" % (value_max, map_scale)

	#now actually scale the data
	for j in xrange(0, map_data.height):
		for i in xrange(0, map_data.width):
			map_data.tiles[i][j] = map_data.tiles[i][j] * map_scale


#image_* functions #
def image_load(path):
	'''reads image data in'''
	print "image_load(path):",path # jake debug:
	img = pygame.image.load(path)

	# lock surface for direct pixel read/writing
	if img.mustlock():
		img.lock()

	#size array
	map_data.size(img.get_width(),img.get_height())
	#read pixel data
	for j in xrange(0, img.get_height()):
		for i in xrange(0, img.get_width()):
			(r,g,b,a) = img.get_at((i,j))
#debug: print "(x,y) = (r/g/b) : (", i, ",", j, ") ",r
			#save color, since it's grayscale, grab just r
			map_data.tiles[i][j] = r

			#debug: print "%dr" % r,	#jake debug: was: print "debug: r,"

	#done, unlock surface
	if img.mustlock():
		img.unlock

def image_template(width, height):
	# create an empty? grid? image for a map template
	print "image_template(width,height) = ",width,height

def main():
	#main function, this is just for clarity/readability
	print APP_VERSION_STRING

	# get args, and output current values
	arg_num = len(sys.argv)

	# no args, print usage
	if arg_num == 1:
		#usage
		print '''
mapeditor.py usage:

	<image> [<image2>] [<image3>] [<map_name>]
		Reads <image> and outputs a GalaxyMage map.
		[<image2>]
			(Optional) path of image that contains tile groups data
		[<image3>]
			(Optional) path of image that contains unit coordinate data
		[<map_name>]
			(optional) path of output map file. (.py is appended)

	<template> <width> <height>
		Outputs a template map image
		'''

	# args: load image data
	if arg_num == 2:
		image_load(sys.argv[1])
		map_scale()
		map_write("map-data.py")

	# args: template
	if arg_num == 4 and sys.argv[1] == "template":
		#create image template
		image_template(sys.argv[2], sys.argv[3])

	# end
	print "done."

# main code
main()