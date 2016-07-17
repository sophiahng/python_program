from arcgis_function.fun_IDW import idw
from arcgis_function.csv_to_shp import make_event_layer
import os
import glob

AOT_SUBDIR = os.path.normcase("D:\Dian\Data/Ozone")
AOTS = ["dayave_mean.csv"]

input_csvs = [os.path.join(AOT_SUBDIR, aot) for aot in AOTS]
out_subdir = os.path.normcase("D:\Dian\Spatial_Image/Try_average")

in_mask = os.path.normcase("D:/Dian/Data/United_States_2000/background/newstates.shp")

for input_csv in input_csvs:
    out_shp = os.path.join(out_subdir, os.path.basename(input_csv)[:-4] + ".shp")
    make_event_layer(input_csv, out_shp)

input_features = [out_shp]

for input_feature in input_features:
    idw(input_feature, "ozone", input_feature[:-4], in_mask)

