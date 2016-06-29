__author__ = 'Sophia'

import arcpy
import os
import glob
import csv
import math
import string
from arcpy.sa import *
arcpy.env.Workspace= "D:/Dian/process/"
#arcpy.env.overwriteOutput = True

def idw_ga(input_shp_file, output_file_path, mask_file, z_field):
    inPointFeatures = input_shp_file
    zField = z_field
    cellSize = 0.02
    power = 2
    arcpy.CheckOutExtension("GeoStats")
#    outLayer = os.path.split(input_shp_file)[-1][:-4] os.path.split(input_shp_file)[-1][:-4]
    outLayer = "ignored_file"
    file_name = os.path.split(input_shp_file)[-1]
    year_str_list = [str(year) for year in range(2000, 2014)]
    name = None
    for year_str in year_str_list:
        if file_name.find(year_str) >= 0:
            name = int(year_str)
            break
    if  name == None:
         print("shp file can't find year")

    name = "tempto" + str(name)
    print name
    out_raster = os.path.join(output_file_path, name)
    arcpy.IDW_ga(inPointFeatures, zField,outLayer, out_raster, cellSize, power)
    print("we have idw_ga %s" % inPointFeatures)

    #Extract by mask the whole states
    inRaster = out_raster
    inMaskData = mask_file
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(os.path.join(output_file_path, "es" + name ))
    print("we have produce")


if __name__ == "__main__":
    input_file_path1 = os.path.normcase("D:/NDVI Process/Ozone layer/Average/MaySep")
    input_file_path2 = os.path.normcase("D:/NDVI Process/Ozone layer/AOT40/MaySep")
    input_file_path3 = os.path.normcase("D:/NDVI Process/Climate layer/Prcp")
    input_file_path4 = os.path.normcase("D:/NDVI Process/Climate layer/Temptotal")
    output_file_path1 = os.path.normcase("D:/NDVI Parks/Maps/IDW/Ozoneave Maysep")
    output_file_path2 = os.path.normcase("D:/NDVI Parks/Maps/IDW/AOT MaySep")
    output_file_path3 = os.path.normcase("D:/NDVI Parks/Maps/IDW/Prcp MaySep")
    output_file_path4 = os.path.normcase("D:/NDVI Parks/Maps/IDW/Temptotal MaySep")
    mask_file = os.path.normcase("D:/Dian/United States/background/newstates.shp")
    input_file_path_list = list()
    output_file_path_list = list()

    for file_dir_index in range(2, 3):
        input_file_path_list.append(eval("input_file_path" + str(file_dir_index)))
        output_file_path_list.append(eval("output_file_path" + str(file_dir_index)))

    for file_dir_index, input_shp_file_path in enumerate(input_file_path_list):
        input_shp_file_list = glob.glob(os.path.join(input_shp_file_path, "*.shp"))
        output_file_path = output_file_path_list[file_dir_index]
        for input_shp_file in input_shp_file_list:
            #z_field = "mean"
            z_field = "mean"
            #if file_dir_index > 0:
                #z_field = "maysep"
            idw_ga(input_shp_file, output_file_path, mask_file, z_field)





















