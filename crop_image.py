#created by Amy Xu
#crop images

import subprocess
import math
import geopandas as gpd
from osgeo import gdal, ogr

def main():
	strips = open('imgs.txt', 'r').readlines()
	for img in strips:
		name = img.split('.')[0]
		counter = 0
		points_list = open('strip_point/' + name + '.txt').readlines()

		for point in points_list:
			newfile = 'data_img/' + name + '_' + str(counter) + '.tif'
			open(newfile, 'w+')
			coords = point.split(' ')
			dim = corners(float(coords[0]), float(coords[1]))
			
			# this could be factored into a method
			# gdalwarp -te xmin ymin xmax ymax -ts 512 512 -overwrite inpf destf
			call = ('gdalwarp -te ' + str(dim[0]) + ' ' + str(dim[1]) + ' ' 
				+ str(dim[2]) + ' ' + str(dim[3]) + ' -ts 512 512 -overwrite strip_img/' 
				+ img + ' ' + newfile)
			print(call)
			subprocess.run(call, shell = True)
			counter = counter + 1

# 111,111 m = 1 deg LAT, 111,111 * cos(LAT) m = 1 deg LONG
def corners(x, y):
	coords = []
	offset = 100 / 111111

	coords.append(x - offset)
	coords.append(y - offset)
	coords.append(x + offset)
	coords.append(y + offset)
	return coords

if __name__ == '__main__':
	main()
