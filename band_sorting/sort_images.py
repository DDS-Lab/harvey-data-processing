import gdal
import os
import shutil

BAND_NUM = 3

for date in os.listdir("/Volumes/My Book/Harvey/postevent/images"):
    print (date)
    os.chdir("/Volumes/My Book/Harvey/postevent/images/"+date)
    for folder in os.listdir("/Volumes/My Book/Harvey/postevent/images/"+date):
        os.chdir("/Volumes/My Book/Harvey/postevent/images/"+date+"/"+folder)
        for img in os.listdir("/Volumes/My Book/Harvey/postevent/images/"+date+"/"+folder):
            if img.split('.')[-1] == 'tif':
                image = gdal.Open(img)
                number_of_bands = image.RasterCount
                if number_of_bands == BAND_NUM:
                    new_path = ('/Volumes/My Book/Harvey/postevent/sorted_images/3_band/'+date+'_'+folder+'_'+img)
                    shutil.copy(img, new_path)
                    print ('copied ' + img + ' to ' + new_path)
                else:
                    new_path = ('/Volumes/My Book/Harvey/postevent/sorted_images/1_band/'+date+'_'+folder+'_'+img)
                    shutil.copy(img, new_path)
