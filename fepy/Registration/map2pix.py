#Modul to convert UTM to Pixel-Coordinates#
#Input: #
#


import numpy as np
import gdal
from gdalconst import *

def map2pix(point_file,img_file):


    # read coordinate file
    a = np.loadtxt(point_file,delimiter='\t')
    data = unique_rows(a)
    # register all of the drivers
    gdal.AllRegister()

    # open the image
    ds = gdal.Open(img_file, GA_ReadOnly)

    # get image size
    rows = ds.RasterYSize
    cols = ds.RasterXSize

    # get georeference info
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    for i in range(0, len(data)):
        # get x,y
        x = data[i,0]
        y = data[i,1]

        # compute pixel offset
        data[i,0] = int((x - xOrigin) / pixelWidth)
        data[i,1] = int((y - yOrigin) / pixelHeight)

    np.savetxt("pixel_points.txt", data, delimiter='\t', fmt="%.12f")
    
def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))