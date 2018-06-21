#created by Daniel Cao
#create table from coordinates to corresponding tiff
import geopandas as gpd
import pandas as pd
import csv
#load the tomnod geojson file
tomnod = gpd.read_file('digitalglobe_crowdsourcing_hurricane_harvey_20170915.geojson')

tomnod_x = tomnod['geometry'].x
tomnod_y = tomnod['geometry'].y
tomnod['tomnod_x'] = tomnod_x
tomnod['tomnod_y'] = tomnod_y

def processTup(tup):
    return [float(ele) for ele in (tup.strip('()').split(','))]

tifRange = pd.read_csv('tifRange-post-1.csv')
def getTifFromCoor(x, y, catalog):
    for index, row in tifRange.iterrows():
        minxy = processTup(row['minxy'])
        maxxy = processTup(row['maxxy'])
        if x >= minxy[0] and x <= maxxy[0] \
                and y >= minxy[1] and y <= maxxy[1] \
                and catalog == row['catalog_id']:
            return row['tif']
#print(tifRange.head(5))
cat_id_range = dict()

#get range of catalog_id
for catalog_id in tifRange['catalog_id'].unique():
    for index,row in tifRange.iterrows():
        if row['catalog_id'] == catalog_id:
            minx = processTup(row['minxy'])[0]
            miny = processTup(row['minxy'])[1]
            maxx = processTup(row['maxxy'])[0]
            maxy = processTup(row['maxxy'])[1]
            if catalog_id not in cat_id_range:
                cat_id_range[catalog_id] = ((minx,miny),(maxx,maxy))
            else:
                cat_id_range[catalog_id] = ((min(minx,cat_id_range[catalog_id][0][0]),
                                            min(miny,cat_id_range[catalog_id][0][1])),
                                            (max(maxx,cat_id_range[catalog_id][1][0]),
                                             max(maxy,cat_id_range[catalog_id][1][1])))

for k,v in cat_id_range.items():
    print (k,v)
print(tomnod.head(5))
#process tomnod further to recover the missing catalog id
post_event_catalog = ['105001000B95E200', '105001000B95E100', '1040010032211E00']
for index, row in tomnod.iterrows():
    if row['catalog_id'] in post_event_catalog:
        s = row['catalog_id']
        #row['complete_catalog_id'] = s
        tomnod.set_value(index,'complete_catalog_id',s)
        #print("found existing post catalog", s)
    elif row['catalog_id'] == '':
        for k,v in cat_id_range.items():
            if row['tomnod_x'] >= v[0][0] and row['tomnod_x'] <= v[1][0] and \
                     row['tomnod_y'] >= v[0][1] and row['tomnod_y'] <= v[1][1]:
                #row['complete_catalog_id'] = k
                tomnod.set_value(index,'complete_catalog_id',k)
                tomnod.set_value(index,'catalog_id',k)
                print(index)

print(tomnod.loc[tomnod['catalog_id'] == ''])
print(tomnod.loc[tomnod['complete_catalog_id'] == ''])

#be careful when uncomment this
tomnod.to_csv('tomnod_complete-both-columns.csv', encoding='utf-8')
print(tomnod.complete_catalog_id.unique())


#make a complete table for corresponding tif to images of POST EVENT
#this is very costly
#be careful with the output file name 
list_of_post = ['105001000B95E200', '105001000B95E100', '1040010032211E00',
                '105001000B9D8100', '1030010070C13600', '105001000B9D7F00',
                '10400100324DAE00', '1020010065DF2700', '1020010068D6F400',
                '1020010067290D00']
'''
with open('coordinateAndTif-post-3.csv','w') as myFile:
    writer = csv.writer(myFile)
    writer.writerow(['post_catalog_id','post_tif','pre_catalog_id','pre_tif','min_xy','max_xy','x_coord', 'y_coord', 'label'])
    for index, row in tomnod.iterrows():
        print("row in tomnod: ",index)
        if row['complete_catalog_id'] in list_of_post:
            for index_t, row_t in tifRange.iterrows():
                minxy = processTup(row_t['minxy'])
                maxxy = processTup(row_t['maxxy'])
                if row['tomnod_x'] >= minxy[0] and row['tomnod_x'] <= maxxy[0] \
                  and row['tomnod_y'] >= minxy[1] and row['tomnod_y'] <= maxxy[1] and row['catalog_id'] == row_t['catalog_id']:
                    temp = [row['complete_catalog_id'], getTifFromCoor(row['tomnod_x'],row['tomnod_y'],row['complete_catalog_id']),
                        row_t['catalog_id'],getTifFromCoor(row['tomnod_x'],row['tomnod_y'],row_t['catalog_id']),
                        row_t['minxy'], row_t['maxxy'], 
                        row['tomnod_x'], row['tomnod_y'], row['label']]
                    #if (row['catalog_id'] == row_t['catalog_id']):
                    #    temp.append(row['label']) 
                    #else:
                    #    temp.append('non-damaged '+ row['label'])
                    writer.writerow(temp)
                    break
'''
import os
import gdal 
def getRangeTif(tif):
    #print(tif)
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
    if index%1000 == 0:
        print('tomnod row: ',index)
    s = row['complete_catalog_id']
    for file in os.listdir(s+'/'):
        if file.endswith('.tif'):
            minmax = getRangeTif(s+'/'+file) 
            minxy = minmax[0]
            maxxy = minmax[1]
            if row['tomnod_x'] >= minxy[0] and row['tomnod_x'] <= maxxy[0] \
                    and row['tomnod_y'] >= minxy[1] and row['tomnod_y'] <= maxxy[1]:
                #print(file)
                tomnod.set_value(index,'tif',file)
                break

tomnod.to_csv('coordinateAndTif-post-3.csv', encoding='utf-8')

