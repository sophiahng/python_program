__author__ = 'Sophia'


import os
import glob

import arcpy
from arcpy import env
from arcpy.sa import *

env.Workspace= "D:/NDVI Process/Environment/"

def shp_to_kml(source_path, target_path):
    if os.path.exists(source_path) is not True:
        print("%s is not existed"%source_path)
        return
    if os.path.exists(target_path) is not True:
        print("%S is note existed"%target_path)
        return

    source_file_list = glob.glob(os.path.join(source_path, "*.lyr"))
    source_file_list = [os.path.split(source_file)[-1] for source_file in source_file_list]
    for source_file in source_file_list:
        target_file = os.path.join(target_path, source_file[:source_file.find(".")]+ ".kmz")
        source_file = os.path.join(source_path, source_file)
        arcpy.LayerToKML_conversion(source_file, target_file)

if __name__ == "__main__":
    rasterpath = os.path.normcase("D:/NDVI Process/Results with para lyr/")
    targetpath = os.path.normcase("D:/NDVI Process/KML Results/")
    shp_to_kml(rasterpath, targetpath)
