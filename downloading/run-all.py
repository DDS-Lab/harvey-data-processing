"""
created by Daniel Cao
write a bash script to download all catalogs at once
the bash script calls each smaller script to run and download by creating a list of .sh files to execute
"""

import os

RUN_POST = 'run-all-post.sh'
POST_EVENT_DIR = "/Users/danielcao/Downloads/DDS/postevent"

my_file = open(RUN_POST, 'w')

#this line is required for hyak run an automated job
my_file.write('#!/bin/bash')
for filename in os.listdir(POST_EVENT_DIR):
    if filename.endswith(".sh"):
        my_file.write('./' + filename + '\n')

my_file.close()
