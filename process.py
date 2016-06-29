# coding=utf-8
__author__ = 'Philip'

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



def intersect(polygon_path, target_path):
    if os.path.exists(polygon_path) is not True:
        print("%s is not existed"%polygon_path)
        return

    polygon_file_list = glob.glob(os.path.join(polygon_path, "*.shp"))
    polygon_file_list = [os.path.split(polygon_file)[-1] for polygon_file in polygon_file_list]
    day_set = set([int(polygon_file[6:polygon_file.find(".")]) for polygon_file in polygon_file_list])
    for day in day_set:
        polygon_file_day_list = [os.path.join(polygon_path, polygon_file) for polygon_file in polygon_file_list if int(polygon_file[6:polygon_file.find(".")]) == day]
        polygon_file_year_day_list = [os.path.join(polygon_path, polygon_file) for polygon_file in polygon_file_list if int(polygon_file[2:6]) in range(2007, 2014)]
        intersect_output_file = os.path.join(os.path.join(target_path, "20072013"), "polygen_intersect_" + str(day) + ".shp")
        arcpy.Intersect_analysis(polygon_file_year_day_list, intersect_output_file)

        polygon_file_year_day_list1 = [os.path.join(polygon_path, polygon_file) for polygon_file in polygon_file_list if int(polygon_file[2:6]) in range(2000, 2007)]
        intersect_output_file = os.path.join(os.path.join(target_path, "20002006"), "polygen_intersect_" + str(day) + ".shp")
        arcpy.Intersect_analysis(polygon_file_year_day_list1, intersect_output_file)


def extract_by_mask(intersect_path, raster_path, target_path):
    if os.path.exists(intersect_path) is not True:
        print("%s is not existed"%intersect_path)
        return
    if os.path.exists(raster_path):
        print("%s is not existed"%raster_path)
        return
    if os.path.exists(target_path):
        print("%s is not existed"%target_path)
        return

    intersect_file_list = glob.glob(os.path.join(intersect_path, "*.shp"))
    intersect_file_list = [os.path.split(intersect_file)[-1] for intersect_file in intersect_file_list]
    day_set = set([int(intersect_file[17:intersect_file.find(".")]) for intersect_file in intersect_file_list])
    raster_file_list = glob.glob(os.path.join(raster_path, "*.tif"))
    raster_file_list = [os.path.split(raster_file) for raster_file in raster_file_list]

    for day in day_set:
        intersect_file = os.path.join(intersect_path, "polygen_intersect_" + str(day) + ".shp")
        if os.path.exists(intersect_file) is not True:
            print("%s is not exited" %intersect_file)
            continue
        raster_file_day_list = [os.path.join(raster_path, raster_file) for raster_file in raster_file_list if int(raster_file[6:raster_file.find(".")]) == day]
        raster_file_year_day_list = [os.path.join(raster_path, raster_file) for raster_file in raster_file_list if int(raster_file[2:6]) in range(2007, 2013)]
        for raster_file in raster_file_year_day_list:
            arcpy.CheckOutExtension("Spatial")
            target_file = raster_file[:-4] + "_mask.tif"
            outExtractByMask = ExtractByMask(raster_file, intersect_file)
            outExtractByMask.save(target_file)


if __name__ == "__main__":
    #rasterpath = os.path.normcase("D:/NDVI Process/MaySep/3K/Extract NDVI by mask4/over 4000")
    #targetpath = os.path.normcase("D:/NDVI Process/MaySepshp/3K")
    #raster_to_polygen(rasterpath, targetpath)

    print "Hello"
    polygon_path = os.path.normcase("D:/NDVI Process/MaySepshp/3K")
    target_path = os.path.normcase("D:/NDVI Process/intersect/MaySep/3K")
    intersect(polygon_path, target_path)
    print "complete"










