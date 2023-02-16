
# MODIS 자료 리스트 만들기
# 집: 콘다 가상환경 : tg38


from datetime import datetime, date, timedelta
from lxml import etree
from io import StringIO
import requests
import time
import os
import pathlib

import pandas as pd


# baseurls = ['https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGM.06/',
#             'https://e4ftl01.cr.usgs.gov/MOLA/MYD13C1.006/',
#             'https://e4ftl01.cr.usgs.gov/MOLT/MOD13C1.006/',
#             'https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.007/']


# GPM: Monthly Global Precipitation Measurement (GPM) v6
# baseurls = 'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGM.06/'

# SMAP Enhanced L3 Radiometer Global Daily 9 km EASE-Grid Soil Moisture, Version 4 (SPL3SMP_E)
# baseurls ='https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.007/'

# MOD15A2H - fpar/LAI 데이터 - MCD15A2H MODIS/Terra+Aqua Leaf Area Index/FPAR 8-day L4 Global 500m SIN Grid V061.
# baseurls = ['https://e4ftl01.cr.usgs.gov/MOTA/MCD15A2H.061/']

# MYD13C1 - MODIS/Aqua Vegetation Indices 16-Day L3 Global 0.05Deg CMG
# baseurls = ["https://e4ftl01.cr.usgs.gov/MOLA/MYD13C1.061/"]

# modis landcover
# baseurls = ["https://e4ftl01.cr.usgs.gov/MOTA/MCD12Q1.061/"]

# MOD17A3HGF - NPP 데이터
# baseurls = ['https://e4ftl01.cr.usgs.gov/MOLT/MOD17A3HGF.061/']

# MOD17A2HGF - GPP 데이터
baseurls = ["https://e4ftl01.cr.usgs.gov/MOLT/MOD17A2HGF.061/"]


# MOD13A2 - NDVI 데이터 - Vegetation Indices 16-Day L3 Global 1km
# baseurls = ['https://e4ftl01.cr.usgs.gov/MOLT/MOD13A2.061/']

year = '2021'
hv_tile = 'h28v05'
modis_product = 'MOD17A2'


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
    for fmt, substr in [('%Y.%m.%d', l[0:10]), ('%Y', l[0:4])]:
        try:
            d = datetime.strptime(substr, fmt).date()
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


# modis 파일 다운리스트 작성

for url in baseurls:
    session = requests.Session()
    basedir = pathlib.PurePath(url).name
    # print(basedir)

    links = getLinks(url)
    # print(links)

    ldates = [l for l in links if isDate(l)]
    # print(ldates)

    hdf_list = []
    xml_list = []

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

                if hv_tile in filepath:
                    # print(filepath)
                    if pathlib.Path(filepath).is_file():
                        print("File exists: " + filepath)
                    else:
                        # print("File doesn't exist: " + filepath )

                        print("Downloading... " + url + d + f)
                        # print('xml filepath', url + d + f + '.xml')

                        hdf_list.append(url + d + f)
                        xml_list.append(url + d + f + ".xml")

    pd.DataFrame(hdf_list).to_csv(
        f"{modis_product}_hdf_list_{year}.csv", index=False, header=None)
    pd.DataFrame(xml_list).to_csv(
        f"{modis_product}_xml_list_{year}.csv", index=False, header=None)
