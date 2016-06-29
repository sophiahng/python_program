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
in_path = "D:/Dian/Data/2014/"
tmp_path= "D:/Dian/process/"
out_path = "D:/Dian/Spatial Image/8hour4th/"
us2010_path = "D:/Dian/Data/United States 2010/"
mask_path = "D:/Dian/Data/United States 2000/background/"
arcpy.env.overwriteOutput = True

site="8hour4th_"
year = 2014

while year<2015:
    # make event layer add xy data
    in_table = in_path+site+str(year)+".csv"
    x_coords="longitude"
    y_coords="latitude"
    z_coords="ozone"
    out_layer= site + str(year)
    saved_layer = out_path + site + str(year) + ".lyr"
    #spRef = arcpy.SpatialReference('NAD 1983 UTM Zone 11N')
    spRef = r"D:\Dian\Data\United States 2000\background\Coordinate.prj"
    arcpy.MakeXYEventLayer_management(in_table,x_coords,y_coords,out_layer,spRef)
    arcpy.SaveToLayerFile_management(out_layer, saved_layer)
    arcpy.FeatureClassToShapefile_conversion(saved_layer,out_path)
    saved_shp = out_path + site + str(year) + ".shp"
    #arcpy.DeleteField_management(saved_shp,["Field10","Field11","min_1"])
   # with arcpy.da.UpdateCursor(out_path + site + str(year) + ".dbf", "Region") as cursor:
    #    for row in cursor:
     #       if row[0] == "Unknown":
      #          cursor.deleteRow()
    #print "event " + str(year)

    # IDW
    inPointFeatures=out_path+ site + str(year) + ".shp"
    zField="ozone"
    cellSize=0.02
    power=2
    arcpy.CheckOutExtension("GeoStats")
    outLayer= "outIDW"+str(year)
    out_raster= out_path+"IDW"+str(year)
    arcpy.IDW_ga(inPointFeatures, zField, outLayer, out_raster, cellSize, power)
    print "IDW " + str(year)

    #Extract by mask the whole states
    inRaster = out_path+"IDW"+str(year)
    inMaskData = mask_path+"newstates"+".shp"
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(out_path + "allIDW" + str(year))
    arcpy.Delete_management(out_raster)
    print "states " + str(year)

    #Build pyramid from raster
    inras = out_path+ "allIDW" + str(year)
    arcpy.BuildPyramids_management(inras)
    print "Build pyramid" + str(year)


    # Execute Kriging of all monitoring sites
    outRaster = out_path + "kr"+str(year)
    kModel = "CIRCULAR"
    arcpy.Kriging_3d(inPointFeatures,zField, outRaster, kModel,cellSize)

    #Extract by mask the whole states
    inRaster = out_path + "kr"+str(year)
    inMaskData = mask_path+"newstates"+".shp"
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(out_path + "krig" + str(year))
    arcpy.Delete_management(outRaster)
    print "states " + str(year)

    #Build pyramid from raster
    inras = out_path+ "krig" + str(year)
    arcpy.BuildPyramids_management(inras)
    print "Build pyramid" + str(year)

    # Execute Kriging of exclude urban monitoring sites
    urban_polygon = us2010_path + "cb_2014_us_ua10_500k" + ".shp"
    urbansites = out_path + "urban" + ".shp"
    non_urban = out_path + "nonurban" + ".shp"
    arcpy.Clip_analysis(inPointFeatures, urban_polygon,urbansites)
    arcpy.Erase_analysis(inPointFeatures, urbansites, non_urban, "")

    outRaster = out_path + "nonkr"+str(year)
    kModel = "CIRCULAR"
    arcpy.Kriging_3d(non_urban,zField, outRaster, kModel,cellSize)

    #Extract by mask the whole states
    inRaster = out_path + "nonkr"+str(year)
    inMaskData = mask_path+"newstates"+".shp"
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(out_path + "nonu_krig" + str(year))
    arcpy.Delete_management(outRaster)
    print "states " + str(year)

    #Build pyramid from raster
    inras = out_path+ "nonu_krig" + str(year)
    arcpy.BuildPyramids_management(inras)
    print "Build pyramid" + str(year)
    year = year + 1