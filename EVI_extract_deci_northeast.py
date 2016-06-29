import arcpy
import os
import glob
import csv
import math
import string
from arcpy import env
from dbfpy import dbf
from arcpy.sa import *
import arcgisscripting


# arcpy.env.Workspace= "D:/Dian/process/"
# evi_path = "G:/evi extract/"
# deci_path = "D:/Dian/Data/Land Use/"
# northeast_path = "D:/Dian/Data/United States 2010/Northeast.shp"
#
# inRaster = deci
#
# def extract_by_mask(inRaster, inMaskData, output_file):
#     arcpy.CheckOutExtension("Spatial")
#     outExtractByMask = ExtractByMask(inRaster, inMaskData)
#     outExtractByMask.save(output_file)
#     print("%s has been produced" % output_file)

# expression= ("raster1" == 41) & ("raster2" == 41) & ("raster3" == 41)
# RasterCalculator (expression, output_raster)
#
# 3)	Convert the output of step 2 (output_raster) to polygon
# In_raster = output + inter_deci.img
# Out_polygon = output + interse_deci.shp
# RasterToPolygon_conversion (in_raster, out_polygon_features, {simplify})
#
#
# 4)	Extract by pixel area
# Out_feature = output + deci1.shp
#    arcpy.Select_analysis(output + interse_deci.shp, out_features,  '"AREA" > 1')
#
#
#
#
#
# clean_path = "D:/Dian/Spatial Image/CAST/"
# ozone_path = "D:/Dian/Spatial Image/Ozone 24h ave/"
# out_workspace = "D:/Dian/Spatial Image/Ozone 24h ave regression/"
# tmp_path= "D:/Dian/process/"
# mask_path = "D:/Dian/Data/United States 2000/background/"
#

def extract_by_mask(inRaster, inMaskData, out_subdir):
    output_file = os.path.join(output_subdir, os.path.basename(inRaster))
    if not os.path.exists(output_file):
        outExtractByMask = ExtractByMask(inRaster, inMaskData)
        outExtractByMask.save(output_file)
        print("%s has been produced" % output_file)


if __name__ == "__main__":
    gp = arcgisscripting.create()
    gp.CheckOutExtension("Spatial")
    arcpy.env.overwriteOutput = True

    deci_subdir = "D:/Dian/Data/Land Use/"
    deci_file_names = ['deci_for_2001', 'deci_for_2006','deci_for_2011']
    northeast_path = "D:/Dian/Data/United States 2010/Northeast.shp"
    output_subdir = "G:\evi_NE"

    for deci_file_name in deci_file_names:
        inRaster = os.path.normcase(os.path.join(deci_subdir, deci_file_name))
        extract_by_mask(inRaster, northeast_path, output_subdir)

    intersec_raster = "G:\evi_NE/inter_raster"
    if not os.path.exists(intersec_raster):
        in_raster_paths = [os.path.join(output_subdir, deci_file_name) for deci_file_name in deci_file_names]
        logic_raster_files = map(lambda a: Raster(a) == 41, in_raster_paths)
        result = reduce(lambda a, b: a & b, logic_raster_files)
        result.save(intersec_raster)

    intersec_polygon = "G:\evi_NE/inter_poly.shp"
    if not os.path.exists(intersec_polygon):
        gp.RasterToPolygon_conversion(intersec_raster, intersec_polygon, "NO_SIMPLIFY")
    calculate_output = "G:\evi_NE/poly_area.shp"
    if not os.path.exists(calculate_output):
        gp.CalculateAreas_stats(intersec_polygon, calculate_output)

    intersec_polygon_area1 = "G:\evi_NE/poly_select.shp"
    if not os.path.exists(intersec_polygon_area1):
        gp.Select_analysis(calculate_output, intersec_polygon_area1, '"F_AREA" > 1000000')
    # gp.Split_analysis(intersec_polygon_area1, intersec_polygon_area1, '', 'G:\evi_NE\polygon_northeast/',
    #                   "5000 Meters")
    #
    # evi_raster_files = glob.glob(os.path.join("G:/evi extract/", '*.tif'))
    # output_subdir = 'G:\evi_NE\evi_ne'
    # for evi_raster_file in evi_raster_files:
    #     extract_by_mask(evi_raster_file, intersec_polygon_area1, output_subdir)






























