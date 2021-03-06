import os
from arcgis_function.csv_to_shp import make_event_layer
from arcgis_function.add_location_URC import loc_urc
import arcpy
arcpy.env.overwriteOutput = True


sitelist_path = "G:\yang\ozone_process/ozone_data/ozone_points_all.csv"
clean_path = "D:\Dian\Data/2012/Castnetsites.csv"

output_subdir = "G:\yang\ozone_process/ozone_data/"

sitelist_shp = os.path.join(output_subdir, os.path.basename(sitelist_path)[:-4] + ".shp")
clean_shp = os.path.join(output_subdir, os.path.basename(clean_path)[:-4] + ".shp")

make_event_layer(sitelist_path, sitelist_shp)
make_event_layer(clean_path, clean_shp)


urban_polygon = "D:\Dian\Spatial_Files\United_States_2010/Urban_area_2010.shp"
loc_urc(sitelist_shp, urban_polygon, cast_sites=clean_shp, out_features=os.path.join(output_subdir, "sitelist_urc.shp"))


