__author__ = 'Sophia'



import os
import glob

import arcpy
from arcpy import env
from arcpy.sa import *

env.Workspace= "D:/NDVI Process/Environment/"


if __name__ == "__main__":
    ndvi_intersect_1_path = os.path.normcase("D:/NDVI Process/intersect/MaySep/3K/20002006")
    ndvi_intersect_2_path = os.path.normcase("D:/NDVI Process/intersect/MaySep/3K/20072013")
    ozone_aot_path = os.path.normcase("D:/NDVI Process/Ozone Buffer/AOT40/Ozone 3km/MaySep")
    ozone_avg_path = os.path.normcase("D:/NDVI Process/Ozone Buffer/Average/Ozone 3km/MaySep")
    climate_prcp_path = os.path.normcase("D:/NDVI Process/Climate Buffer/Climate 5km/Prcp buffer")
    climate_tavg_path = os.path.normcase("D:/NDVI Process/Climate Buffer/T total 3km MaySep")#
    result_path = os.path.normcase("D:/NDVI Process/Result")

    ndvi_file_1_list = glob.glob(os.path.join(ndvi_intersect_1_path, "*.shp"))
    ndvi_file_2_list = glob.glob(os.path.join(ndvi_intersect_2_path, "*.shp"))
    ozone_aot_file_list = glob.glob(os.path.join(ozone_aot_path, "*shp"))
    ozone_avg_file_list = glob.glob(os.path.join(ozone_avg_path, "*.shp"))
    climate_prcp_file_list = glob.glob(os.path.join(climate_prcp_path, "*.shp"))
    climate_tavg_file_list = glob.glob(os.path.join(climate_tavg_path, "*.shp"))
    all_file_list = [ozone_aot_file_list, ozone_avg_file_list, climate_prcp_file_list, climate_tavg_file_list]

    year_1_list = range(2000, 2007)
    year_2_list =range(2007, 2014)
    for year in range(2000, 2014):
        out_path = os.path.join(result_path, str(year))
        if os.path.exists(out_path) is not True:
            os.mkdir(out_path)
        if year in year_1_list:
            ndvi_file_list = ndvi_file_1_list
        else:
            ndvi_file_list = ndvi_file_2_list
        for ndvi_file in ndvi_file_list:
            ndvi_file_name = os.path.split(ndvi_file)[-1]
            day = int(ndvi_file_name[ndvi_file_name.find(".")-3:ndvi_file_name.find(".")])
            input_features_list = []
            input_features_list.append(ndvi_file)
            for file_list in all_file_list:
                if file_list == climate_tavg_file_list:
                    for year_file in file_list:
                        temp_year = int(os.path.split(year_file)[-1][0:4])
                        if year == temp_year:
                            shp_file = [year_file, ]
                            break
                else:
                    shp_file = [year_file for year_file in file_list if int(year_file[year_file.find(".")-4:year_file.find(".")]) == year]
                if len(shp_file) == 0:
                    print("there has no shp file in that year %s" %year)
                    continue
                shp_file = shp_file[0]
                input_features_list.append(shp_file)
            out_file = str(year) + '_' + str(day) + ".shp"
            out_file = os.path.join(out_path, out_file)
            arcpy.Intersect_analysis(input_features_list, out_file)
    print "hell"

