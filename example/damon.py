# -*- coding: UTF-8 -*-
# File: damon
# Time: 7/14/2016 -> 11:03 PM
import os
import arcpy
from arcpy import env
from arcpy.sa import ExtractByMask

arcpy.CheckOutExtension('Spatial')
env.workspace = os.path.normcase("D:\yang")
env.overwriteOutput = True

OZONE_SHP_SUBDIR = os.path.normcase("G:\Environment\Ozone aot junaug layer")
REGION_MASK = os.path.normcase("D:\Dian\Data\United_States_2010\climate_region")

EVI_REGION_C_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_region\evi_C")
EVI_REGION_MASK_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_mask")


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


def evi_raster_shrink(evi_raster_path, feature_points_path, radius):
    if not os.path.exists(os.path.join(env.workspace, "feature_points_buffer.shp")):
        arcpy.Buffer_analysis(feature_points_path, "feature_points_buffer", radius, dissolve_option="ALL")
    out_raster = ExtractByMask(evi_raster_path, "feature_points_buffer.shp")
    out_raster.save("evi_raster_shrink.tif")
    return out_raster


if __name__ == "__main__":
    evi_raster_path = os.path.join(EVI_REGION_C_SUBDIR, "US20021.250m_16_days_EVI.tif")
    feature_points_path = "ozone.shp"
    shrink_evi_raster = evi_raster_shrink(evi_raster_path, feature_points_path, radius="20000 meters")
    arcpy.RasterToPoint_conversion(shrink_evi_raster, "shrink_evi.shp")
    ozone_evi_match("ozone.shp", "shrink_evi.shp", "output.shp")

















