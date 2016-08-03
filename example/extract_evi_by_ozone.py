# -*- coding: UTF-8 -*-
# File: extract_evi_by_ozone
# Time: 8/1/2016 -> 11:07 PM
import os
import arcpy
from arcpy import env
from arcpy.sa import ZonalStatisticsAsTable
# import gc
# gc.enable()


def make_event_layer(csv_file, shp_file):
    if not os.path.exists(os.path.dirname(shp_file)): os.mkdir(os.path.dirname(shp_file))
    if os.path.exists(shp_file): return
    x_coords = "Longitude"
    y_coords = "Latitude"
    spRef = r"D:/Dian/Spatial_Files/United_States_2000/background/Coordinate.prj"
    shp_basename = os.path.basename(shp_file)[:-4]
    arcpy.MakeXYEventLayer_management(csv_file, x_coords, y_coords, shp_basename, spRef)
    # arcpy.SaveToLayerFile_management(out_layer, saved_layer)
    arcpy.FeatureToPoint_management(shp_basename, shp_file)


def zonal_sta(shp_file, tif_file):
    inZoneData = shp_file
    zoneField = "FID"
    inValueRaster = tif_file
    outTable = "zonalstattblout.dbf"

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute ZonalStatisticsAsTable
    outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster,
                                     outTable, "DATA", "MEAN")


if __name__ == "__main__":
    env.workspace = "G:\yang\evi_base_ozone"
    csv_file = "G:\yang\evi_base_ozone/ozone_00_14_points.csv"
    shp_file = "G:\yang\evi_base_ozone/ozone_00_14_points.shp"
    make_event_layer(csv_file, shp_file)
    tif_file = "G:\yang\ozone_add_evi\evis_for_41/US20021.250m_16_days_EVI.tif"
    # zonal_sta(shp_file, tif_file)
