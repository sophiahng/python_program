import os
from arcgis_function.csv_to_shp import make_event_layer
from arcgis_function.fun_add_location_UR import loc_ur
from arcgis_function.csv_file_process import add_field_by_others
from arcgis_function.csv_map_funcs import statecode_to_region
import glob
import arcpy
arcpy.env.overwriteOutput = True

URAN_PATH = os.path.normcase("D:\Dian\Data\United_States_2010")
URBAN_NAMES = ["Urban_area_1990.shp", "Urban_area_2000.shp", "Urban_area_2010.shp"]

SITELIST_SUBDIR = os.path.normcase("D:\Dian\Data\Ozone")
SITELIST_NAMES = ["sitelist_9099.csv", "sitelist_0009.csv", "sitelist_1014.csv"]

site_files = [os.path.join(SITELIST_SUBDIR, item) for item in SITELIST_NAMES]
output_subdir = "D:\Dian\Data\United_States_2010\sites_shp_of_3per/"


for site_file in site_files:
    out_file = os.path.join(output_subdir, os.path.basename(site_file)[:-4]+".shp")
    make_event_layer(site_file, out_file)

for site_name, urban_name in zip(SITELIST_NAMES, URBAN_NAMES):
    total_site = os.path.join(output_subdir, site_name[:-4] + '.shp')
    urban_polygon = os.path.join(URAN_PATH, urban_name)
    year_range = site_name[-8:-4]
    output_features = os.path.join(output_subdir, "site_ur_" + year_range + ".shp")
    loc_ur(total_site, urban_polygon, output_features)

csv_files = glob.glob(os.path.join(output_subdir, "*.csv"))
for csv_file in csv_files:
    add_field_by_others(csv_file, "region", "statecode", map_func=statecode_to_region)














