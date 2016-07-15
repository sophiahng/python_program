import arcpy
import os
from file_utils import *
from arcpy.sa import ExtractByMask

arcpy.CheckOutExtension('Spatial')

__all__ = ['extract_by_mask', 'split_features']


def extract_by_mask(in_raster, in_mask, output_path):
    path_check(output_path)
    if os.path.exists(output_path):
        print("{} has already been created before".format(output_path))
        return
    print "Extracting {} by mask {}".format(output_path, in_mask)
    temp_output = ExtractByMask(in_raster, in_mask)
    temp_output.save(output_path)


def split_features(in_feature, split_feature, split_field, out_workplace):
    path_check(out_workplace)
    if len(os.listdir(out_workplace)) > 3:
        print("{} has already been splitted before.".format(in_feature))
        return
    print("{} is splitting by {} via field name {}".format(in_feature, split_feature, str(split_field)))
    arcpy.Split_analysis(in_feature, split_feature, split_field, out_workplace)


def select_analysis(in_features, out_features, sql_clause):
    path_check(out_features)
    if path_check(out_features):
        print("{} has already been selected".format(in_features))
        return
    print "Selecting analysis {}".format(in_features)
    arcpy.Select_analysis(in_features, out_features, sql_clause)


def merge_management(in_features, out_feature):
    path_check(out_feature)
    if path_exist(out_feature):
        print("{} has already been merged".format(out_feature))
        return
    arcpy.Merge_management(in_features, out_feature)
