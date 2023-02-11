

from datetime import datetime, date, timedelta
from lxml import etree
from io import StringIO
import requests
import time
import os
import pathlib

from requests.auth import HTTPBasicAuth  

import pandas as pd



# baseurls = ['https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGM.06/',
#             'https://e4ftl01.cr.usgs.gov/MOLA/MYD13C1.006/', 
#             'https://e4ftl01.cr.usgs.gov/MOLT/MOD13C1.006/',
#             'https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.007/'] 

baseurls = ['https://e4ftl01.cr.usgs.gov/MOLT/MOD13A2.006/']

year = '2020'
hv_tile = 'h28v05'

def getLinks(url):
   
    print("Getting links from: " + url)
    page = session.get(url)
    print("페이지", page)

    html = page.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=etree.HTMLParser())
    refs = tree.xpath("//a")    
    return list(set([link.get('href', '') for link in refs]))

def isDate(l):
    isDate = False
    for fmt,substr in [('%Y.%m.%d',l[0:10]), ('%Y',l[0:4])]:
        try:
            d = datetime.strptime(substr,fmt).date()
            return True
        except ValueError:
            isDate = False
    return False

def isHDFFile(l):
    ext = ['.HDF5', '.H5', '.HDF']
    return any([l.lower().endswith(e.lower()) for e in ext])

def isXMLFile(x):
    ext = ['.XML']
    return any([x.lower().endswith(e.lower()) for e in ext])      

for url in baseurls: 
    session = requests.Session()   
    session.auth = ("web1mhz", "Web10240214")
    basedir = pathlib.PurePath(url).name 
    # print(basedir)

    links = getLinks(url)
    # print(links)
    
    ldates = [l for l in links if isDate(l)]
    # print(ldates)

    hdf_list=[]
    xml_list=[]
    
    # path와 row를 지정해서 파일 다운로드       
    for d in ldates:
        if year in d:   
            links_date = getLinks(url + d)
            l_hdf = [l for l in links_date if isHDFFile(l)]
            xml = [x for x in links_date if isXMLFile(x)]
            
            for f in l_hdf:
                folder = basedir + '/' + d
                filepath = folder + f
                xmlfilepath = folder + f + '.xml'
                xmlfile = f + '.xml'

                # print('folder', folder)
                # print('d', d)
                # print('파일패스', filepath)
                # print('xml 패스',xmlfilepath)
                # print(f)
                # 
                # print('xml filepath', url + d + f + '.xml')                      

                if hv_tile in filepath:  
                    # print(filepath)
                    if pathlib.Path(filepath).is_file():
                        print ("File exists: " + filepath )
                    else:
                        # print("File doesn't exist: " + filepath )                   
                                        
                        print("Downloading... " + url + d + f)
                        # print('xml filepath', url + d + f + '.xml')

                        # hdf_list.append(f"<a class ='link' href='{url + d + f}'>modis</a>")
                        # xml_list.append(f"<a class ='link' href='{url + d + f}.xml'>modis</a>")

                        hdf_list.append(url + d + f)
                        xml_list.append(url + d + f + ".xml")

                        # print("Downloading... ", hdf_list)                       

                        # f = session.get(url + d + f)
                        # f.auth = ("web1mhz", "Web10240214")
                        # time.sleep(1)
                        # pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
                        # open(filepath, 'wb').write(f.content)

                        # xml_f = session.get(url + d + xmlfile)
                        # time.sleep(1)
                        # pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
                        # open(xmlfilepath, 'wb').write(xml_f.content)

    pd.DataFrame(hdf_list).to_csv(f"hdf_list_{year}.csv", index=False, header=None) 
    pd.DataFrame(xml_list).to_csv(f"xml_list_{year}.csv", index=False, header=None)                 


    # 전체 파일 다운로드
    # for d in ldates:
    #     links_date = getLinks(url + d)
    #     l_hdf = [l for l in links_date if isHDFFile(l)]
    #     for f in l_hdf:
    #         folder = basedir + '/' + d
    #         filepath = folder + f
    #         if pathlib.Path(filepath).is_file():
    #             print ("File exists: " + filepath )
    #         else:
    #             print("File doesn't exist: " + filepath )
    #             print("Downloading... " + url + d + f)
    #             f = session.get(url + d + f)
    #             time.sleep(1)
    #             pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    #             open(filepath, 'wb').write(f.content)
        