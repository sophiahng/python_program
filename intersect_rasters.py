__author__ = 'Sophia'

import arcpy
import os
import glob
import csv
import math
import string
from string import Template
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.Workspace= "D:/Dian/process/"
arcpy.env.overwriteOutput = True



if __name__ == "__main__":
    template = Template("H:/Data/ndvi over 5000/US$year$day.250m_16_days_NDVI.tif")
    day_list = [i*16 + 1 for i in range(23) if (i*16 + 1) <= 366]
    for day in day_list:
        inraster_path_list = [template.substitute({"year": year, "day": day}) for year in range(2000, 2015) if os.path.exists(template.substitute({"year": year, "day": day}))]
        outFzyOverlay = FuzzyOverlay(inraster_path_list, "AND")
        out_path = os.path.normcase("H:/data/intersect_rasters")
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        out_put = os.path.join(out_path, str(day) + "_intersect.tif")
        outFzyOverlay.save(out_put)
        print("%s is produced"%day)
