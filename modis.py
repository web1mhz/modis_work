from osgeo import gdal
import os


folder = 'C:/Users/Javier/Pecaries'
hdf_file = 'C:/Users/Javier/Pecaries/MOD021KM.A2020114.1445.061.2020115011536.hdf'

# open the dataset
hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)
subdatasets = hdf_ds.GetSubDatasets()

for i in range(0, len(subdatasets)+1):
    subdataset_name = subdatasets[i][0]
    band_ds = gdal.Open(subdataset_name, gdal.GA_ReadOnly)
    band_path = os.path.join(folder, 'band{0}.tif'.format(i))
    if band_ds.RasterCount > 1:
        for j in range(1, band_ds.RasterCount + 1):
            band = band_ds.GetRasterBand(j)
            band_array = band.ReadAsArray()

    else:
        band_array = band_ds.ReadAsArray()
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  band_ds.RasterXSize,
                                                  band_ds.RasterYSize,
                                                  1,
                                                  gdal.GDT_Int16,
                                                  ['COMPRESS=LZW', 'TILED=YES'])
    out_ds.SetGeoTransform(band_ds.GetGeoTransform())
    out_ds.SetProjection(band_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(band_array)
    out_ds.GetRasterBand(1).SetNoDataValue(-32768)
