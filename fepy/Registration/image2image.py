"""
Image two image registration

This class uses homologous points extraction and RPC Sensor modelling for image to image to image registration
"""

# OTB Workflow for image matching
# 
# 
#
# Usage:
# $ image2image.py <input1> <band1> <input2> <band2> <dem> <utm_zone> <northhem> <epsg> <precision>
# <input1> is the slave image and <input2> is the master image.
#
# RapidEye example:
# fep_image2image sub_5053018_2009-03-31_RE5_3A_151123.tif 4 sub_5053018_2012-10-02_RE3_3A_151123.tif 4 /srtm4 50 True 32650 50 5.0


import sys
import time
import os
import otbApplication
import map2pix

class ImageRegistration:
    @classmethod
    def PointExtraction(cls,master,slave,band,dem, PointsFile, OutVector,precision):
        try:
            import  otbApplication
        except:
            raise ImportError("Can not find module otbAbblication")

        if not os.path.isfile(master):
            raise ValueError('The master file does not exits')
        if not os.path.isfile(slave):
            raise ValueError('The slave file does not exits')
        #if not os.path.isfile(dem):
        #    raise ValueError('The dem file does not exits')

        HomologousPointsExtraction = otbApplication.Registry.CreateApplication("HomologousPointsExtraction")

        # Application parameters:
        HomologousPointsExtraction.SetParameterString("in1", master)
        HomologousPointsExtraction.SetParameterInt("band1", band)
        HomologousPointsExtraction.SetParameterString("in2", slave)
        HomologousPointsExtraction.SetParameterInt("band2", band)
        HomologousPointsExtraction.SetParameterString("algorithm","surf")
        HomologousPointsExtraction.SetParameterString("mode","full")
        HomologousPointsExtraction.SetParameterFloat("threshold",5.0)
        HomologousPointsExtraction.SetParameterFloat("precision", precision)
        HomologousPointsExtraction.SetParameterString("mfilter","mfilter",False)
        HomologousPointsExtraction.SetParameterString("2wgs84","2wgs84",True)
        HomologousPointsExtraction.SetParameterString("elev.dem",dem)
        HomologousPointsExtraction.SetParameterString("out", PointsFile)
        HomologousPointsExtraction.SetParameterString("outvector",OutVector)

        # Execute the application
        print "Starting HomologousPointsExtraction ........Using SURF"
        result=HomologousPointsExtraction.ExecuteAndWriteOutput()
        if result == 0:
            print "Finished HomologousPointsExtraction ........Using SURF"
        else:
            raise ValueError("Failed to extract homologous points")

    @classmethod
    def GenerateRPCModel(cls,ImageName,InputPoints,StatsFile,map,utmZone,north,epsg,dem):
        try:
            import  otbApplication
            import  subprocess
            from os.path import abspath, dirname, join
        except:
            raise ImportError("Can not find module otbAbblication")

        #Instance of the GenerateRPCSensorModel application
        #GenerateRPCSensorModel = otbApplication.Registry.CreateApplication("GenerateRPCSensorModel")

        # Application parameters:
        out_geom=ImageName+".geom"
        GenerateRPCSensor = ['otbcli_GenerateRPCSensorModel','-outgeom',out_geom,'-inpoints',InputPoints,'-outstat',StatsFile,'-map', map,'-map.utm.zone',str(utmZone),'-map.utm.northhem','1','-map.epsg.code',str(epsg),'-elev.dem',dem]

        # Execute the application
        print "Starting GenerateRPCSensorModel"
        result=subprocess.call(GenerateRPCSensor,shell=True)

        if result == 0:
            print "Finished GenerateRPCSensorModel"
        else:
            raise ValueError("Unable to generate RPC Sensor Model")

    @classmethod
    def FilterTiePoints(cls,InputPointsFile,InputStatsFile,FilterPointsFile,precision):
        try:
            import  numpy as np
        except:
            raise ImportError("Can not find module numpy")
        statnames=['ref_lon','ref_lat','elevation','predicted_lon', 'predicted_lat', 'elevation', 'x_error', 'y_error' ,'global_error']
        stats = np.genfromtxt(InputStatsFile, dtype=float, delimiter='\t',skiprows=1,names=statnames)
        points = np.genfromtxt(InputPointsFile, dtype=float, delimiter='\t')

        if stats.shape[0]!= points.shape[0]:
            raise ValueError('The point file and the stat file do not have the same number of rows')

        filtered=points[np.logical_or.reduce([stats['global_error'] < precision])]
        np.savetxt(FilterPointsFile, filtered, delimiter='\t', fmt="%.12f")
        print "Filtered Points File saved"

    @classmethod
    def unique_rows(cls,array):
        try:
            import numpy as np
        except:
            raise ImportError("Can not find modul numpy")
        a = np.ascontiguousarray(array)
        unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
        return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

    @classmethod
    def map2pix(cls,InputPointFile,OutputPointfile,RasterFile):
        try:
            import  gdal
            import numpy as np
            from gdalconst import GA_ReadOnly
        except:
            raise ImportError("Can not find modul gdal")
        # read coordinate file
        a = np.loadtxt(InputPointFile,delimiter='\t')
        data = cls.unique_rows(a)
        # register all of the drivers
        gdal.AllRegister()
        # qurey the image
        ds = gdal.Open(RasterFile, GA_ReadOnly)
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

        np.savetxt(OutputPointfile, data, delimiter='\t', fmt="%.12f")
        print "Coordinate transformation finished"


# Adding this allows to run the code as module as well as a script
if __name__ == "__main__":
    import sys
    import time
    import os
    import otbApplication
    import map2pix

    parser = argparse.ArgumentParser(description='Process to extract homologous points from two image bands.')
    parser.add_argument("Master",action='store', help="Path to the master image")
    parser.add_argument("Slave",action='store', help="Path to the slave image")
    parser.add_argument("band",action='store',help="Number of band to be used")
    parser.add_argument("dem", action='store', help="Path to the DEM")
    parser.add_argument("OutPoints", action='store', help="Path to the text file were the points are saved")
    parser.add_argument("PixelPoints", action='store', help="Path to the text file were the points with pixel coordinates are saved")
    parser.add_argument("OutVector", action='store', help="Path to the shapefile were the points are saved")
    parser.add_argument("precision", action='store', help="Precision in physical units")

    inputs=parser.parse_args()

    master = os.path.normpath(inputs.Maser)
    slave  = os.path.normpath(inputs.Slave)
    band = inputs.band
    dem    = os.path.normpath(inputs.dem)
    OutputPoints = os.path.normpath(inputs.OutPoints)
    OutVector = os.path.normpath(inputs.OutVector)
    precision=inputs.precision

    filenameMaster = os.path.splitext(master)[0]

    #Start Time
    start = time.time()
    ImageRegistration.PointExtraction(master, slave, band, dem, OutputPoints, OutVector, precision)
    end = time.time()
    elapsed = end - start
    print "Time taken: ", elapsed, "seconds."

# # Convert map to pixel coordinates
    print "Starting ConvertMapToImageCoordinates ........"
    ImageRegistration.map2pix(OutPoints, PixelPoints, master)
    print "ConvertMapToImageCoordinates ........DONE"

# # 2. Step
#
#
# # Execute the application
# print "Starting GenerateRPCSensorModel ........"
# GenerateRPCSensorModel.ExecuteAndWriteOutput()
# print "GenerateRPCSensorModel ........DONE"
# end = time.time()
# elapsed = end - start
# print "Time taken: ", elapsed, "seconds."
#
# # 3. Step
# # Instance of the OrthoRectification application
# OrthoRectification = otbApplication.Registry.CreateApplication("OrthoRectification")
#
# # The following lines set all the application parameters:
# OrthoRectification.SetParameterString("io.in", in1+"?&skipcarto=true")
# OrthoRectification.SetParameterString("io.out", "ortho_"+in1)
# OrthoRectification.SetParameterString("map","utm")
# OrthoRectification.SetParameterInt("map.utm.zone", utm_zone)
# OrthoRectification.SetParameterString("map.utm.northhem", "map.utm.northhem",utm_north)
# OrthoRectification.SetParameterInt("map.epsg.code", epsg)
# OrthoRectification.SetParameterString("elev.dem",dem)
# OrthoRectification.SetParameterString("outputs.mode","orthofit")
# OrthoRectification.SetParameterString("outputs.ortho", in1)
# OrthoRectification.SetParameterString("interpolator","nn")
# OrthoRectification.SetParameterFloat("opt.gridspacing",1)
#
# # The following line execute the application
# print "Starting OrthoRectification ........"
# OrthoRectification.ExecuteAndWriteOutput()
# print "OrthoRectification ........DONE"
# end = time.time()
# elapsed = end - start
# print "Time taken: ", elapsed, "seconds."
