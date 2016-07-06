from arcgis_function.fun_IDW import idw
from arcgis_function.fun_from_csv_to_shp import make_event_layer
from arcgis_function.fun_extract_by_mask import extract_by_mask
import os
import glob

AOT_SUBDIR = os.path.normcase("D:\Dian\Data\Ozone")
years = range(1990, 2015)
AOTS = ["aot49_" + str(year) + ".csv" for year in years]

input_csvs = [os.path.join(AOT_SUBDIR, aot) for aot in AOTS]
out_subdir = os.path.normcase("D:\Dian\Spatial_Image\Ozone49")

in_mask = os.path.normcase("D:/Dian/Data/United_States_2000/background/newstates.shp")

for input_csv in input_csvs:
    make_event_layer(input_csv, out_subdir, os.path.basename(input_csv)[:-4])

input_features = glob.glob(os.path.join(out_subdir, "*.shp"))

for input_feature in input_features:
    idw(input_feature, "mozone", input_feature[:-4], in_mask)









