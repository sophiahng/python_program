# coding=utf-8
__author__ = 'Philip'

import os
import arcpy
from arcpy import env
from arcpy.sa import *
import glob

OUTPATH = os.path.normcase("D:/NDVI Process/MaySep/3K/over 4000/")
FILEPATH = os.path.normcase("D:/NDVI Process/MaySep/3K/Extract NDVI by mask4/")
env.Workspace= "D:/NDVI Extract/Workspace"

def extract(input_file, output_file):
    inRaster = input_file
    inSQLClause= "VALUE >=4000"
    arcpy.CheckOutExtension("Spatial")
    attExtract = ExtractByAttributes(inRaster, inSQLClause)
    attExtract.save(output_file)

if __name__ == '__main__':
    if os.path.exists(OUTPATH) is False:
        os.mkdir(OUTPATH)
    if os.path.exists(FILEPATH) is False:
        print("FILEPATH is not existed")
    else:
        path = FILEPATH
        file_list = glob.glob(os.path.join(path, '*.tif'))
        for filename in file_list:
            print filename
            name_without_path = os.path.split(filename)[1]
            output_name = os.path.join(OUTPATH, name_without_path)
            print output_name
            extract(filename, output_name)

