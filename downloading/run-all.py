"""
created by Daniel Cao
write a bash script to download all catalogs at once
the bash script calls each smaller script to run and download by creating a list of .sh files to execute
"""

import os

my_file = open('run-all-post.sh', 'w')
my_file.write('#!/bin/bash')
for filename in os.listdir("/Users/danielcao/Downloads/DDS/postevent"):
    if filename.endswith(".sh"):
        my_file.write('./' + filename + '\n')

my_file.close()
