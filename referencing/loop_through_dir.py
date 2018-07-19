# created by Daniel Cao
# get coordinate ranges of catalog ids and tiffs
import gdal
import os
import csv


folders = []
# outfile = open('tifRange.csv', 'w')


def get_range_tif(tif):
    print(tif)
    ds = gdal.Open(tif)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5]
    # from http://gdal.org/gdal_datamodel.html
    maxx = gt[0] + width*gt[1] + height*gt[2]
    # from http://gdal.org/gdal_datamodel.html
    maxy = gt[3]
    range = ((minx, miny), (maxx, maxy))
    return range


# Will loop through all items in the current folder and create a list of folders
for file in os.listdir():
    if os.path.isdir(file):
        folders.append(file)

# Will loop through tifs found in the folders and append the csv file with the folder, file, min, and max values
with open('tifRange-post-1.csv', 'w') as myFile:
    writer = csv.writer(myFile)
    for folder in folders:
        # folder is the folder name
        print(folder)
        for file in os.listdir(folder+'/'):
            if file.endswith('.tif'):
                try:
                    # print(file)
                    temp = [folder, file]
                    minmax = get_range_tif(folder + '/' + file)
                    temp.append(minmax[0])
                    temp.append(minmax[1])
                    writer.writerow(temp)
                except Exception:
                    pass
