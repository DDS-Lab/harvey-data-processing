#created by Daniel Cao
#crop images with specific pixel size from tiff

import osgeo
import gdal
import numpy as np
import pandas as pd
import geopandas as gpd
import csv
import os

def get_geoinfo(ds):
    width = ds.RasterXSize
    height = ds.RasterYSize

    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5]  

    maxx = gt[0] + width*gt[1] + height*gt[2]  

    maxy = gt[3]

    print(minx,miny,maxx,maxy) 

size = 0.000897575
count = 0
fail = 0
coordinate_tif_3 = pd.read_csv('coordinateAndTif-post-3.csv')
for index, row in coordinate_tif_3.iterrows():
    if row['label'] == 'Flooded / Damaged Building':
        folder = row['complete_catalog_id']
        tif = row['tif']
        xmin = row['tomnod_x'] - size
        xmax = row['tomnod_x'] + size
        ymin = row['tomnod_y'] - size
        ymax = row['tomnod_y'] + size
        #print('{} {} {} {}'.format(xmin, ymin, xmax, ymax))
        file_name_to_write = str(row['tomnod_x'])+'_'+str(row['tomnod_y'])+'.jpeg'
        print('{} {}'.format(folder, tif))
        try:
            ds = gdal.Open(''+folder+'/'+tif)
                    #get_geoinfo(ds) 
            os.chdir('cropped-post-400/') 
            #print(os.getcwd())
            try:
                gdal.Translate(file_name_to_write,ds, projWin = [xmin, ymin+2*size, xmax, ymax-2*size],format = 'jpeg') 
                #print("Crop success")
            except:
                print("Crop failure")
                pass
            os.chdir('../')
            #print(os.getcwd())
            #print("finish")
            count += 1
        except:
            print("something wrong with gdal open")
            fail += 1
            pass
        
        print("total number of cropped images: ", count)
        print("total number of failed images: ", fail)
print("finish")
