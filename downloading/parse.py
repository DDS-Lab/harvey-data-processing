"""
created by DDS lab member Amy Xu
modified by Daniel Cao

This script scrapes the Digital Globe Open Data Program Harvey Post-Event site to download the Tif images.
"""

# import library
import requests
from bs4 import BeautifulSoup

# set page
page = "http://www.digitalglobe.com/opendata/hurricane-harvey/post-event"

# initialize instance
req = requests.get(page)
soup = BeautifulSoup(req.content, "html.parser")

# get download links per Catalog ID
for textarea in soup.findAll("textarea"):	
    links_file = open(str(textarea['id']).split('-')[1] + '.txt', 'w+')
    links = textarea.text.split()
    for link in links:
        links_file.write(link + '\n')
