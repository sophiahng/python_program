__author__ = 'Sophia'

import arcpy,arcgisscripting,sys,os,os.path
import csv
import math
import string
import glob
from arcpy import env
from arcpy.sa import *
FILEPATH = "D:/NDVI Process/NDVI 200300/"
MASKDATAPATH1 = os.path.normcase("D:/NDVI Process/Ozone Buffer/Average/Ozone 3km/MaySep/")
MASKDATAPATH2 = "D:/NDVI Process/Ozone Buffer/AOT40/Ozone 3km/MaySep/"
MASKDATAPATH3 = "D:/NDVI Process/Climate Buffer/T total 3km MaySep/"
MASKDATAPATH4 ="D:/NDVI Process/Climate Buffer/Climate 5km/Prcp buffer/"
OUTPATH1 = "D:/NDVI Process/MaySep/3K/Extract NDVI by mask1/"
OUTPATH2 = "D:/NDVI Process/MaySep/3K/Extract NDVI by mask2/"
OUTPATH3 = "D:/NDVI Process/MaySep/3K/Extract NDVI by mask3/"
OUTPATH4 = "D:/NDVI Process/MaySep/3K/Extract NDVI by mask4/"
env.Workspace= "D:/NDVI Process/Environment"
#arcpy.env.overwriteOutput = True

def extract(input, output, mask_data):
    inRaster = input
    inMaskData = mask_data
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(output)

if __name__ == '__main__':
    file_list = glob.glob(os.path.join(FILEPATH, '*.tif'))
    for filename in file_list:
        print filename
        name = os.path.split(filename)[1]
        year_number = int(name[2:6])
        output_name = os.path.join(OUTPATH1, name)
        print output_name
        MASKDATAPATH = MASKDATAPATH1 +"24hmaysep3k"+str(year_number)+".shp"
        extract(filename, output_name, MASKDATAPATH)
    file_list = glob.glob(os.path.join(OUTPATH1, '*.tif'))
    for filename in file_list:
        print filename
        name = os.path.split(filename)[1]
        year_number = int(name[2:6])
        output_name = os.path.join(OUTPATH2, name)
        print output_name
        MASKDATAPATH = MASKDATAPATH2 +"aotmaysep3k"+str(year_number)+".shp"
        extract(filename, output_name, MASKDATAPATH)
    file_list = glob.glob(os.path.join(OUTPATH2, '*.tif'))
    for filename in file_list:
        print filename
        name = os.path.split(filename)[1]
        year_number = int(name[2:6])
        output_name = os.path.join(OUTPATH3, name)
        print output_name
        MASKDATAPATH = MASKDATAPATH3 +str(year_number)+"_union"+".shp"
        extract(filename, output_name, MASKDATAPATH)
    file_list = glob.glob(os.path.join(OUTPATH3, '*.tif'))
    for filename in file_list:
        print filename
        name = os.path.split(filename)[1]
        year_number = int(name[2:6])
        output_name = os.path.join(OUTPATH4, name)
        print output_name
        MASKDATAPATH = MASKDATAPATH4 +"Prcp"+str(year_number)+".shp"
        extract(filename, output_name, MASKDATAPATH)


