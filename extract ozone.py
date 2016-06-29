import arcpy,arcgisscripting,sys,os,os.path
import csv
import math
import string
from arcpy import env
from arcpy.sa import *
gp=arcgisscripting.create()
env.Workspace= "C:/Dian/process/"
in_p = "C:/Dian/Data/NO2/"
in_r = "C:/Dian/Spatial Image/Ozone 24h ave/"
tmp_path= "C:/arcgis/tmp/"
out_path = "C:/Dian/Spatial Image/Ozone NO2 24h/"
mask_path = "C:/Dian/United States/background/"

site="24hNO2_"
year = 1990

while year<2014:
    in_Table = in_p + site + str(year) + ".csv"
    out_name = "dbf" + str(year)
    arcpy.TableToTable_conversion(in_Table,out_path,out_name)
    print "process dbf " + str(year)
    in_table = out_path+out_name
    x_coords="Longitude"
    y_coords="Latitude"
    z_coords="mean"
    out_layer="event"+str(year)
    saved_layer = out_path+"event"+str(year)+".lyr"
    spRef = r"c:\Dian\United States\background\Coordinate.prj"
    arcpy.MakeXYEventLayer_management(in_table,x_coords,y_coords,out_layer,spRef,z_coords)
    arcpy.SaveToLayerFile_management(out_layer, saved_layer)
    gp.FeatureClassToShapefile(saved_layer,out_path)
    print "event " + str(year)
    
    in_point = out_path + "event" + str(year) + ".lyr"
    in_raster = in_r + "estats" + str(year)
    outpoint = out_path + "NO2ozone_" + str(year) + ".shp"
    arcpy.CheckOutExtension("Spatial")
    ExtractValuesToPoints(in_point, in_raster, outpoint)
    print "NO2ozone" + str(year)

    input_features = out_path+"NO2ozone_"+str(year)+".shp"
    export_ASCII = out_path+"NO2ozone_"+str(year)+".txt"
    arcpy.env.workspace = env.workspace
    arcpy.ExportXYv_stats(input_features,["YEAR","STATECODE","COUNTYCODE","SITENUM", "LATITUDE", "LONGITUDE", "MEAN","SD", "RASTERVALU"], "COMMA", export_ASCII, "ADD_FIELD_NAMES")
    print "TPOZ" +str(year)
    
    year = year + 1



