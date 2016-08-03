# -*- coding: UTF-8 -*-
# File: analysis
# Time: 8/2/2016 -> 11:22 AM
import arcpy

arcpy.CheckOutExtension('Spatial')

__all__ = ["create_buffer", "shp_split", "shp_select"]


def create_buffer(input_shp, output_shp, radius="20000 meters"):
    arcpy.Buffer_analysis(input_shp, output_shp, radius)


def shp_split(in_features, split_features, split_field, out_workplace):
    arcpy.Split_analysis(in_features, split_features, split_field, out_workplace)


def shp_select(in_shp, out_shp, expression):
    arcpy.Select_analysis(in_shp, out_shp, expression)