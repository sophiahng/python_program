import os
import arcpy
from arcpy import env
from arcpy.sa import *
import glob

#arcpy.env.overwriteOutput = True

FILEPATH = os.path.normcase("D:/NDVI Process/Ozone layer/Average/MaySep/")
OUTPATH = os.path.normcase("D:/NDVI Process/Ozone Buffer/Average/Ozone 3km/MaySep/")
env.workspace= "D:/NDVI Extract/Workspace/"

site="24hmaysep"
year = 2000

while year<2014:
    in_features = arcpy.mapping.Layer(FILEPATH + site + str(year) + "layer" + ".shp")
    out_features = OUTPATH + site +"3k" + str(year)
    arcpy.Buffer_analysis(in_features,out_features,"3000 meters")
    year=year+1







