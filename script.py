#created by Daniel Cao
#to create bash script to download all the catalog id from the links 
#download them to their respective catalog folders

catalogs = open('postevent_catalogs.txt', 'r').readlines()

for catalog in catalogs:
	print(catalog)
	catalog2 = catalog.strip()
	link_list = open(catalog2 + '.txt', 'r').readlines()
	script = open(catalog2 + '.sh', 'w+')

	script.write('#!/bin/bash\n')
	script.write('mkdir ' + catalog2 + '\n')
	script.write('cd ' + catalog2 + '\n')
	for link in link_list:
		script.write('wget ' + link + '\n')
	script.write('cd ..')