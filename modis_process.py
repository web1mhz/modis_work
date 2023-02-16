import os

from osgeo import gdal
import glob

from pathlib import PurePath
import matplotlib.pyplot as plt

# 집
# url = r"C:\Users\DeepGIS\Desktop\modis_work\mod13a2v600_ndvi"

# 사무소
url = r"C:\Users\TETRA\Desktop\modis_work\mod13a2v600_ndvi"
years = os.listdir(url)

#  집
# out_base_folder = r"C:\Users\DeepGIS\Desktop\modis_work\tif_file"

# 사무소
out_base_folder = r"C:\Users\TETRA\Desktop\modis_work\tif_file"


product = "NDVI"
product_year = "A2020"

# 여러개의 HDF 파일을 하나씩 좌표계를 변환하는 함수
def sinusoida2wgs84(in_file, product, product_year):

    in_file = in_file
    product = product
    product_year = product_year

    out_folder = os.path.join(out_base_folder, product, product_year)

    if not os.path.isdir(out_folder):
        os.makedirs(out_folder, exist_ok=True)

    out_file = os.path.join(out_folder, PurePath(
        in_file).name.split('.hdf')[0] + ".tif")
    print(out_file)

    # open dataset
    dataset = gdal.Open(in_file, gdal.GA_ReadOnly)
    subdataset = gdal.Open(dataset.GetSubDatasets()[0][0], gdal.GA_ReadOnly)

    # gdalwarp
    kwargs = {'format': 'GTiff', 'dstSRS': 'EPSG:4326'}
    ds = gdal.Warp(destNameOrDestDS=out_file,
                   srcDSOrSrcDSTab=subdataset, **kwargs)
    del ds

    ndvi_data = gdal.Open(out_file)
    array = ndvi_data.GetRasterBand(1).ReadAsArray()

    # plt.figure
    # plt.imshow(array)
    # plt.show()

for year in years:
    url_year = os.path.join(url, year)
    # print(url_year)

    hdf_files = glob.glob(url_year + "/*.hdf")
    # print(hdf_file)

    for hdf_file in hdf_files:
        if product_year in hdf_file:
            print(f"좌표변환 중 {hdf_file}>>>>>>")
            # sinusoida2wgs84(hdf_file, product, product_year)


# 하나의 HDF 파일의 좌표계를 변환하기
# IGBP 분류체계의 2021년 토지피복도를 sinusoidal 좌표계를 wgs84좌표계로 변환하여 저장
hdf_file = 'MCD12Q1_landcover/MCD12Q1.A2021001.h28v05.061.2022216154624.hdf'
product = 'Landcover'
product_year= "2021"

sinusoida2wgs84(hdf_file, product, product_year)


# 좌표변환된 MODiS 데이터를 날짜 순서대로 층층이 겹쳐 만드는 stack 
out_folder = glob.glob(os.path.join(out_base_folder, product, product_year) + "/*.tif")
print(list(out_folder)) 

# ImageList = ['Band1.tif', 'Band2.tif', 'Band3.tif']  # or use sorted(glob.glob('*.tif')) if input images are sortable

def modis_stack(out_folder):

    ImageList = list(out_folder)
    VRT = 'OutputImage.vrt'
    gdal.BuildVRT(VRT, ImageList, separate=True, callback=gdal.TermProgress_nocb)

    InputImage = gdal.Open(VRT, 0)  # open the VRT in read-only mode

    outputImaage = product + product_year + ".tif"

    gdal.Translate(outputImaage, InputImage, format='GTiff',
                creationOptions=['COMPRESS:DEFLATE', 'TILED:YES'],
                callback=gdal.TermProgress_nocb)

    del InputImage  # close the VRT

