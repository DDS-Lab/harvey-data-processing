# harvey-data-processing
For processing of data in the Hurricane Harvey project

Folder Arrangement (Hyak):  
1. DSSG (I assume ran locally)  
    a. crop_post_event.py  
    b. run-all.py  
    c. test.py  
    d. loopThroughDir.py  
    e. script.py  
    f. tomnod.py
2. dds  
    a. Crop.py  
    b. Crop_image.py  
    c. loopThroughDir.py  
    e. *anaconda3*  
    f. *core.3459*  
    g. *crop_pre*  
    h. *damage_data.csv*  
    i. *non_damage_data.csv*  
    j. *postevent*  
    k. *preevent*  
    l. *readme*  
    m. *run.slurm*  
    n. *run_all.sh*  
    o. *slurm-167806.out*  
    p. *tifRange.csv*  
    q. *tifRange1.csv*  
3. img  
    a. crop_img.py
    
Folder Arrangement (GitHub Repo):
1. cropping 
2. data
3. downloading  
    a. parse.py  
    b. getCatalog.py  
    c. script.py  
    d. run-all.py
4. notebooks
5. referencing  
    a. loop_through_dir.py  
    b. tomnod.py  
6. band_sorting
    a. sort_images.py

Process flow:
1. parse.py
2. getCatalog.py
3. script.py
4. run-all.py
5. loop_through_dir.py  
6. tomnod.py
7. crop_post_event.py

Script Documentation

* parse.py  
This script works to pull html links from Digital Globe's Open Data Program
on hurricane Harvey. You must open the script to change the link if you would 
like to download another event's data.  
*Input:* html link (in script)  
*Output:* txt files with html links inside (each file is one Catalog ID)

* getCatalog.py  
This script will loop through the txt files that were given as output
from parse.py and will get the IDs to be stored in a separate list.  
*Input:* txt files from parse.py  
*Output:* postevent_catalogs.txt (this is an input file for script.py)

* script.py   
This script will loop through each Catalog ID in the output file from
getCatalog.py and write a bash script to download the images into separate
folders.  
*Input:* postevent_catalogs.txt, txt files from parse.py  
*Output:* bash scripts (.sh, each script is for one Catalog ID)
  
* run-all.py  
This script will create a bash script to run through all the individual
bash scripts created by script.py in order to download all the images
without the need to individually call all scripts. This script should be
run in the outer folder of the directory where you wish the individual
folders containing tifs will be saved.  
*Input:* bash scripts from script.py  
*Output:* run-all-post.sh
  
* loop_through_dir.py  
This script goes through all the Tif files in order to find the coordinate ranges 
of each and saves it in a csv file.  
*Input:* tif files in folders  
*Output:* tifRange-post-1.csv

* tomnod.py  
This script goes through the TomNod GeoJSON file and creates a table that matches the
point to the specific tif file that it exists in. This also goes through all the tif
files to locate points that did not have the catalog ID indicated.    
*Input:* digitalglobe_crowdsourcing_hurricane_harvey_20170915.geojson, tifRange-post-1.csv  
*Output:* coordinateAndTif.csv  

* crop_post_event.py  
This script goes through the coordinateAndTif.csv reference file to crop the tiff images
based on a determined, fixed pixel size.  
*Input:* coordinateAndTif.csv  
*Output:* jpeg images

* sort_images.py
This script separates the 3-band from the 1-band images and renames the files in a
date_catalogid_img name format.
*Input:* Tiff images in folders
*Output:* Band Sorted images in folders