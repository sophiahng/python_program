
__author__ = 'Sophia'

import arcpy, arcinfo
import os
import glob
import csv
import sys
import math
import threading
import string
from arcpy import env
from dbfpy import dbf
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True

INPUT_DIRS = ["D:/Dian/Spatial Image/Add attributes/", "D:/Dian/Spatial Image/Night Image/F16_20100111-20110731_rad_v4.geotiff/"]
OUTPUT_DIR = "D:/Dian/Spatial Image/Human activity/"
FILENAMES = ["Sitelist_new_2014.shp", "F16_20100111-20110731_rad_v4.avg_vis.tif"]


def split_analysis(split_features, radius):
    split_field = "id"
    output_workspace = os.path.normcase(os.path.join(OUTPUT_DIR, split_field + str(radius)))
    if not os.path.exists(output_workspace):
        os.mkdir(output_workspace)
    try:
        arcpy.Split_analysis(split_features, split_features, split_field, output_workspace)
    except:
        raise Exception("split process")
    return output_workspace


def extract_by_mask(inRaster, inMaskData, output_file):
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(output_file)
    print("%s has been produced" % output_file)


def buffer_analysis(radius):
    input_file_path = os.path.normcase(os.path.join(INPUT_DIRS[0], FILENAMES[0]))
    input_features = arcpy.mapping.Layer(input_file_path)
    output_filename = "sitelist_2014_buffer.shp"
    output_features = os.path.normcase(os.path.join(OUTPUT_DIR, output_filename))
    assert type(radius) is int
    radius_meters = "{} Kilometers".format(radius)
    arcpy.Buffer_analysis(input_features, output_features, "10 Kilometers")
    return output_features


def extract(output_workspace, radius):
    shp_files = glob.glob(os.path.join(output_workspace, "*.shp"))
    inraster_file = os.path.normcase(os.path.join(INPUT_DIRS[1], FILENAMES[1]))
    output_dir = os.path.normcase(os.path.join(OUTPUT_DIR, "tiff" + str(radius)))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for shp_file in shp_files:
        output_path = os.path.join(output_dir, os.path.split(shp_file)[-1][:-4])
        extract_by_mask(inraster_file, shp_file, output_path)
    return output_dir


def tif_mean_sta(output_dir):
    subdirs = os.listdir(output_dir)
    subdirs = [os.path.join(output_dir, subdir) for subdir in subdirs if os.path.isdir(os.path.join(output_dir, subdir))]
    def get_mean(subdir):
        try:
            elevSTDResult = arcpy.GetRasterProperties_management(subdir, "MEAN")
        except:
            return "error"
        return elevSTDResult.getOutput(0)
    mean_list = [(os.path.split(subdir)[-1], get_mean(subdir)) for subdir in subdirs]
    output_path = os.path.join(output_dir, "sitelist.csv")
    with file(output_path, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        for tiff_filename, mean_value in mean_list:
            output_writer.writerow([tiff_filename, mean_value])


def ozone_radius(radius):
    output_features = buffer_analysis(radius)
    output_workspace = split_analysis(output_features, radius)
    output_dir = extract(output_workspace, radius)
    # output_dir = os.path.normcase(os.path.join(OUTPUT_DIR + "tiff"))
    tif_mean_sta(output_dir)


if __name__ == "__main__":
    for radius in range(4, 11):
        ozone_radius(radius)





