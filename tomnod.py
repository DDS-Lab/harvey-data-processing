"""
created by Daniel Cao
This script creates a table from coordinates to corresponding tif images where you can find those coordinates and
will look for the catalog IDs of those which are missing that information

Steps:
1. Loads the tomnod geojson file and tifRange file
2. Cleans the list of catalog IDs into a column called 'complete_catalog_id'
3. Creates a reference table for the damage points <-> tif file
"""

import gdal
import geopandas as gpd
import os
import pandas as pd

# load the tomnod geojson file, TOMNOD = GEOJSON & tifRange file
tomnod = gpd.read_file('digitalglobe_crowdsourcing_hurricane_harvey_20170915.geojson')
tifRange = pd.read_csv('tifRange-post-1.csv')


# splitting coordinates to different callable variables
tomnod_x = tomnod['geometry'].x
tomnod_y = tomnod['geometry'].y
tomnod['tomnod_x'] = tomnod_x
tomnod['tomnod_y'] = tomnod_y


# convert the lat lng tuple into individual floats
def process_tup(tup):
    return [float(ele) for ele in (tup.strip('()').split(','))]


# dictionary that will store all the lat lng ranges of each catalog ID
cat_id_range = dict()

# get lat lng range of catalog_id (corner points), iterate over the tifs in order to get the catalog's range
for catalog_id in tifRange['catalog_id'].unique():
    for index,row in tifRange.iterrows():
        if row['catalog_id'] == catalog_id:
            minx = process_tup(row['minxy'])[0]
            miny = process_tup(row['minxy'])[1]
            maxx = process_tup(row['maxxy'])[0]
            maxy = process_tup(row['maxxy'])[1]
            if catalog_id not in cat_id_range:
                cat_id_range[catalog_id] = ((minx,miny),(maxx,maxy))
            else:
                # get the minimum and maximum and save that as the lat lng range
                cat_id_range[catalog_id] = ((min(minx,cat_id_range[catalog_id][0][0]),
                                            min(miny,cat_id_range[catalog_id][0][1])),
                                            (max(maxx,cat_id_range[catalog_id][1][0]),
                                             max(maxy,cat_id_range[catalog_id][1][1])))

# known catalogs that exist in the data set
POST_EVENT_CATALOG = ['105001000B95E200', '105001000B95E100', '1040010032211E00']

# process tomnod further to recover the missing catalog id by creating a new column 'complete_catalog_id"
for index, row in tomnod.iterrows():
    # checks to see if the catalog IDs are indicated,
    if row['catalog_id'] in POST_EVENT_CATALOG:
        s = row['catalog_id']
        tomnod.set_value(index, 'complete_catalog_id', s)
    # tries to locate missing catalog IDs
    elif row['catalog_id'] == '':
        # v = x value, k = y value
        for k,v in cat_id_range.items():
            # checks to see if the point is within the range of the catalog ID and stores it where it is found
            if v[0][0] <= row['tomnod_x'] <= v[1][0] and v[0][1] <= row['tomnod_y'] <= v[1][1]:
                tomnod.set_value(index,'complete_catalog_id',k)
                tomnod.set_value(index,'catalog_id',k)
                print(index)


# make a complete table for corresponding tif to images of POST EVENT
# this is very costly
# be careful with the output file name
def get_range_tif(tif):
    # print(tif)
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
    range = ((minx,miny),(maxx,maxy))
    return range


for index, row in tomnod.iterrows():
    if index % 1000 == 0:
        print('tomnod row: ',index)
    s = row['complete_catalog_id']
    for file in os.listdir(s+'/'):
        if file.endswith('.tif'):
            minmax = get_range_tif(s + '/' + file)
            minxy = minmax[0]
            maxxy = minmax[1]
            if minxy[0] <= row['tomnod_x'] <= maxxy[0] \
                    and minxy[1] <= row['tomnod_y'] <= maxxy[1]:
                # print(file)
                tomnod.set_value(index,'tif',file)
                break

tomnod.to_csv('coordinateAndTif.csv', encoding='utf-8')

