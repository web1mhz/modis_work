import os
import requests

import re

from bs4 import BeautifulSoup

# params fo LP DAAC
# you will require an EarthData login
host = fr'https://e4ftl01.cr.usgs.gov/MOTA/MCD64A1.061'
login = os.getenv('web1mhz')
password = os.getenv('Web10240214')

# list folders 
r = requests.get(host, verify=True, stream=True,auth=(login,password))
soup = BeautifulSoup(r.text, "html.parser")
folders = list()
for link in soup.findAll('a', attrs={'href': re.compile("\d{4}.\d{2}.\d{2}/")}):
    folders.append(link.get('href'))
print(f"{len(folders)} folders found")