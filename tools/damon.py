# -*- coding: UTF-8 -*-
# File: damon
# Time: 7/14/2016 -> 11:03 PM
import os
import arcpy
from arcpy import env


env.workspace = os.path.normcase("D:\yang")
env.overwriteOutput = True

OZONE_SHP_SUBDIR = os.path.normcase("G:\Environment\Ozone aot junaug layer")
REGION_MASK = os.path.normcase("D:\Dian\Data\United_States_2010\climate_region")

EVI_REGION_C_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_region\evi_C")
EVI_REGION_MASK_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_mask")



#
# ozone_shp_file = os.path.join(OZONE_SHP_SUBDIR, "aotjunaug_2000layer.shp")
#
# evi_tif_file = os.path.join(EVI_REGION_C_SUBDIR, "US20021.250m_16_days_EVI.tif")
# evi_shp_file = os.path.join(WORK_DIR, "evi.shp")
# # arcpy.RasterToPoint_conversion(evi_tif_file, os.path.join(WORK_DIR, "evi.shp"), "VALUE")
# combine_shp_file = os.path.join(WORK_DIR, "combine1.shp")
# arcpy.SpatialJoin_analysis(ozone_shp_file, evi_shp_file, combine_shp_file, "JOIN_ONE_TO_ONE", "KEEP_ALL",
#                            match_option="WITHIN_A_DISTANCE", search_radius="20 KM", distance_field_name="distance")


def ozone_evi_match(ozone_shp_file, evi_shp_file, output_shp_file):
    target_features = ozone_shp_file
    join_features = evi_shp_file
    output_features = output_shp_file

    field_mappings = arcpy.FieldMappings()
    field_mappings.addTable(target_features)
    field_mappings.addTable(join_features)
    grid_code_field_index = field_mappings.findFieldMapIndex("GRID_CODE")
    grid_code_field_map = field_mappings.getFieldMap(grid_code_field_index)
    field = grid_code_field_map.outputField
    field.name = "evi_value"
    field.aliasName = "evi_value"
    grid_code_field_map.outputField = field
    grid_code_field_map.mergeRule = "mean"
    field_mappings.replaceFieldMap(grid_code_field_index, grid_code_field_map)
    arcpy.SpatialJoin_analysis(target_features, join_features, output_features, "JOIN_ONE_TO_ONE", "KEEP_COMMON",
                               field_mappings, "WITHIN_A_DISTANCE", search_radius=20000)



# central_mask_shp = os.path.join(REGION_MASK, "Central.shp")
# arcpy.Clip_analysis(os.path.join(OZONE_SHP_SUBDIR, "aotjunaug_2000layer.shp"), central_mask_shp, "ozone.shp")

ozone_shp_file = "ozone.shp"
evi_shp_file = "evi.shp"
output_shp_file = "output.shp"

ozone_evi_match(ozone_shp_file, evi_shp_file, output_shp_file)















