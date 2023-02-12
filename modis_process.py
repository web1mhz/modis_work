from osgeo import gdal
import matplotlib.pyplot as plt

gdal_dataset = gdal.Open(
    "MOD17A3HGF061_npp/MOD17A3HGF.A2015001.h28v05.061.2021351205520.hdf")

sub_dataset = gdal_dataset.GetSubDatasets()

for idx, sub in enumerate(sub_dataset):
    print(idx, sub)


print("서브데이터", sub_dataset[0][0])

# npp_data = gdal.Open(
#     'HDF4_EOS:EOS_GRID:"MOD17A3HGF061_npp/MOD17A3HGF.A2015001.h28v05.061.2021351205520.hdf":MOD_Grid_MOD17A3H:Npp_500m')

npp_data = gdal.Open(sub_dataset[0][0])

npp = npp_data.ReadAsArray()

print(npp/10000)

plt.imshow(npp, interpolation='nearest', vmin=0, cmap=plt.cm.gist_earth)

plt.show()


# print(npp_data.GetGeoTransform())
# print(npp_data.GetMetadata())
# print(npp_data.RasterCount)
# print(npp_data.GetRasterBand(1))
# print(npp_data.GetProjectionRef())
