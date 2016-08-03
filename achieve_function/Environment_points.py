# -*- coding: UTF-8 -*-
# File: Environment_points
# Time: 7/28/2016 -> 5:58 PM

from arcgis_function.csv_to_shp import make_event_layer

import os

AOT_SUBDIR = os.path.normcase("G:\Environment")
AOTS = ["stations.csv"]

input_csvs = [os.path.join(AOT_SUBDIR, aot) for aot in AOTS]
out_subdir = os.path.normcase("G:\Environment\Environment_spatial")

in_mask = os.path.normcase("D:/Dian/Spatial_Files/United_States_2000/background/newstates.shp")

for input_csv in input_csvs:
    out_shp = os.path.join(out_subdir, os.path.basename(input_csv)[:-4] + ".shp")
    make_event_layer(input_csv, out_shp)