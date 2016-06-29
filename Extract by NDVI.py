import os
import arcpy
from arcpy import env
from arcpy.sa import *
import glob
import shutil

env.workspace = "D:/phython environment/"

OUTPATH = os.path.normcase("H:/Data/NDVI over 5000")
FILEPATH = os.path.normcase("H:/Data/NDVI")

def extract(input,output,inSQLClause):
    inRaster=input
    inSQLClause= "value>=5000"
    arcpy.CheckOutExtension("Spatial")
    attExtract = ExtractByAttributes(inRaster, inSQLClause)
    attExtract.save(output)

if __name__ == '__main__':
    if os.path.exists(OUTPATH) is False:
        os.mkdir(OUTPATH)
    if os.path.exists(FILEPATH) is False:
        print("FILEPATH is not existed")
    else:
        path = FILEPATH
        print(path)
        if os.path.exists(path) is False:
            print 'not existed'
        else:
            file_list = glob.glob(os.path.join(path, '*.tif'))
            for filename in file_list:
                print filename
                name = os.path.split(filename)[1]
                output_name = os.path.join(OUTPATH, name)
                print output_name
                inSQLClause = None
                extract(filename, output_name, inSQLClause)

