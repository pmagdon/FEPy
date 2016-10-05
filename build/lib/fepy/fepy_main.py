__author__ = 'pmagdon'
import sys
import os
import time
import argparse
from im import *

start = time.time()
parser = argparse.ArgumentParser(description='Process to orthorectify RapidEye L1B data based on RPC correction.')
parser.add_argument("InFileName",action='store', help="Path to the corresponding MetaData.xml file")
parser.add_argument("OutFileName",action='store', help="L1B output file name")
parser.add_argument("InDEMName", action='store', help="DEM  file name")
inputs=parser.parse_args()

InFileName = os.path.normpath(inputs.InFileName)
OutFileName = os.path.normpath(inputs.OutFileName)
InDemName = os.path.normpath(inputs.InDEMName)

#Import Metadata File and create metadata object
metadata = MetaData()
MetaDataRapidEye.import_rapideye_metadata(metadata ,inputs.InFileName)
print metadata

band=1
EPSG=32632
#Orthorectify and Import L1B Band
inband=ImportL1B.ConvertFileName(inputs.InFileName,band)
ortho_band=ImportL1B.OrthoRectifyRaster(inband,inputs.InDEMName,EPSG)
band=ImportL1B.ReadRaster(ortho_band)

#Parametrizes the Atmosperhic models
#s=SixS()
#print metadata.Acquisitiondate

#s.geometry.solar_z = metadata.SunZenith
#s.geometry.solar_a = metadata.SunElevation
#s.geometry.view_a = metadata.SensorAzimuth
#s.geometry.view_z = metadata.SensorZenith
#s.geometry.month=metadata.Month
#s.geometry.day = metadata.Day
#s.geometry.latitude = metadata.CenterLatidue
#s.geometry.longitude = metadata.CenterLongitude
#print inputs.InAERONETName
#s.atmos_profile = SixSHelpers.Aeronet.import_aeronet_data(s,inputs.InAERONETName, "03/12/2014 11:18:27.38")

#s.atmos_profile = SixSHelpers.Aeronet.import_aeronet_data(s,inputs.InAERONETName)
#s.run()

end = time.time()
elapsed = end - start
print "Time taken: ", elapsed, "seconds."

