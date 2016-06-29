# -*- coding: cp936 -*-
import arcpy,arcgisscripting,csv,sys,os,os.path
import math
import string
from arcpy import env
from arcpy.sa import *
env.Workspace= "C:/Dian/process/"
in_path = "C:/Dian/step1/"
tmp_path= "C:/arcgis/tmp/"
out_path = "C:/Dian/step2/"
mask_path = "C:/Dian/United States/background/"

year = 1980

while year<2014:
    # select layer by location
    arcpy.MakeFeatureLayer_management(in_path+"ests"+str(year)+".shp", 'elyr'+str(year))
    arcpy.SelectLayerByLocation_management('elyr'+str(year), 'intersect', mask_path+"Urbanized_area"+".shp")
    arcpy.CopyFeatures_management("elyr"+str(year),out_path+'usits'+str(year))
    print "usits " +str(year)
    # get the nusits by erase
    in_features=in_path+"ests"+str(year)+".shp"
    erase_features=out_path+'usits'+str(year)+".shp"
    out_feature_class=out_path+'nusits'+str(year)+".shp"
    arcpy.Erase_analysis(in_features, erase_features, out_feature_class)
    print "nusits " +str(year)
    #export usits attribute to txt
    input_features = out_path+"usits"+str(year)+".shp"
    export_ASCII = out_path+"usits"+str(year)+".txt"
    arcpy.ExportXYv_stats(input_features, ["YEAR","STATECODE","COUNTYCODE","SITENUM","MEAN","SD"], "COMMA", export_ASCII, "ADD_FIELD_NAMES")
    print "usits " +str(year)
    #export nusits attribute to txt
    input_features = out_path+"nusits"+str(year)+".shp"
    export_ASCII = out_path+"nusits"+str(year)+".txt"
    arcpy.ExportXYv_stats(input_features, ["YEAR","STATECODE","COUNTYCODE","SITENUM","MEAN","SD"], "COMMA", export_ASCII, "ADD_FIELD_NAMES")
    print "nusits " +str(year)
    year=year+1


