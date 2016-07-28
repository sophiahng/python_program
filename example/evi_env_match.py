# -*- coding: UTF-8 -*-
# File: evi_env_match
# Time: 7/15/2016 -> 11:00 PM
import arcpy
import os
from arcpy import env

env.workspace = os.path.normcase("G:\yang\evi_year_statistic")
arcpy.CheckOutExtension('Spatial')

OZONE_SHP_SUBDIR = os.path.normcase("G:\Environment")
REGION_MASK = os.path.normcase("D:\Dian\Data\United_States_2010\climate_region")

EVI_REGION_C_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_region\evi_C")
EVI_REGION_MASK_SUBDIR = os.path.normcase("G:\evi_deci_national\evi_mask")
