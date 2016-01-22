import os
import os.path
from glob import glob
from fepy.Ortho import Orthorectify_RapidEye_L1B


files = []
start_dir = "U:/data/raw/RapidEye/L1B/alb"
pattern   = "*metadata.xml"

for dir,_,_ in os.walk(start_dir):
    files.extend(glob(os.path.join(dir,pattern)))

outdir="U:/data/edit/RapidEye/L3A/alb/L3A1/"
dem="Z:/Aktuell/Projekte/BioDiv/data/final/raster/dem/alb/dtmAlb_utm32_wgs84.tif"
aoi="Z:/Aktuell/Projekte/BioDiv/data/final/vector/alb/geb_buf100_utm32_wgs84.shp"
file=files[0]
basename=os.path.splitext(os.path.basename(file))[0]
outfile=(outdir+basename+'_L3A1.tif').replace("_metadata","")
test=Orthorectify_RapidEye_L1B.PreProcess.PreProcess(file,outfile,dem,aoi)

#for file in files:
#    basename=os.path.splitext(os.path.basename(file))[0]
#    outfile=(outdir+basename+'_L3A1.tif').replace("_metadata","")
#    test= Orthorectify_RapidEye_L1B.PreProcess.PreProcess(file,outfile,dem,aoi)
