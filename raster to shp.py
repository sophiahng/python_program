__author__ = 'Sophia'


import os
import glob

import arcpy
from arcpy import env
from arcpy.sa import *

env.Workspace= "D:/NDVI Process/Environment/"

def raster_to_polygen(source_path, target_path):
    if os.path.exists(source_path) is not True:
        print("%s is not existed"%source_path)
        return
    if os.path.exists(target_path) is not True:
        print("%S is note existed"%target_path)
        return

    source_file_list = glob.glob(os.path.join(source_path, "*.tif"))
    source_file_list = [os.path.split(source_file)[-1] for source_file in source_file_list]
    for source_file in source_file_list:
        target_file = os.path.join(target_path, source_file[:source_file.find(".")] + ".shp")
        source_file = os.path.join(source_path, source_file)
        arcpy.RasterToPolygon_conversion(source_file, target_file, "NO_SIMPLIFY")

if __name__ == "__main__":
    rasterpath = os.path.normcase("D:/NDVI Process/MaySep/3K/over 4000/")
    targetpath = os.path.normcase("D:/NDVI Process/MaySepshp/3K")
    raster_to_polygen(rasterpath, targetpath)
