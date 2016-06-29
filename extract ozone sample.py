import arcpy,arcgisscripting,sys,os,os.path
import csv
import math
import string
from arcpy import env
from arcpy.sa import *
gp=arcgisscripting.create()
env.Workspace= "C:/Dian/process/"
in_p = "C:/Dian/Data/Temp data/"
in_r = "C:/Dian/Spatial Image/Ozone 24h ave/"
tmp_path= "C:/arcgis/tmp/"
out_path = "C:/Dian/Spatial Image/24h ozone value derived by temp/"
mask_path = "C:/Dian/United States/background/"

site="TEMP24h_"
year = 1980


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
outpoint = out_path + "Tempozone" + str(year) + ".shp"
arcpy.CheckOutExtension("Spatial")
ExtractValuesToPoints(in_point, in_raster, outpoint)
print "Tempozone" + str(year)

#here I want to export the attribute table of the shapfile 
input_features = out_path+"Tempozone"+str(year)+".shp"
export_ASCII = out_path+"Tempozone"+str(year)+".txt"
arcpy.env.workspace = env.workspace
arcpy.ExportXYv_stats(input_features,["YEAR","STATECODE","COUNTYCODE","SITENUM", "LATITUDE", "LONGITUDE", "MEAN","SD", "RASTERVALU"], "COMMA", export_ASCII, "ADD_FIELD_NAMES")
print "TPOZ" +str(year)
    
   



