# created by Amy Xu
# to check coordinates

import geopandas as gpd 
from osgeo import gdal
import requests
import shutil
import os


def main():
    HARVEY_RAW = 'id-catalog/harvey_raws.geojson' # this file name where my raw data is stored
    PATH = 'img/strip_img/' # path should be where you want to store the image. (don't edit the + filename part)
    
    data = gpd.read_file(HARVEY_RAW)
    points = data['geometry'].tolist()

    # this is a text file containing an image link for each strip on each line.
    # you can write code to do this yourself, or contact me for my program.
    NEW_LINKS = "newlinks.txt"
    
    f = open(NEW_LINKS, "r")
    urls = f.readlines()

    for url in urls: # download file
        url = url.strip()
        filename = url.split('/')[-1]

        print(url)
        print(filename)
        
        path = PATH + filename
        r = requests.get(url, stream = True)
        if r.status_code == 200: # 200: OK: add more details
            with open(path, 'wb+') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            coords = get_coords(path)
            if not check_coords(points, coords, filename):
                os.remove(path)
        else:
            print('error:' + r.status_code)


def get_coords(filename):
    ds = gdal.Open(filename)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    coord = [gt[0], gt[3] + width * gt[4] + height * gt[5], gt[0] + width * gt[1] + height * gt[2], gt[3]]# mixmiymxxmxy
    return coord


def check_coords(points, coords, filename):
    IMG_STRIP_PT = 'img/strip_point/'
    
    has_point = False
    # reformat here as well
    name = IMG_STRIP_PT + filename.split('.')[0] + '.txt'
    point_list = open(name, 'w+')
    for point in points:
        if point.x >= coords[0] <= coords[2] and coords[1] <= point.y <= coords[3]:
            point_list.write(str(point.x) + ' ' + str(point.y) + '\n')
            has_point = True
    if not has_point:
        os.remove(name)
    return has_point


if __name__ == '__main__':
    main()
