import sys
import os
import time
import argparse
from fepy.Import import *


class PreProcess:
    """Class for PreProcessing
    """
    @classmethod
    def PreProcess(cls,InFileName, OutFileName, InDEMName,AOI):
        start = time.time()
        EPSG=32632
        bands=[1,2,3,4,5]
        outbands=[]
        outbands_clip=[]

        for i in bands:
            print "Processing Band %1d" % (i)
            inband=ImportL1B.ConvertFileName(InFileName,i)
            outband=os.path.splitext(inband)[0]+"_ortho"+".tif"
            outband_clip=os.path.splitext(inband)[0]+"_ortho_clip"+".tif"
            print "Orthorectifying %s"%(outband)
            ortho_band=ImportL1B.OrthoRectifyRaster(inband,outband,InDEMName,EPSG,AOI)
            print "Clipping %s"%(outband)
            ortho_clip=ImportL1B.ClipRaster(outband,outband_clip,EPSG,AOI)
            outbands.append(outband)
            outbands_clip.append(outband_clip)
        print "Creating multispectral stack %s"%(OutFileName)
        merged=ImportL1B.MultiLayerStack(outbands_clip,OutFileName)
        print "Deleting temporary files"
        for f in outbands:
            os.remove(f)
        for f in outbands_clip:
            os.remove(f)

        end = time.time()
        elapsed = end - start
        print "Time taken: ", elapsed, "seconds."


# Adding this allows to run the code as module as well as a script
if __name__ == "__main__":
    import sys
    import os
    import time
    import argparse
    from fepy.Import import *

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

    tmp = PreProcess(InFileName,OutFileName,InDemName,AOI)

#Import Metadata File
#metadata = MetaData()
#MetaDataRapidEye.import_rapideye_metadata(metadata ,inputs.InFileName)
#print metadata



