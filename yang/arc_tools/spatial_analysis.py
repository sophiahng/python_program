# -*- coding: UTF-8 -*-
# File: spatial_analysis
# Time: 8/2/2016 -> 11:41 AM
import arcpy
import os
from arcpy.sa import ExtractByMask

__all__ = ["extract_by_mask"]

arcpy.CheckOutExtension('Spatial')


def extract_by_mask(in_raster, in_mask):
    out_raster = ExtractByMask(in_raster, in_mask)
    return out_raster
