__author__ = 'Sophia'

import arcpy
import os
import glob
import csv
import math
import string
from arcpy.sa import *

arcpy.env.Workspace= "D:/Dian/process/"
arcpy.env.overwriteOutput = True





if __name__ == "__main__":
    shp_file_list = glob.glob(os.path.join("D:/Dian/United States/State", "*.shp"))
    in_features = os.path.normcase("D:/Dian/United States/Parks (Local).lyr")
    out_put_dir = os.path.normcase("D:/NDVI APRSEP/State")
    for shp_file in shp_file_list:
        shp_file_name = os.path.split(shp_file)[-1]
        state_name = shp_file_name[:-4]
        out_put_path = os.path.join(out_put_dir, state_name)
        if os.path.exists(out_put_path) is False:
            os.mkdir(out_put_path)
        temp_out_features = os.path.join(out_put_path, state_name + " ParksOr")
        if os.path.exists(temp_out_features + ".shp") is False:
            arcpy.Clip_analysis(in_features, shp_file, temp_out_features)
#            print("%s is produced" % temp_out_features)
        out_features = os.path.join(out_put_path, state_name + " Parks")
        if os.path.exists(out_features + ".shp") is False:
            try:
                arcpy.Select_analysis(temp_out_features + ".shp", out_features,  '"AREA" > 1')
            except:
                print("%s fails to be produced" %out_features)
                continue
            print("%s is produced" % out_features)

