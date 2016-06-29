# coding=utf-8
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




def task1():
    inraster_path = os.path.normcase("D:/NDVI Process/Ozone layer/Average/MaySep")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_ave_maysep")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)


def task2():
    inraster_path = os.path.normcase("D:/NDVI Process/Ozone layer/AOT40/MaySep")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_aot_maysep")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)

def task3():
    inraster_path = os.path.normcase("D:/NDVI Process/Climate layer/Prcp")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorthParks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_prcp")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0]
            if len(inraster_file_year) == 0:
                continue
            inraster_file_year = inraster_file_year[0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)

def task4():
    inraster_path = os.path.normcase("D:/NDVI Process/Climate layer/Temptotal")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_temp")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0]
            if len(inraster_file_year) == 0:
                continue
            inraster_file_year = inraster_file_year[0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)

if __name__ == "__main__":
    for index in range(1,5):
        task_name = "task" + str(index)
        function = eval(task_name)
        function()