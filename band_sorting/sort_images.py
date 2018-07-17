import gdal
import os
import shutil

BAND_NUM = 3
POST_EVENT_DIR = "/Volumes/My Book/Harvey/postevent/images"
POST_EVENT_SORT3BAND = '/Volumes/My Book/Harvey/postevent/sorted_images/3_band/'
POST_EVENT_SORT1BAND = '/Volumes/My Book/Harvey/postevent/sorted_images/1_band/'

for date in os.listdir(POST_EVENT_DIR):
    print (date)
    os.chdir(POST_EVENT_DIR+date)
    for folder in os.listdir(POST_EVENT_DIR+date):
        os.chdir(POST_EVENT_DIR+date+"/"+folder)
        for img in os.listdir(POST_EVENT_DIR+date+"/"+folder):
            if img.split('.')[-1] == 'tif':
                image = gdal.Open(img)
                number_of_bands = image.RasterCount
                if number_of_bands == BAND_NUM:
                    new_path = (POST_EVENT_SORT3BAND+date+'_'+folder+'_'+img)
                    shutil.copy(img, new_path)
                    print ('copied ' + img + ' to ' + new_path)
                else:
                    new_path = (OST_EVENT_SORT1BAND+date+'_'+folder+'_'+img)
                    shutil.copy(img, new_path)
