import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal


# Read in the landcover data
g = gdal.Open(
    r"C:\Users\DeepGIS\Desktop\modis_work\MCD12Q1_landcover\MCD12Q1.A2021001.h28v05.061.2022216154624.hdf")

# print(g.GetSubDatasets())

# for subdata in g.GetSubDatasets():
#     print(subdata)

lc_type_01 = g.GetSubDatasets()[0]


lc = gdal.Open(lc_type_01[0])

print(lc)
lc_01 = lc.ReadAsArray()

print(lc_01)

plt.figure
plt.imshow(lc_01)
plt.show()


def arcTotiff(in_asc, out_tif):
    in_asc = in_asc
    out_tif = out_tif

    drv = gdal.GetDriverByName("GTiff")
    ds_in = gdal.Open(in_asc)
    print(ds_in)
    proj = ds_in.GetProjection()

    ds_out = drv.CreateCopy(out_tif, ds_in)

    # srs = osr.SpatialReference()
    # srs.ImportFromEPSG(4326)
    # ds_out.SetProjection(srs.ExportToWkt())

    ds_out.SetProjection(proj)

    ds_in = None
    ds_out = None


out_tif = "igbp.tif"
arcTotiff(lc_type_01[0], out_tif)


# The different landcover types we are interested in
# lc_labels = {1: "Evergreen Needleleaf forest",
#              2:    "Evergreen Broadleaf forest",
#              3:    "Deciduous Needleleaf forest",
#              4:    "Decidious Broadleaf forst",
#              5:    "Mixed forest",
#              6:    "Closed shrublands",
#              7:    "Open shrublands",
#              8:    "Woody savannas",
#              9:    "Savannas",
#              10:   "Grasslands",
#              11:   "Permanent wetlands",
#              12:   "Croplands",
#              14:   "Cropland/Natural vegetation mosaic"}
# # Time axis
# doys = np.arange(1, 365, 8)

# print(doys)

# t_axis = np.array([730486. + doys + 365*i for i in range(10)]).flatten()

# print(t_axis)

# for year in range(2002, 2012):
#     print(year)
