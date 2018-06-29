# by Amy Xu

import subprocess
from joblib import Parallel, delayed
# ipyparallel


def main():
    # imgs is a text file containing a list of tif files which contain the points
    # (center) for the images that will be cropped.
    strips = open('imgs.txt', 'r').readlines()
    for img in strips:
        name = img.split('.')[0] # this gives us the name of the file.
        # this will open a text file containing the points for the images to be
        # cropped from the current substrip.
        points_list = open('strip_point/' + name + '.txt').readlines()

        # parallelizes the cropping process. n_jobs would be the number of cpus
        # available. this uses the multiprocess parallelism.
        Parallel(n_jobs=2)(delayed(crop(name, point)) for points in points_list)


# name:  substrip name
# point: point to crop 
def crop(name, point):
    # name of the new cropped image. the str(point) part is just a filler, will
    # be replaced with a more meaningful naming scheme later.
    newfile = 'data_img/' + name + '_' + str(point) + '.tif'
    open(newfile, 'w+')
    coords = point.split(' ') # splits point into x and y coordinate
    dim = corners(float(coords[0]), float(coords[1]))

    # command line syntax:
    # gdalwarp -te xmin ymin xmax ymax -ts 512 512 -overwrite inpf destf
    # change as needed to get the proper image sizes, options, etc.
    call = ('gdalwarp -te ' + str(dim[0]) + ' ' + str(dim[1]) + ' '
    + str(dim[2]) + ' ' + str(dim[3]) + ' -ts 512 512 -overwrite strip_img/'
    + img + ' ' + newfile)

    # this line below can be uncommented to see your progress, and to help debug.
    # print(call)
    subprocess.run(call, shell = True)


# conversion: 111,111 m = 1 deg LAT, 111,111 * cos(LAT) m = 1 deg LONG
# gives the corners of an image that has the given (x,y) point as its center.
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