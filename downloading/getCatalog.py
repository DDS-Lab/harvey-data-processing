# created by Daniel Cao
# get all catalog id into list

# import library
import os
# the directory has all the download shell
file = open("postevent_catalogs.txt", "w")
for filename in os.listdir("/Users/danielcao/Downloads/DDS/postevent"):
    file.write(filename.split('.')[0])
    file.write('\n')

file.close()	
