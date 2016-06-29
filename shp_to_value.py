__author__ = 'Sophia'

import os
import glob

import arcpy
from arcpy import env
from arcpy.sa import *

env.Workspace= "D:/NDVI Process/Environment/"
arcpy.env.overwriteOutput = True

if __name__ == "__main__":
    result_path = os.path.normcase("D:/NDVI Process/Result")
    target_path = os.path.normcase("D:/NDVI Process/Stats")

    year_list = range(2000, 2014)
    value_fields = ["GRIDCODE", "GRIDCODE_6","GRIDCOD_12", "GRIDCOD_18","GRIDCOD_24","GRIDCOD_30","GRIDCOD_36","mean","mean_1","maysep","maysep_1"]
  #  value_fields = "GRIDCODE_12"
    for year in year_list:
        file_path = os.path.join(result_path, str(year))
        file_list = glob.glob(os.path.join(file_path, "*.shp"))
        for shp_file in file_list:
            out_file = os.path.join(target_path, os.path.split(shp_file)[-1][:-4] + ".txt")
            arcpy.ExportXYv_stats(shp_file, value_fields, "SPACE",out_file,"ADD_FIELD_NAMES")
    print("dfjdjf")

