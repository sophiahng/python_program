__author__ = 'Sophia'


import os
import glob

import arcpy
from arcpy import env
from arcpy.sa import *

env.Workspace= "D:/NDVI Process/Environment/"
arcpy.env.overwriteOutput = True

if __name__ == "__main__":
    result_path = os.path.normcase("D:/NDVI Process/Result with para")
    target_path = os.path.normcase("D:/NDVI Process/Stats/new")


    value_fields = ["GRIDCODE","State","Latitude_2","Longitud_2","mean","mean_1","maysep","maysep_1","mean_12"]
  #  value_fields = "GRIDCODE_12"


    file_list = glob.glob(os.path.join(result_path, "*.shp"))
    for shp_file in file_list:
        out_file = os.path.join(target_path, os.path.split(shp_file)[-1][:-4] + ".txt")
        arcpy.ExportXYv_stats(shp_file, value_fields, "SPACE",out_file,"ADD_FIELD_NAMES")
print("dfjdjf")