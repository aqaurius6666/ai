from osgeo import gdal, gdal_array, osr
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import cookbook.clip
import os

from src.main.hdf2rgb import hdf2rgb
from src.main.ndwi import ndwi, ndwi_mean
from src.main.utils import getCloudMask, listHdf, convertCSR


def showSubDataset(hdf_file):
    hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)
    subdatasets = hdf_ds.GetSubDatasets()
    for i in range(0, len(subdatasets)):
        print(subdatasets[i], i)


def mergeSubdatasetFromHDF(hdf_file, dst_dir, subdatasets):
    hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)

    cloud_ds = gdal.Open(hdf_ds.GetSubDatasets()[18][0], gdal.GA_ReadOnly)
    cloud_array = cloud_ds.ReadAsArray().astype(np.int16)

    # build output path
    band_path = os.path.join(dst_dir,
                             os.path.basename(os.path.splitext(hdf_file)[0]) + "-merge" +
                             ",".join(str(i) for i in subdatasets) + ".tif")
    # write raster
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  cloud_ds.RasterXSize,
                                                  cloud_ds.RasterYSize,
                                                  len(subdatasets),  # Number of bands
                                                  gdal.GDT_Int16)
    out_ds.SetGeoTransform(cloud_ds.GetGeoTransform())
    out_ds.SetProjection(cloud_ds.GetProjection())

    for i in range(0, len(subdatasets)):
        dataset_info = hdf_ds.GetSubDatasets()[subdatasets[i]]
        # read into numpy array
        band_ds = gdal.Open(dataset_info[0], gdal.GA_ReadOnly)
        band_array = band_ds.ReadAsArray().astype(np.int16)
        cloud_mask = getCloudMask(cloud_array, 0, 1, 0)
        # convert no_data values
        band_array[band_array == -28672] = -32768
        band_array[band_array & cloud_mask == 1] = -200
        band_array[band_array < -100] = -32768
        band_array[band_array > 8000] = -32768

        out_ds.GetRasterBand(i + 1).SetDescription(dataset_info[1])
        out_ds.GetRasterBand(i + 1).WriteArray(band_array)
        out_ds.GetRasterBand(i + 1).SetNoDataValue(-32768)


if __name__ == "__main__":
    # mergeSubdatasetFromHDF("../data4/MYD09GA.A2019091.h28v07.061.2020291100944.hdf", "test", [11, 14, 13])
    # hdf2rgb("../data4/MYD09GA.A2019041.h28v07.061.2020287101526.hdf", "test")
    ndwi_mean("clip", "test")
    # mergeSubdatasetFromHDF("../data4/MYD09GA.A2019031.h28v07.061.2020285042001.hdf", "test", [18])
    # showSubDataset("../data4/MYD09GA.A2019001.h28v07.061.2020283162101.hdf")


    # src_dir = "../data4"
    # out_dir = "tif"
    # hdf_list = listHdf(src_dir)
    # for hdf in hdf_list[50:100]:
    #     mergeSubdatasetFromHDF(os.path.join(src_dir, hdf), out_dir, [11, 12, 13, 14, 15, 16, 17, 18])

    # cookbook.clip.main("../shapefile/MienNam/MIEN_NAM/MienNam.shp", "reproject/reproject1.tif")
    # convertCSR("test/MYD09GA.A2019235.h28v07.061.2020306061544-rgb.tif", "test")

