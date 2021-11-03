import os

import numpy as np
from osgeo import gdal

from src.main.utils import getCloudMask


def getRedArray(hdf_ds, cloud_array):
    dataset_info = hdf_ds.GetSubDatasets()[11]
    band_ds = gdal.Open(dataset_info[0], gdal.GA_ReadOnly)
    band_array = band_ds.ReadAsArray().astype(np.int16)
    cloud_mask = getCloudMask(cloud_array, 0, 1, 0)

    band_array[cloud_mask == 1] = -28672
    band_array[band_array == -28672] = -32768
    band_array[band_array < -100] = -32768
    band_array[band_array > 8000] = -32768

    return band_array

def getGreenArray(hdf_ds, cloud_array):
    dataset_info = hdf_ds.GetSubDatasets()[14]
    band_ds = gdal.Open(dataset_info[0], gdal.GA_ReadOnly)
    band_array = band_ds.ReadAsArray().astype(np.int16)
    cloud_mask = getCloudMask(cloud_array, 0, 1, 0)

    band_array[cloud_mask == 1] = -28672
    band_array[band_array == -28672] = -32768
    band_array[band_array < -100] = -32768
    band_array[band_array > 8000] = -32768

    return band_array

def getBlueArray(hdf_ds, cloud_array):
    dataset_info = hdf_ds.GetSubDatasets()[13]
    band_ds = gdal.Open(dataset_info[0], gdal.GA_ReadOnly)
    band_array = band_ds.ReadAsArray().astype(np.int16)
    cloud_mask = getCloudMask(cloud_array, 0, 1, 0)

    band_array[cloud_mask == 1] = -28672
    band_array[band_array == -28672] = -32768
    band_array[band_array < -100] = -32768
    band_array[band_array > 8000] = -32768

    return band_array

def hdf2rgb(hdf_file, dst_dir):
    hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)

    cloud_ds = gdal.Open(hdf_ds.GetSubDatasets()[18][0], gdal.GA_ReadOnly)
    cloud_array = cloud_ds.ReadAsArray().astype(np.int16)
    # build output path
    band_path = os.path.join(dst_dir,
                             os.path.basename(os.path.splitext(hdf_file)[0]) + "-rgb" + ".tif")
    # write raster
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  cloud_ds.RasterXSize,
                                                  cloud_ds.RasterYSize,
                                                  3,  # Number of bands
                                                  gdal.GDT_Int16)
    out_ds.SetGeoTransform(cloud_ds.GetGeoTransform())
    out_ds.SetProjection(cloud_ds.GetProjection())

    red_array = getRedArray(hdf_ds, cloud_array)
    out_ds.GetRasterBand(1).SetDescription("red")
    out_ds.GetRasterBand(1).WriteArray(red_array)
    out_ds.GetRasterBand(1).SetNoDataValue(-32768)

    green_array = getGreenArray(hdf_ds, cloud_array)
    out_ds.GetRasterBand(2).SetDescription("green")
    out_ds.GetRasterBand(2).WriteArray(green_array)
    out_ds.GetRasterBand(2).SetNoDataValue(-32768)

    blue_array = getBlueArray(hdf_ds, cloud_array)
    out_ds.GetRasterBand(3).SetDescription("blue")
    out_ds.GetRasterBand(3).WriteArray(blue_array)
    out_ds.GetRasterBand(3).SetNoDataValue(-32768)