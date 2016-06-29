import os
import arcpy
from arcpy import env
from arcpy.sa import *
import glob


FILEPATH = os.path.normcase("D:/Dian/Spatial Image/Climate dataset/Tavg buffer/")
OUTPATH = os.path.normcase("D:/Dian/Spatial Image/Climate dataset/Climate overlay/")
env.workspace= "D:/NDVI Extract/Workspace"

arcpy.Intersect_analysis ([FILEPATH + "Buffer1980.shp", FILEPATH + "Buffer1981.shp"], OUTPATH + "mysites")


