# -*- coding: UTF-8 -*-
# File: damon
# Time: 7/14/2016 -> 11:03 PM
import os
import arcpy
from arcpy import env

WORK_DIR = os.path.normcase("D:\yang")



OZONE_SHP_SUBDIR = os.path.normcase("G:\Environment\Ozone aot junaug layer")
EVI_REGION_C_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_region\evi_C")
EVI_REGION_MASK_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_mask")


ozone_shp_file = os.path.join(OZONE_SHP_SUBDIR, "aotjunaug_2000layer.shp")

evi_tif_file = os.path.join(EVI_REGION_C_SUBDIR, "US20021.250m_16_days_EVI.tif")
evi_shp_file = os.path.join(WORK_DIR, "evi.shp")
# arcpy.RasterToPoint_conversion(evi_tif_file, os.path.join(WORK_DIR, "evi.shp"), "VALUE")
combine_shp_file = os.path.join(WORK_DIR, "combine1.shp")
arcpy.SpatialJoin_analysis(ozone_shp_file, evi_shp_file, combine_shp_file, "JOIN_ONE_TO_ONE", "KEEP_ALL",
                           match_option="WITHIN_A_DISTANCE", search_radius="20 KM", distance_field_name="distance")














