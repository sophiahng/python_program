from arcgis_function.Idw import idw
from arcgis_function.csv_to_shp import make_event_layer
import arcpy
import os

AOT_SUBDIR = os.path.normcase("D:\Ozone_data_process\ozone_norm_sta")
AOTS = ["ozone_raw_2012.csv"]

input_csvs = [os.path.join(AOT_SUBDIR, aot) for aot in AOTS]
out_subdir = os.path.normcase("D:\Ozone_data_process\ozone_spatial")

in_mask = os.path.normcase("D:/Dian/Spatial_Files/United_States_2000/background/newstates.shp")

for input_csv in input_csvs:
    out_shp = os.path.join(out_subdir, os.path.basename(input_csv)[:-4] + ".shp")
    make_event_layer(input_csv, out_shp)

aot_shp = os.path.join(os.path.dirname(out_shp),"AOT49.shp")
annual_shp = os.path.join(os.path.dirname(out_shp),"Ymean.shp")
arcpy.Select_analysis(out_shp, aot_shp, 'Aot4_9 > 0')
arcpy.Select_analysis(out_shp, annual_shp, 'Year_mean > 0')


idw(aot_shp, "Aot4_9", os.path.join(out_subdir,"Aotidw"), in_mask)
idw(annual_shp, "Year_mean", os.path.join(out_subdir, "Yearidw"), in_mask)





