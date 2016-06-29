# coding=utf-8
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

def create_parks(state):
    in_features = os.path.normcase("D:/NDVI/" + state + "/parks/" + state + " Parks.shp")
    split_features = in_features
    split_field = "NAME"
    out_workspace = os.path.normcase("D:/NDVI/" + state + "/parks/" + state + " Parks")

    if os.path.exists(out_workspace) is False:
        os.mkdir(out_workspace)
    try:
        arcpy.Split_analysis (in_features, split_features, split_field, out_workspace)
    except:
        print("there are some errors in %s during create parks process" % state)



def extract_by_mask(inRaster, inMaskData, output_file):
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(output_file)
    print("%s has been produced" % output_file)

def task(inmask_path, day_list):
    inraster_path = os.path.normcase("H:/Data/ndvi extract intersect")
    state = os.path.normcase(inmask_path).split("\\")[2]
    output_path = os.path.normcase("D:/NDVI/" + state + "/parks/ndvi " + state + " parks")
    inraster_file_list = glob.glob(os.path.join(inraster_path, "*.tif"))
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4]
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            inraster_file_year = inraster_file_name[2:6]
            inraster_file_day = inraster_file_name[6:inraster_file_name.find(".")]
            if int(inraster_file_day) not in day_list:
                continue
            output_file = os.path.join(output_dir, str(inraster_file_year) + "_" + str(inraster_file_day))
            if os.path.exists(output_file) is True:
                continue
            try:
                extract_by_mask(inraster_file, inmask_file, output_file)
            except:
                print output_file


if __name__ == "__main__":
    #state_list = ["Texas", "New York", "Illinois", "Northern California", "Southern California"]
    #state_list = ["Texas", "New York", "Illinois","Arizona","Northern California","Maryland","Southern California"]
    #state_list = ["Arizona", "Maryland"]
    state_list = ["Arizona"]
    #state_day_list = [range(1, 366, 16), range(1, 366, 16), range(1, 366, 16), range(1, 366, 16), range(1, 366,16),range(1, 366,16),range(1, 366,16)]
    state_day_list = [range(1, 366, 16)]
    for index, value in enumerate(state_list):
        state = value
        create_parks(state)
        inmask_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + state + " Parks")
        task(inmask_path, state_day_list[index])
