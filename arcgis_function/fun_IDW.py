import arcpy
import os
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')


arcpy.env.Workspace = os.path.normcase("D:/Dian/process/")

def idw(inPointFeatures, zField, out_raster, in_Mask):
    if not os.path.exists(os.path.dirname(out_raster)):
        os.mkdir(os.path.dirname(out_raster))
    if os.path.exists(os.path.basename(out_raster)):
        return
    cellSize = 0.02
    power = 2
    total_raster = os.path.join(os.path.dirname(out_raster),os.path.basename(out_raster)+"IDW")
    arcpy.CheckOutExtension("GeoStats")
    arcpy.IDW_ga(inPointFeatures, zField, "", total_raster, cellSize, power)
    outExtractByMask = ExtractByMask(total_raster, in_Mask)
    outExtractByMask.save(out_raster)
    arcpy.BuildPyramids_management(out_raster)

if __name__ == "__main__":
    pass

