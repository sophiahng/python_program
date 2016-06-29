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
    inmask_path = os.path.normcase("H:/data/intersect_rasters")
    inmask_file_list = glob.glob(os.path.join(inmask_path, "*.tif"))
    for mask_file in inmask_file_list:
        mask_file_name = os.path.split(mask_file)[-1]
        mask_file_day = mask_file_name[0:mask_file_name.find("_")]
        year_list = range(2000, 2015)
        for year in year_list:
            inraster_path = template.substitute({"year": year, "day": mask_file_day})
            if not os.path.exists(inraster_path):
                continue
            outExtractByMask=ExtractByMask(inraster_path, mask_file)
            output_path = os.path.normcase("H:/Data/ndvi extract intersect")
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            out_template = Template("US$year$day.250m_16_days_NDVI.tif")
            output_file = os.path.join(output_path, out_template.substitute({"year": year, "day": mask_file_day}))
            outExtractByMask.save(output_file)

