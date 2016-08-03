# -*- coding: UTF-8 -*-
# File: data_manage
# Time: 8/2/2016 -> 12:06 PM
import arcpy

__all__ = ["get_raster_property"]


def get_raster_property(in_raster, field=None):
    res = arcpy.GetRasterProperties_management(in_raster, field)
    return res.getOutput(0)