import os

import gdal
import matplotlib.pyplot as plt
import numpy as np
from osgeo import osr


def getCloudMask(qcArray, fromBit, toBit, value=0):
    cloudMask = np.zeros(qcArray.shape).astype(np.int16)
    # cloudBits = ((1 << toBit - fromBit) - 1) << fromBit
    #
    # cloudMask[(qcArray & cloudBits) >> fromBit != value] = 1
    # cloudMask[(qcArray & cloudBits) >> fromBit == value] = 0
    # cloudMask[qcArray != 0] = 1
    mask = (1 << 2) - 1
    cloudMask[:] = (qcArray & mask)
    cloudMask[cloudMask != 0] = 1

    return cloudMask


def listHdf(src_dir):
    list_files = os.listdir(src_dir)
    hdf_list = []
    for f in list_files:
        k = f.split(".")
        if k[len(k) - 1] == "hdf":
            hdf_list.append(f)

    return hdf_list

def convertCSR(src_tiff, dst_dir):
    ds = gdal.Open(src_tiff, gdal.GA_ReadOnly)
    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())

    new_cs = osr.SpatialReference()
    new_cs.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(old_cs,new_cs)

    band_path = os.path.join(dst_dir,
                             os.path.basename(os.path.splitext(src_tiff)[0]) + "-csr" + ".tif")
    out_ds = gdal.GetDriverByName("GTiff").Create(band_path, ds.RasterXSize, ds.RasterYSize, ds.RasterCount)
    out_geo = out_ds.GetGeometryRef()
