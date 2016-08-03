# -*- coding: UTF-8 -*-
# File: ozone_evi
# Time: 8/2/2016 -> 11:04 AM
import os
import arcpy
from arc_tools import *
from arcpy import env
import glob
import pandas as pd

env.workspace = "G:\yang\evi_base_ozone"
env.overwriteOutput = True


def shp_files_prepare():
    ozone_csv = "ozone_00_14_points.csv"
    csv_to_shp(ozone_csv, "ozone_points.shp")
    create_buffer("ozone_points.shp", "ozone_points_buffer.shp", radius="20 Kilometers")
    # print "Spliting ..."
    # shp_split("ozone_points_buffer.shp", "ozone_points_buffer.shp", "Id", "G:\yang\evi_base_ozone/ozone_points")
    ozone_points_dir = "G:\yang\evi_base_ozone/ozone_points"
    for ind in xrange(1898):
        print "Selecting {}".format(ind)
        id_value = "ozone_points_{}".format(ind)
        expression = '"Id" = ' + "'ozone_points_{}'".format(ind)
        shp_select("ozone_points_buffer.shp", os.path.join(ozone_points_dir, id_value + ".shp"), expression)


def extract_tif():
    shp_files = ["G:\yang\evi_base_ozone/ozone_points/ozone_points_{}.shp".format(ind) for ind in range(1898)]
    for shp_file in shp_files:
        means, maximums, minimums, date_times = ([], [], [], [])
        for tif_file in glob.glob(os.path.join("G:\yang\ozone_add_evi\evis_for_41", "*.tif")):
            print "Extracting {} for {}".format(os.path.basename(tif_file), os.path.basename(shp_file))
            tif_basename = os.path.basename(tif_file)
            try:
                point_raster = extract_by_mask(tif_file, shp_file)
            except:
                continue
            date_times.append("{}-{}".format(tif_basename[2:6], tif_basename[6:tif_basename.find('.')]))
            save_dir = os.path.join("G:\yang\evi_base_ozone\points_rasters", os.path.basename(shp_file)[:-4])
            if not os.path.exists(save_dir): os.mkdir(save_dir)
            point_raster.save(os.path.join(save_dir, os.path.basename(tif_file)))
            means.append(point_raster.mean)
            maximums.append(point_raster.maximum)
            minimums.append(point_raster.minimum)

        point_df = pd.DataFrame(dict(
            zip(("Datetime", "Mean", "Maximum", "Minimum"), (date_times, means, maximums, minimums))))
        point_df.to_csv(os.path.join("G:\yang\evi_base_ozone\ozone_csvs", os.path.basename(shp_file)[:-4] + ".csv"),
                        index=False)


def ozone_evi():
    shp_files_prepare()
    extract_tif()


if __name__ == "__main__":
    ozone_evi()


