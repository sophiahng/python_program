# -*- coding: UTF-8 -*-
# File: Environment_csv_to_shp
# Time: 8/1/2016 -> 11:06 AM
import os
from arcgis_function.csv_to_shp import make_event_layer
import arcpy

Temp_subdir = os.path.normcase("G:\Environment\Temp")
Temp = "temp_points.csv"
out_subdir = os.path.normcase("G:\Environment\Environment_spatial")
Prcp_subdir = os.path.normcase("G:\Environment\Prcp")
Prcp = "prcp_points.csv"

Temp_csv = os.path.join(Temp_subdir, Temp)
Temp_shp = os.path.join(out_subdir, Temp[:-4] + ".shp")
make_event_layer(Temp_csv, Temp_shp)

Prcp_csv = os.path.join(Prcp_subdir, Prcp)
Prcp_shp = os.path.join(out_subdir, Prcp[:-4] + ".shp")
make_event_layer(Prcp_csv, Prcp_shp)

target_shp = os.path.join(out_subdir, "ozone_points.shp")
ozone_temp = os.path.join(out_subdir,"ozone_temp_join.shp")

# arcpy.Select_analysis(out_shp, aot_shp, 'Aot4_9 > 0')
