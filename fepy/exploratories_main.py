import sys
import os
import time
import argparse
from Import import *

start = time.time()
parser = argparse.ArgumentParser(description='Process to orthorectify RapidEye L1B data based on RPC correction.')
parser.add_argument("InFileName",action='store', help="Path to the corresponding MetaData.xml file")
parser.add_argument("OutFileName",action='store', help="L1B output file name")
parser.add_argument("InDEMName", action='store', help="DEM  file name")
parser.add_argument("AOI", action='store', help="Shapfile with the AOI")
inputs=parser.parse_args()

InFileName = os.path.normpath(inputs.InFileName)
OutFileName = os.path.normpath(inputs.OutFileName)
InDemName = os.path.normpath(inputs.InDEMName)
AOI=InDemName = os.path.normpath(inputs.AOI)


#Import Metadata File
#metadata = MetaData()
#MetaDataRapidEye.import_rapideye_metadata(metadata ,inputs.InFileName)
#print metadata


EPSG=32632
bands=[1,2,3,4,5]
outbands=[]

for i in bands:
    print "Processing Band %1d" % (i)
    inband=ImportL1B.ConvertFileName(inputs.InFileName,i)
    outband=os.path.splitext(inband)[0]+"_ortho"+".tif"
    ortho_band=ImportL1B.OrthoRectifyRaster(inband,outband,inputs.InDEMName,EPSG,AOI)
    outbands.append(outband)

merged=ImportL1B.MultiLayerStack(outbands,OutFileName)

for f in outbands:
    os.remove(f)

end = time.time()
elapsed = end - start
print "Time taken: ", elapsed, "seconds."

