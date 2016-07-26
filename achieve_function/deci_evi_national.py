import arcpy
import os
import glob
from arcgis_function.extract_by_mask import extract_by_mask
from arcgis_function.fun_from_raster_to_polygon import raster_polygon
from arcgis_function.fun_intersect_raster import intersect_raster
from arcgis_function.fun_calculate_polygon_area import calculate_polygon_area
from arcgis_function.fun_select_analysis import select_analysis
from arcgis_function.fun_split_features import split_features

Urban_PATH = os.path.normcase("D:\Dian\Data\United_States_2010/Urban_area_2010.shp")
EVI_PATH = os.path.normcase("G:\evi extract/")
LAND_PATH = os.path.normcase("D:\Dian\Data\Land_Use/")
REGION_PATH = os.path.normcase("D:\Dian\Data\United_States_2010/Region.shp")
OUTPUT_PATH = os.path.normcase("G:\EVI_deci_national")
# Region_names = ["Northwest", "West North Central", "West", "Southwest", "East North Central", "Central",
#                 "South", "Southeast", "Northeast"]
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

deci_intersect_file = os.path.join(OUTPUT_PATH, "deci_inter")
deci_file_names = ['deci_for_2001', 'deci_for_2006', 'deci_for_2011']
deci_files = [os.path.join(LAND_PATH, file_name) for file_name in deci_file_names]

in_rasters = []
for file in deci_files:
    in_rasters.append(file)

deci_file_intersect_path = os.path.join(deci_intersect_file, "deci_inter")
intersect_raster(in_rasters, deci_file_intersect_path, 41)

out_workspace = os.path.join(os.path.dirname(REGION_PATH),"climate_region")
split_features(REGION_PATH,REGION_PATH,"Climate",out_workspace)
Region_names = glob.glob(os.path.join(out_workspace,"*.shp"))

deci_region = os.path.join(OUTPUT_PATH, "deci_Region")

name_map_dict = {"Northwest": 'NW', "West North Central": 'WNC', "West": 'W', "Southwest": 'SW',
                 "East North Central": 'ENC', "Central": 'C', "South": 'S', "Southeast": 'SE', "Northeast": 'NE'}
for Region_name in Region_names:
    Region_deci_raster_name = "deci_" + name_map_dict[os.path.basename(Region_name)[:-4]]
    Region_deci_raster = os.path.join(deci_region, Region_deci_raster_name)
    extract_by_mask(deci_file_intersect_path, Region_name, Region_deci_raster)
    Region_deci_polygon = Region_deci_raster + ".shp"
    raster_polygon(Region_deci_raster, Region_deci_polygon)
    calculate_polygon_area(Region_deci_polygon, Region_deci_polygon[:-4] + "_area.shp")
    deci_evi_mask_subdir = os.path.join(OUTPUT_PATH, "evi_mask")
    deci_evi_mask_name = os.path.basename(Region_deci_polygon[:-4]) + "_mask.shp"
    deci_evi_mask_path = os.path.join(deci_evi_mask_subdir, deci_evi_mask_name)
    select_analysis(Region_deci_polygon[:-4] + "_area.shp", deci_evi_mask_path, "F_AREA>1000000")

evi_mask_files = glob.glob(os.path.join(deci_evi_mask_subdir, "*.shp"))
evi_files = glob.glob(os.path.join(EVI_PATH, "*.tif"))


output_sub_subdir = os.path.join(OUTPUT_PATH, 'evi_region')
if not os.path.exists(output_sub_subdir):
    os.mkdir(output_sub_subdir)
for evi_mask_file in evi_mask_files:
    mask_file_basename = os.path.basename(evi_mask_file)
    region_str = mask_file_basename[mask_file_basename.find('_')+1:mask_file_basename.rfind('_')]
    output_subdir = os.path.join(output_sub_subdir, "evi_" + region_str)
    for evi_file in evi_files:
        output_file = os.path.join(output_subdir, os.path.basename(evi_file))
        extract_by_mask(evi_file, evi_mask_file, output_file)












out_polygon = os.path.join(OUTPUT_PATH, "deci_national.shp")




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


