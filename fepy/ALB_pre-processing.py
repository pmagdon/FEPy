"""
Main file for pre-processing of L1b RapidEye images
"""

import os
import os.path
from glob import glob
from fepy.Ortho import Orthorectify_RapidEye_L1B
from fepy.Registration import ImageRegistration


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


dem = "F:/projects/biodiv/final/raster/dem/alb/dtmAlb_clip_lat_long_wgs84.tif"
master = "F:/projects/biodiv/edit/imageAnalysis/Registration/test/ALB_2015-08-08_sub.tif"
slave = "F:/projects/biodiv/edit/imageAnalysis/Registration/test/ALB_2015-10-02_sub.tif"
slave_nogeom = "F:/projects/biodiv/edit/imageAnalysis/Registration/test/ALB_2015-10-02_sub_no_geom.tif"
PointsFile = "F:/projects/biodiv/edit/imageAnalysis/Registration/homologous_points.txt"
StatsFile = os.path.splitext(PointsFile)[0]+".stats"
PixelPointsFile = "F:/projects/biodiv/edit/imageAnalysis/Registration/homologous_points_pixel.txt"
FilteredPixelPointsFile = "F:/projects/biodiv/edit/imageAnalysis/Registration/homologous_points_pixel_filtered.txt"

OutVector = "F:/projects/biodiv/edit/imageAnalysis/Registration/homologous_points.shp"

#Wenn die geometrie entfernt wird kann GenerateRPCModel nur mit den Pixelkoordinaten rechnen

test = ImageRegistration.ImageRegistration.PointExtraction(master, slave, 4, dem, PointsFile, OutVector, precision=0.1)
test=ImageRegistration.ImageRegistration.map2pix(PointsFile, PixelPointsFile, master)
test=ImageRegistration.ImageRegistration.GenerateRPCModel(slave, PixelPointsFile, StatsFile, 'utm', 32, True, 32632, dem)

#test=image2image.ImageRegistration.GenerateRPCModel(slave,PointsFile,StatsFile,'utm',32,True,32632,dem)
test=ImageRegistration.ImageRegistration.FilterTiePoints(PixelPointsFile, StatsFile, FilteredPixelPointsFile, 5)

FilteredStatsFile = os.path.splitext(PointsFile)[0]+"_filtered.stats"
test=ImageRegistration.ImageRegistration.GenerateRPCModel(slave, FilteredPixelPointsFile, FilteredStatsFile, 'utm', 32, True, 32632, dem)


#for file in files:
#    basename=os.path.splitext(os.path.basename(file))[0]
#    outfile=(outdir+basename+'_L3A1.tif').replace("_metadata","")
#    test= Orthorectify_RapidEye_L1B.PreProcess.PreProcess(file,outfile,dem,aoi)
