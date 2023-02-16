#!/usr/bin/env python
"""
A script to grab timeseries from MODIS data using GDAL and python
Author: J Gomez-Dans/NCEO & UCL
__author__: J Gómez-Dans

"""


import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

plt.ion()
# Read in the landcover data
g = gdal.Open("IGBP.tif")

lc = g.ReadAsArray()

# The different landcover types we are interested in
lc_labels = {1: "Evergreen Needleleaf forest",
             2:    "Evergreen Broadleaf forest",
             3:    "Deciduous Needleleaf forest",
             4:    "Decidious Broadleaf forst",
             5:    "Mixed forest",
             6:    "Closed shrublands",
             7:    "Open shrublands",
             8:    "Woody savannas",
             9:    "Savannas",
             10:   "Grasslands",
             11:   "Permanent wetlands",
             12:   "Croplands",
             14:   "Cropland/Natural vegetation mosaic"}
# Time axis
doys = np.arange(1, 365, 8)

t_axis = np.array([730486. + doys + 365*i for i in range(10)]).flatten()

iplot = 1
# Loop over landcover types
for (class_no, class_label) in lc_labels.items():
    # The landcover filter for this class is calculated now.
    passer_lc = (lc == class_no)
    print(class_label)
    print(passer_lc)  
#     n_years = 0
#     plt.clf()
#     # Remember to clear the screen
#     mean_gpp = []
#     std_gpp = []

#     for year in range(2002, 2012):
#         print(year)
#         # Open the relevant file
#         g = gdal.Open("MOD17A2.%04d.tif" % year)
#         # For eacth time step (ie band)...
#         for tstep in range(g.RasterCount):
#             # Read the data. Note bands start @ 1 in GDAL, not 0
#             gpp = g.GetRasterBand(tstep+1). ReadAsArray()
#             # Scale and filter wrong values
#             gpp = np.where(gpp >= 30000, np.nan, gpp*0.0001)
#             # Filter, where the data are OK, and the landcover is
#             # the one we stipulated above
#             passer = np.logical_and(np.isfinite(gpp),passer_lc)
#             # The pixels that get selected from this date.
#             work = gpp[passer]
#             # Calculate means and standard deviations
#             mean_gpp.append(work.mean())
#             std_gpp.append(work.std())


g = gdal.Open("IGBP.tif")
lc = g.ReadAsArray()
print(g.RasterXSize)

enf = np.where(lc == 1, lc, np.nan)


print(enf)

print("평균", np.mean(enf))

def array_to_raster(array):
    """Array > Raster
    Save a raster from a C order array.
    :param array: ndarray
     """
    dst_filename = 'xxx.tiff'
    x_pixels = g.RasterXSize # number of pixels in x
    y_pixels = g.RasterYSize # number of pixels in y
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(
           dst_filename,
           x_pixels,
           y_pixels,
           1,
           gdal.GDT_Float32, )
    
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()  # Write to disk.

    return dataset, dataset.GetRasterBand(1) 



# array_to_raster(enf)


arr = np.array([[20, 15, 37], [47, 13, np.nan]])

print(np.nanmean(arr))