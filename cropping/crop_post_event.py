"""
created by Daniel Cao
crop images with specific pixel size from tiff based on the center points of the damage annotated in tomnod
"""


import gdal
import pandas as pd
import os

SIZE = 0.000897575  # used to get exactly 400x400 images (maybe???) hyak: 0.000574448
COUNT = 0
FAIL = 0
COOR_TIF_POST = 'coordinateAndTif-post-3.csv'

coordinate_tif_3 = pd.read_csv(COOR_TIF_POST)
for index, row in coordinate_tif_3.iterrows():
    if row['label'] == 'Flooded / Damaged Building':
        folder = row['complete_catalog_id']
        tif = row['tif']
        xmin = row['tomnod_x'] - SIZE
        xmax = row['tomnod_x'] + SIZE
        ymin = row['tomnod_y'] - SIZE
        ymax = row['tomnod_y'] + SIZE
        file_name_to_write = str(row['tomnod_x'])+'_'+str(row['tomnod_y'])+'.jpeg'
        print('{} {}'.format(folder, tif))
        try:
            ds = gdal.Open(''+folder+'/'+tif)
            os.chdir('cropped-post-400/')
            try:
                gdal.Translate(file_name_to_write, ds,
                               projWin=[xmin, ymin + 2 * SIZE, xmax, ymax - 2 * SIZE], format='jpeg')
            except:
                print("Crop failure")
                pass
            os.chdir('../')
            COUNT += 1
        except:
            print("something wrong with gdal open")
            FAIL += 1
            pass
        
        print("total number of cropped images: ", COUNT)
        print("total number of failed images: ", FAIL)
print("finish")
