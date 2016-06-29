__author__ = 'Sophia'


import os
import glob

import arcpy
from arcpy import env

env.Workspace= "D:/NDVI Process/Environment/"
arcpy.env.overwriteOutput = True



if __name__ == "__main__":
    source1_path = os.path.normcase("D:/NDVI/Environment/Temptavg layer")
    source2_path = os.path.normcase("D:/NDVI/Environment/Tempepa decfeb layer")
    target_path = os.path.normcase("D:/NDVI/Environment/Ttotal decfeb layer")
    if os.path.exists(target_path) is False:
        os.mkdir(target_path)
    file1_list = glob.glob(os.path.join(source1_path, "*.shp"))
    file2_list = glob.glob(os.path.join(source2_path, "*shp"))
    file_list = file1_list + file2_list
    year_list = range(2000, 2015)
    shp_file_dict = dict.fromkeys(year_list, None)
    for shp_file in file_list:
        year = None
        year_str_list = [str(year) for year in year_list]
        for year_str in year_str_list:
            if shp_file.find(year_str) >= 0:
                year = int(year_str)
                break
        if  year == None:
            print("shp file can't find year")
        if shp_file_dict[year] is None:
            shp_file_dict[year] = list()
        shp_file_dict[year].append(shp_file)
    for k,v in shp_file_dict.items():
        print(k)
        outfile_name = str(k) + "_decfeb.shp"
        arcpy.Merge_management(v, os.path.join(target_path, outfile_name))
    print "dfjdjf"