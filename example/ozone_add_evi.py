# -*- coding: UTF-8 -*-
# File: ozone_add_evi
# Time: 7/26/2016 -> 10:40 AM
import os
import arcpy
from arcpy import env
from arcpy.sa import Raster, ExtractByMask, SetNull, ExtractByCircle
import glob
import pandas as pd


env.workspace = "G:\yang\ozone_add_evi"
arcpy.CheckOutExtension('Spatial')

# out_raster = Raster(landcover) == 41
# out_raster.save("land_cover.tif")
#
# evi_by_mask = ExtractByMask(evi_file, "land_cover.tif")
# evi_by_mask.save("evi_by_mask.tif")



def land_cover_create():
    land_cover_template = "nlcd_{}_landcover_2011_edition_2014_10_10/nlcd_{}_landcover_2011_edition_2014_10_10.img"
    land_cover_files = [os.path.join("D:\Dian\Spatial_Files\Land_Use", land_cover_template.format(year, year))
                        for year in [2001, 2006, 2011]]
    land_covers = [SetNull(land_cover_file, 1, "VALUE <> 41") for land_cover_file in land_cover_files]
    land_cover = land_covers[0] & land_covers[1] & land_covers[2]
    return land_cover


def filter_evi(land_cover_ras):
    evi_dir = "G:\evi_extract"
    evi_files = glob.glob(os.path.join(evi_dir, "*.tif"))
    for evi_file in evi_files:
        print("Extracting {} by mask".format(evi_file))
        filted_evi = ExtractByMask(evi_file, land_cover_ras)
        filted_evi.save(os.path.join(env.workspace, "evis_for_41", os.path.basename(evi_file)))


def get_points_location():
    ozone_point_file = "G:\yang\ozone_process\ozone_data/total_ozone_sites.csv"
    ozone_pdf = pd.read_csv(ozone_point_file)
    locations = []
    for _, location in ozone_pdf.iterrows():
        locations.append(location.loc["longitude"], location.loc["latitude"])
    return locations


def calc_evi_around_point(location):
    evi_files = glob.glob(os.path.join(env.workspace, "evis_for_41", "*.tif"))
    center_point = arcpy.Point(location[0], location[1])
    for evi_file in evi_files:
        outExtCircle = ExtractByCircle(evi_file, center_point, 1000, "INSIDE")



if __name__ == "__main__":
    if not os.path.exists("land_cover.tif"):
        land_cover_ras = land_cover_create()
        land_cover_ras.save("land_cover.tif")
    else:
        land_cover_ras = "land_cover.tif"
    if not os.listdir(os.path.join(env.workspace, "evis_for_41")):
        filter_evi(land_cover_ras)
    locations = get_points_location()
    for location in locations:
        center_point = arcpy.Point(location[0], location[1])








