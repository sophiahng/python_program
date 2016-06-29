import arcpy
import os
from arcpy.sa import *

def IDW(inPointFeatures, zField, out_raster):
    if not os.path.exists(os.path.dirname(out_raster)):
        os.mkdir(os.path.dirname(out_raster))
    cellSize = 0.02
    power = 2
    out_layer = os.path.basename(out_raster)
    arcpy.CheckOutExtension("GeoStats")
    arcpy.IDW_ga(inPointFeatures, zField, out_layer, out_raster, cellSize, power)


if __name__ == "__main__":
    pass

