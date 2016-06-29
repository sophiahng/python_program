__author__ = 'Philip'


import arcpy
import os
import glob
import csv
import math
import string
from arcpy.sa import *
arcpy.env.Workspace= "D:/Dian/process/"
arcpy.env.overwriteOutput = True


def extract_by_mask(inRaster, inMaskData, output_file):
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(output_file)
    print("%s has been produced" % output_file)

def task1():
    inraster_path = os.path.normcase("D:/NDVI Process/NDVI 200300")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/NDVI CalNorth parks")
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
            year_list = range(2000, 2014)
            day_list = [209, 225, 241, 257, 273, 289]
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            inraster_file_day = [day for day in day_list if inraster_file_name.find(str(day)) == 6][0]
            output_file = os.path.join(output_dir, str(inraster_file_year) + "_" + str(inraster_file_day))
            if os.path.exists(output_file) is True:
                continue
            try:
                extract_by_mask(inraster_file, inmask_file, output_file)
            except:
                print output_file



def task2():
    inraster_path = os.path.normcase("D:/NDVI Parks/Maps/IDW/AOT MaySep")
    inmask_path = os.path.normcase("D:/NDVI Parks/New York/NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/Ozone AOT NY parks")
    inraster_file_list = [os.path.join(inraster_path, "esep_" + str(year)) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4]
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        else:
            continue
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            if inraster_file_name == "Macedonia Brook State Park.shp":
                continue
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            output_file = os.path.join(output_dir, str(inraster_file_year))
            extract_by_mask(inraster_file, inmask_file, output_file)






def task3():
    inraster_path = os.path.normcase("D:/NDVI Parks/Maps/IDW/Ozoneave Maysep")
    inmask_path = os.path.normcase("D:/NDVI Parks/New York/NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/Ozone ave NY parks")
    inraster_file_list = [os.path.join(inraster_path, "eshmaysep" + str(year)) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))

    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4]
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            output_file = os.path.join(output_dir, str(inraster_file_year))
            extract_by_mask(inraster_file, inmask_file, output_file)

def task4():
    inraster_path = os.path.normcase("D:/NDVI Parks/Maps/IDW/Prcp MaySep")
    inmask_path = os.path.normcase("D:/NDVI Parks/New York/NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/Prcp NY parks")
    inraster_file_list = [os.path.join(inraster_path, "esprcp" + str(year)) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))

    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4]
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            output_file = os.path.join(output_dir, str(inraster_file_year))
            extract_by_mask(inraster_file, inmask_file, output_file)

def task5():
    inraster_path = os.path.normcase("D:/NDVI Parks/Maps/IDW/Temptotal MaySep")
    inmask_path = os.path.normcase("D:/NDVI Parks/New York/NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/Temptotal NY parks")
    inraster_file_list = [os.path.join(inraster_path, "estempto" + str(year)) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))

    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4]
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            output_file = os.path.join(output_dir, str(inraster_file_year))
            extract_by_mask(inraster_file, inmask_file, output_file)

if __name__ == "__main__":
    for index in range(1, 2):
        task_name = "task" + str(index)
        function = eval(task_name)
        function()

