
__author__ = 'Sophia'

import arcpy, arcinfo
import os
import glob
import csv
import math
import string
from arcpy import env
from dbfpy import dbf
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')

arcpy.env.Workspace = "D:/Dian/process/"
ozone_path = "D:/Dian/Data/Ozone/"
clean_path = "D:/Dian/Spatial_Image/CAST/"
us2010_path = "D:/Dian/Data/United_States_2010/"
tmp_path = "D:/arcgis/tmp/"
out_path = "D:/Dian/Spatial_Image/Add attributes/"
mask_path = "D:/Dian/Data/United_States_2000/background/"
arcpy.env.overwriteOutput = True

site = "sitelist_"
year = 2000

while year < 2001:
    in_table = ozone_path+site+str(year)+".csv"
    x_coords = "longitude"
    y_coords = "latitude"
    out_layer = "event"+str(year)+".shp"
    spRef = r"D:/Dian/Data/United_States_2000/background/Coordinate.prj"
    arcpy.MakeXYEventLayer_management(in_table, x_coords, y_coords, out_layer, spRef)
    arcpy.FeatureClassToShapefile_conversion(out_layer, out_path)
    print "event " + str(year)

    # Extract multiple values to points
    inRasters1 = "D:/Dian/Data/US_DEM/US_dem.tif"
    inRasters2 = "D:/Dian/Spatial_Image/Night_Image/nightri2013.tif"
    inPoints = out_path+"event"+str(year)+".shp"
    inRasters3 = out_path + "nlcd_2011_landcover_2011_edition_2014_10_10/" + "nlcd_2011_landcover_2011_edition_2014_10_10.img"
    ExtractMultiValuesToPoints(inPoints, [[inRasters1, "elevation"], [inRasters2, "nightlight"]], "BILINEAR")
    ExtractMultiValuesToPoints(inPoints, [inRasters3], "BILINEAR")

    urban_polygon = us2010_path + "cb_2014_us_ua10_500k" + ".shp"
    urban_sites = out_path + "urban" + ".shp"
    sites = out_path + "event" + str(year) + ".shp"
    arcpy.Clip_analysis(sites, urban_polygon, urban_sites)

    clean_input = clean_path + "CASTMEAN_" + str(year) + ".shp"
    clean_sites = out_path + "clean" + ".shp"
    bufferOutput = out_path + "clebuf_10k" + ".shp"
    bufferDist = "10000 Meters"
    arcpy.Buffer_analysis(clean_input, bufferOutput, bufferDist)
    arcpy.Clip_analysis(sites, bufferOutput, clean_sites)

    erase_1 = out_path + "erase_1" + ".shp"
    rural_sites = out_path + "rural" + ".shp"
    arcpy.Erase_analysis(sites, clean_sites, erase_1, "")
    arcpy.Erase_analysis(erase_1, urban_sites, rural_sites, "")

    arcpy.AddField_management(urban_sites, "location", "TEXT", field_length=50)
    arcpy.AddField_management(clean_sites, "location", "TEXT", field_length=50)
    arcpy.AddField_management(rural_sites, "location", "TEXT", field_length=50)

    with arcpy.da.UpdateCursor(urban_sites, "location") as cursor:
        for row in cursor:
            for i in range(len(row)):
                row[i] = "Urban"
                cursor.updateRow(row)

    with arcpy.da.UpdateCursor(rural_sites, "location") as cursor:
        for row in cursor:
            for i in range(len(row)):
                row[i] = "Rural"
                cursor.updateRow(row)

    with arcpy.da.UpdateCursor(clean_sites, "location") as cursor:
        for row in cursor:
            for i in range(len(row)):
                row[i] = "Clean"
                cursor.updateRow(row)

    out_feature = out_path + "urban_sites" + ".shp"
    major_city = us2010_path + "major_cities" + ".shp"
    arcpy.SpatialJoin_analysis(urban_sites, major_city, out_feature, "#", "#", "#", "CLOSEST")

    inFeatures = [out_feature, clean_sites, rural_sites]
    outFeatures = out_path + "Sitelist_new_" + str(year)+ ".shp"
    arcpy.Merge_management(inFeatures, outFeatures)

    in_putdbf = outFeatures[:-4] + '.dbf'
    csv_fn = outFeatures[:-4] + '.csv'
    with open(csv_fn, 'wb') as csvfile:
        in_db = dbf.Dbf(in_putdbf)
        out_csv = csv.writer(csvfile)
        names = []
        for field in in_db.header.fields:
            names.append(field.name)
        out_csv.writerow(names)
        for rec in in_db:
            out_csv.writerow(rec.fieldData)
        in_db.close()
        print "Done..."


    year = year +1

