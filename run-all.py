#created by Daniel Cao
#write a bash script to download all catalogs at once

import os

file = open('run-all-post.sh','w')
file.write('#!/bin/bash')
for filename in os.listdir("/Users/danielcao/Downloads/DDS/postevent"):
	if filename.endswith(".sh"):
		file.write('./'+filename+'\n')

file.close()
