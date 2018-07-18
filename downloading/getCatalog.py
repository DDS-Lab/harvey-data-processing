# created by Daniel Cao
# get all catalog id into list

# import library
import os

POST_EVENT_DIR = "txt_files/"
POST_EVENT_CAT = "txt_files/postevent_catalogs.txt"

# the directory has all the download shell
file = open(POST_EVENT_CAT, "w")
for filename in os.listdir(POST_EVENT_DIR):
    file.write(filename.split('.')[0])
    file.write('\n')

file.close()	
