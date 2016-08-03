# -*- coding: UTF-8 -*-
# File: convert
# Time: 8/2/2016 -> 11:11 AM
import arcpy
import os

__all__ = ["csv_to_shp"]


def csv_to_shp(csv_file, shp_file=None):
    x_coords = "Longitude"
    y_coords = "Latitude"
    spRef = r"D:/Dian/Spatial_Files/United_States_2000/background/Coordinate.prj"
    if not shp_file:
        shp_file = csv_file[:-4] + ".shp"
    shp_basename = os.path.basename(shp_file)[:-4]
    arcpy.MakeXYEventLayer_management(csv_file, x_coords, y_coords, shp_basename, spRef)
    arcpy.FeatureToPoint_management(shp_basename, shp_file)