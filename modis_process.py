
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



# 모디스 레이어 stack 
out_folder = glob.glob(os.path.join(out_base_folder, product, product_year) + "/*.tif")
print(list(out_folder)) 

# ImageList = ['Band1.tif', 'Band2.tif', 'Band3.tif']  # or use sorted(glob.glob('*.tif')) if input images are sortable

ImageList = list(out_folder)
VRT = 'OutputImage.vrt'
gdal.BuildVRT(VRT, ImageList, separate=True, callback=gdal.TermProgress_nocb)


InputImage = gdal.Open(VRT, 0)  # open the VRT in read-only mode

outputImaage = product + product_year + ".tif"

gdal.Translate(outputImaage, InputImage, format='GTiff',
               creationOptions=['COMPRESS:DEFLATE', 'TILED:YES'],
               callback=gdal.TermProgress_nocb)

del InputImage  # close the VRT

