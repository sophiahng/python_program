# -*- coding: UTF-8 -*-
# File: Kriging
# Time: 7/25/2016 -> 6:01 PM
import arcpy
import os
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')


arcpy.env.Workspace = os.path.normcase("D:/Dian/process/")

def Krig(inPointFeatures, zField, outRaster, in_Mask):
    if os.path.exists(outRaster):
        return
    kModel = "CIRCULAR"
    cellSize = 0.02
    total_raster = os.path.join(os.path.dirname(outRaster),os.path.basename(outRaster)+"Kr")
    arcpy.CheckOutExtension("GeoStats")
    arcpy.Kriging_3d(inPointFeatures, zField, total_raster, kModel, cellSize)
    outExtractByMask = ExtractByMask(total_raster, in_Mask)
    arcpy.Delete_management(total_raster)
    outExtractByMask.save(outRaster)
    arcpy.BuildPyramids_management(outRaster)

if __name__ == "__main__":
    pass
