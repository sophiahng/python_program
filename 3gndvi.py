import arcpy,arcgisscripting,sys,os,os.path
import csv
import math
import string
from arcpy import env
from arcpy.sa import *
gp=arcgisscripting.create()
env.Workspace= "E:/Data/process/"
file_dir = "F:/Data/3g/2013s/"
mask_path = "C:/Dian/United States/background/"
out_path = "F:/Data/3g/Data2010s/"
tmp_path= "E:/Data/process/"
arcpy.env.overwriteOutput = True

# you can alter the file directory as 'C:\data\xxx'

file_name = [file for file in os.listdir(file_dir) if file[-9:] == '.ndvi.asc']
for file in file_name:
    print file[3:11]
    inRaster = file_dir + file
    inMaskData = mask_path+"newstates"+".shp"
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(out_path + file[3:11]+"ndvi")

   
 
