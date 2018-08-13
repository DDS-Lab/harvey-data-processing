"""
created by Daniel Cao
to create bash script to download all the catalog id from the links
download them to their respective catalog folders
"""
POST_EVENT_CAT = 'txt_files/postevent_catalogs.txt'

catalogs = open(POST_EVENT_CAT, 'r').readlines()

for catalog in catalogs:
    print(catalog)
    catalog2 = catalog.strip()
    # Open txt file of the iterated catalog ID 
    link_list = open('txt_files/' + catalog2 + '.txt', 'r').readlines()
    script = open('txt_files/' + catalog2 + '.sh', 'w+')

    # Writes the bash script that makes a directory for a catalog ID, enters it, downloads from the links, and exits dir
    script.write('#!/bin/bash\n')
    script.write('mkdir ' + catalog2 + '\n')
    script.write('cd ' + catalog2 + '\n')
    for link in link_list:
        script.write('wget ' + link + '\n')
    script.write('cd ..')
