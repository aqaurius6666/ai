import os

import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

from src.main.utils import getCloudMask

def ndwi(tiff_file, dst_dir):
    tiff_ds = gdal.Open(tiff_file, gdal.GA_ReadOnly)

    # build output path
    band_path = os.path.join(dst_dir,
                             os.path.basename(os.path.splitext(tiff_file)[0]) + "-ndwi" + ".tiff")
    # write raster
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  tiff_ds.RasterXSize,
                                                  tiff_ds.RasterYSize,
                                                  1,  # Number of bands
                                                  gdal.GDT_Float32)
    out_ds.SetGeoTransform(tiff_ds.GetGeoTransform())
    out_ds.SetProjection(tiff_ds.GetProjection())

    tiff_array = tiff_ds.ReadAsArray()
    nir_array = tiff_array[1].astype(np.float)
    nir_array[nir_array == -32768] = np.NaN

    green_array = tiff_array[3].astype(np.float)
    green_array[green_array == -32768] = np.NaN

    ndwi_array = (nir_array - green_array) / (green_array + nir_array)
    ndwi_array[ndwi_array == np.NaN] = -32768

    plt.figure()
    plt.imshow(ndwi_array)
    plt.show()

    out_ds.GetRasterBand(1).SetDescription("ndwi")
    out_ds.GetRasterBand(1).WriteArray(ndwi_array)
    out_ds.GetRasterBand(1).SetNoDataValue(-32768)

def ndwi_mean(tiff_dir, dst_dir):
    array_list = []
    tiff_files = os.listdir(tiff_dir)
    tiff_ds = gdal.Open(os.path.join(tiff_dir, tiff_files[0]), gdal.GA_ReadOnly)

    for tiff_file in tiff_files:
        if os.path.basename(os.path.splitext(tiff_file)[1]) != ".tif":
            continue
        tiff_ds = gdal.Open(os.path.join(tiff_dir, tiff_file), gdal.GA_ReadOnly)
        tiff_array = tiff_ds.ReadAsArray()
        nir_array = tiff_array[1].astype(np.float)
        nir_array[nir_array == -32768] = np.NaN

        green_array = tiff_array[3].astype(np.float)
        green_array[green_array == -32768] = np.NaN

        ndwi_array = (nir_array - green_array) / (green_array + nir_array)

        array_list.append(ndwi_array)


    # build output path
    band_path = os.path.join(dst_dir, "ndwi-mean" + ".tiff")
    # write raster
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  tiff_ds.RasterXSize,
                                                  tiff_ds.RasterYSize,
                                                  1,  # Number of bands
                                                  gdal.GDT_Float32)
    out_ds.SetGeoTransform(tiff_ds.GetGeoTransform())
    out_ds.SetProjection(tiff_ds.GetProjection())
    array_list = np.vstack(array_list)
    ndwi_mean_array = np.mean(array_list)
    ndwi_mean_array[ndwi_mean_array == np.NaN] = -32768
    out_ds.GetRasterBand(1).SetDescription("ndwi-mean")
    out_ds.GetRasterBand(1).WriteArray(ndwi_mean_array)
    out_ds.GetRasterBand(1).SetNoDataValue(-32768)


