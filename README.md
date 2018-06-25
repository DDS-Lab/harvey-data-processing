# harvey-data-processing
For processing of data in the Hurricane Harvey project

Process flow:
1. parse.py
2. getCatalog.py
3. script.py
4. run-all.py

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
  
 