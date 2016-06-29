# -*- coding: cp936 -*-
import arcpy,arcgisscripting,csv,sys,os,os.path
import math
import string
from arcpy import env
from arcpy.sa import *
env.Workspace= "C:/Dian/process/"
in_path = "C:/Dian/Ozone data phython/"
tmp_path= "C:/arcgis/tmp/"
out_path = "C:/Dian/Ozone data phython1/"

year = 1980

# select layer by location
arcpy.MakeFeatureLayer_management(in_path+"ests"+str(year)+".shp", 'elyr'+str(year))
arcpy.SelectLayerByLocation_management('elyr'+str(year), 'intersect', in_path+"Urbanized_area"+".shp")
arcpy.CopyFeatures_management("elyr"+str(year),out_path+'usits'+str(year))
print "usits " +str(year)

#export usits attribute to txt
input_features = out_path+"usits"+str(year)+".shp"
export_ASCII = "usits"+str(year)+".txt"
arcpy.ExportXYv_stats(input_features, "YEAR", "SPACE", export_ASCII, "ADD_FIELD_NAMES")


gp=arcgisscripting.create()
output=open(r+str(year)+'.csv','w')
linewriter=csv.writer(output,delimiter=',')
fcdescribe=gp.Describe(out_path+'usits'+'.shp')
flds=fcdescribe.Fields

header=[]
for fld in flds:
    value=fld.Name
    header.append(value)
linewriter.writerow(header)

cursor=gp.SearchCursor(out_path+'usits'+'.shp')
row=cursor.Next()

while row:
    line=[]
    for fld in flds:
        value=row.GetValue(fld.Name)
        line.append(value)
    linewriter.writerow(line)
    del line
    row=cursor.Next()
    
del cursor
output.close()

input_features = "usits"+str(year)+".shp"
export_ASCII = "usits"+str(year)+".txt"
arcpy.ExportXYv_stats(input_features, 'MEAN', "COMMA", export_ASCII, "ADD_FIELD_NAMES")
    


