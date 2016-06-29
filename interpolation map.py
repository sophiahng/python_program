
import arcpy
import os
import glob
import csv
import math
import string
from arcpy import env
from dbfpy import dbf
from arcpy.sa import *

arcpy.env.Workspace= "D:/Dian/process/"
in_path = "D:/Dian/Data/Ozone data/"
tmp_path= "D:/Dian/process/"
out_path = "D:/Dian/Spatial Image/Ozone AOT410/"
us2010_path = "D:/Dian/Data/United States 2010/"
mask_path = "D:/Dian/Data/United States 2000/background/"
arcpy.env.overwriteOutput = True

site="aotaproct_"
year = 2014

while year<2015:
    # make event layer add xy data
    in_table = in_path+site+str(year)+".csv"
    x_coords="longitude"
    y_coords="latitude"
    z_coords="ozone"
    out_layer= site + str(year)
    saved_layer = out_path + site + str(year) + ".lyr"
    spRef = r"D:\Dian\Data\United States 2000\background\Coordinate.prj"
    arcpy.MakeXYEventLayer_management(in_table,x_coords,y_coords,out_layer,spRef)
    arcpy.SaveToLayerFile_management(out_layer, saved_layer)
    arcpy.FeatureClassToShapefile_conversion(saved_layer,out_path)
    saved_shp = out_path + site + str(year) + ".shp"

    inPointFeatures = out_path + site + str(year) + ".shp"
    zField = "ozone"
    cellSize = 0.02
    power = 2
    arcpy.CheckOutExtension("GeoStats")
    outLayer = "outIDW" + str(year)
    out_raster = out_path + "IDW" + str(year)
    arcpy.IDW_ga(inPointFeatures, zField, outLayer, out_raster, cellSize, power)
    print "IDW " + str(year)

    # Extract by mask the whole states
    inRaster = out_path + "IDW" + str(year)
    inMaskData = mask_path + "newstates" + ".shp"
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(out_path + "allIDW" + str(year))
    arcpy.Delete_management(out_raster)
    print "states " + str(year)

    year = year+1