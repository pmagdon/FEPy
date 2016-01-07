
"""
Import RapidEye L1B images

This class imports the RapidEye L1B products performs RPC based orthorectification and clips the image to the defined AOI
"""

import sys
import time
import argparse
import os
from osgeo import gdal
from osgeo import gdalconst

class ImportL1B:
    """ Class for importing RapidEye L1B  images
    """
    @classmethod
    def ConvertFileName(cls,infile,band):
        """ Method to find the ntf file from the xml file
        """
        try:
            import os
        except:
            raise ImportError("Can not find module os")
        try:
            base = str.split(infile,"_metadata.xml")[0]
            print base
            ext="_band"+str(band)+".ntf"
            outfile=base+ext
            return outfile
        except:
            raise ImportError("Can not covert file names")

    @classmethod
    def OrthoRectifyRaster(cls,InRaster,OutRaster,InDEM,EPSG,AOI):
        """ RPC based orthorectification

        :param InRaster: Full path to the L1B ntf file
        :param InDEM: Full path to the DEM file
        :type InRaster: string
        :type InDEM: string
        :return: Full path the orthorectified tif file
        :rtype: string
        """
        com = " ".join(["gdalwarp -overwrite -ot UInt16 -s_srs EPSG:4326 -multi -tr 5 5 -cutline "+AOI +" -crop_to_cutline -t_srs EPSG:"+str(EPSG)+" -rpc -to RPC_DEM=" + InDEM, InRaster, OutRaster])
        print com
        tmp=os.system(com)
        print tmp
        if tmp !=0:
          raise Exception("Could not orthorectify the image ")
        #return OutRaster

    @classmethod
    def MultiLayerStack(cls,InRasters,OutRaster):
        """ Creates a multilayer stack
        :return:
        """
        try:
            import otbApplication
        except:
            raise ImportError("Can not import module otbApllication")

        ConcatenateImages = otbApplication.Registry.CreateApplication("ConcatenateImages")
        ConcatenateImages.SetParameterStringList("il", InRasters)
        ConcatenateImages.SetParameterString("out", OutRaster)
        ConcatenateImages.ExecuteAndWriteOutput()


    @classmethod
    def ReadRaster(cls,infile):
        """ Read Raster into array

        :param InFile: Full path to raster that should be imported
        :type InFile: string
        :return: 2D Array with pixel values
        :rtype: numpy2d Array
        """
        try:
            import gdal
            import rasterio
        except:
            raise ImportError("Can not import module GDAL or RasterIO")

        with rasterio.open(infile) as src:
            transform = src.meta['transform']
            nBands = (src.indexes)
            array = src.read_band(1)
            return array
        #except:
        #    raise ImportError("Can not read band")

    @classmethod
    def Reproject(cls,inRaster, outRaster,EPSG):
        """ Reprojects rasters using GDAL

        The class method uses the GDAL wrap function to reporject raster files

        :param inRaster: Full path to raster that should be reprojected
        :param outRaster: Full path where reprojected raster is stored
        :param EPSG: EPSG Code of the target raster
        :type InFile: string
        :type outFile: string
        :type EPSG: string
        """
        try:
            import gdal
        except:
            raise ImportError("Can not import module GDAL")
        try:
            dataset = gdal.Open(infile)
            out = dataset.GetRasterBand(1)
            print dataset.GetMetadata()
            return out
        except:
            raise ImportError("Can not read band")
        #if not tmp:
        #  raise Exception("Could not orthorectify the image ")

        com=" ".join(["gdalwarp -t_srs EPSG:"+str(EPSG),InRaster,OutRaster])
        tmp=os.system(com)
        print tmp
        #if not tmp:
        #    raise Exception("Could not reproject the image ")
        #os.remove(OutRaster)

# Adding this allows to run the code as module as well as a script
if __name__ == "__main__":
    import sys
    import os
    # Start Time
    start = time.time()
    parser = argparse.ArgumentParser(description='Process to orthorectify RapidEye L1B data based on RPC correction.')

    parser.add_argument("InFileName", help="L1B input band", required=True)
    parser.add_argument("OutFileName", help="L1B output file name", required=True)
    parser.add_argument("InDemName", help="DEM  file name", required=True)
    parser.add_argument("OutDemName", help="Reprojected DEM  file name", required=True)

    InFileName = os.path.normpath(str(sys.argv[1]))
    OutFileName = os.path.normpath(str(sys.argv[2]))
    InDemName = os.path.normpath(str(sys.argv[3]))
    OutDemName = os.path.normpath(str(sys.argv[4]))

    dataset = gdal.Open(InFileName, GA_ReadOnly)

    print 'Driver: ', dataset.GetDriver().ShortName, '/', dataset.GetDriver().LongName
    print 'Projection is ', dataset.GetProjection()
    geotransform = dataset.GetGeoTransform()
    if not geotransform is None:
        print 'Origin = (', geotransform[0], ',', geotransform[3], ')'
        print 'Pixel Size = (', geotransform[1], ',', geotransform[5], ')'
    #Reproject the elevation model
    OutEPSG='4326'
    ReprojectRaster(InDemName,OutDemName,OutEPSG)
    #com = " ".join(["gdalwarp -t_srs EPSG:4326", InDemName, OutDemName])
    #os.system(com)

    #Orthorectification based on RPC transformation
    #com = " ".join(["gdalwarp  -rpc -to RPC_DEM=" + OutDemName, InFileName, OutFileName])
    #os.system(com)

#Get band
#band = dataset.GetRasterBand(1)
#dataset = None

