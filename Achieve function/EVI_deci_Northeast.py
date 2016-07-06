import arcpy
import os
import glob
from arcpy.sa import *
import arcgisscripting
from arcgis_function.fun_extract_by_mask import extract_by_mask
from arcgis_function.fun_intersect_raster import intersect_raster

NORTHEAST_PATH = os.path.normcase("D:\Dian\Data\United_States_2010\Northeast.shp")
Urban_PATH = os.path.normcase("D:\Dian\Data\United_States_2010/cb_2014_us_ua10_500k.shp")
EVI_PATH = os.path.normcase("G:\evi extract/")
LAND_PATH = os.path.normcase("D:\Dian\Data\Land_Use/")
OUTPUT_PATH = os.path.normcase("G:\EVI_deci_northeast")

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

deci_northeast = os.path.join(OUTPUT_PATH, "deci_northeast")
deci_file_names = ['deci_for_2001', 'deci_for_2006', 'deci_for_2011']
deci_files = [os.path.join(LAND_PATH, file_name) for file_name in deci_file_names]

for deci_file in deci_files:
    extract_by_mask(deci_file, NORTHEAST_PATH, deci_northeast)


in_rasters = []
for file in deci_northeast:
    in_rasters.append(file)

intersect_raster(in_rasters, os.path.normcase(deci_northeast,), 41)
# deci_files = []
# for file_name in deci_file_names:
#     file_name_paht = os.path.join(LAND_PATH, file_name)
#     deci_files.append(file_name_paht)
#
# for deci_file in deci_files:
#     func(deci_file)
#
# result = [func(deci_file) for deci_file in deci_files]
#
#
#
#
# for year in range(2000, 2015):
#     tif_files = glob.glob(os.path.join(EVI_PATH, "*.tif"))
#     tif_files = [item for item in tif_files if os.path.basename(item)[:6] == "US" + str(year)]
#     for tif_file in tif_files:
#         extract_by_mask(tif_file, maskfile)
#
# pass
#
#
#
#
# # def extract_by_mask(inRaster, inMaskData, out_subdir):
# #     output_file = os.path.join(output_subdir, os.path.basename(inRaster))
# #     if not os.path.exists(output_file):
# #         outExtractByMask = ExtractByMask(inRaster, inMaskData)
# #         outExtractByMask.save(output_file)
# #         print("%s has been produced" % output_file)
# #
# #
# # if __name__ == "__main__":
# #     gp = arcgisscripting.create()
# #     gp.CheckOutExtension("Spatial")
# #     arcpy.env.overwriteOutput = True
# #
# #     deci_subdir = "D:/Dian/Data/Land Use/"
# #     deci_file_names = ['deci_for_2001', 'deci_for_2006','deci_for_2011']
# #
# #     output_subdir = "G:\evi_NE"
# #
# #     for deci_file_name in deci_file_names:
# #         inRaster = os.path.normcase(os.path.join(deci_subdir, deci_file_name))
# #         extract_by_mask(inRaster, northeast_path, output_subdir)
# #
# #     intersec_raster = "G:\evi_NE/inter_raster"
# #     if not os.path.exists(intersec_raster):
# #         in_raster_paths = [os.path.join(output_subdir, deci_file_name) for deci_file_name in deci_file_names]
# #         logic_raster_files = map(lambda a: Raster(a) == 41, in_raster_paths)
# #         result = reduce(lambda a, b: a & b, logic_raster_files)
# #         result.save(intersec_raster)
# #
# #     intersec_polygon = "G:\evi_NE/inter_poly.shp"
# #     if not os.path.exists(intersec_polygon):
# #         gp.RasterToPolygon_conversion(intersec_raster, intersec_polygon, "NO_SIMPLIFY")
# #     calculate_output = "G:\evi_NE/poly_area.shp"
# #     if not os.path.exists(calculate_output):
# #         gp.CalculateAreas_stats(intersec_polygon, calculate_output)
# #
# #     intersec_polygon_area1 = "G:\evi_NE/poly_select.shp"
# #     if not os.path.exists(intersec_polygon_area1):
# #         gp.Select_analysis(calculate_output, intersec_polygon_area1, '"F_AREA" > 1000000')
# #     # gp.Split_analysis(intersec_polygon_area1, intersec_polygon_area1, '', 'G:\evi_NE\polygon_northeast/',
# #     #                   "5000 Meters")
# #     #
# #     # evi_raster_files = glob.glob(os.path.join("G:/evi extract/", '*.tif'))
# #     # output_subdir = 'G:\evi_NE\evi_ne'
# #     # for evi_raster_file in evi_raster_files:
# #     #     extract_by_mask(evi_raster_file, intersec_polygon_area1, output_subdir)
# #
# #
# #
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


