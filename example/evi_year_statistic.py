# -*- coding: UTF-8 -*-
# File: evi_year_statistic
# Time: 7/15/2016 -> 9:56 PM
import os
import arcpy
import glob
from arcpy import env
from arcpy.sa import CellStatistics

env.workspace = os.path.normcase("G:\yang\evi_year_statistic")
arcpy.CheckOutExtension('Spatial')

EVI_RASTER_SUBDIR = os.path.normcase("G:\evi_extract")
YEARS = range(2000, 2015)


def evi_year_maximum_stat():
    years = YEARS
    for year in years:
        evi_raster_paths = glob.glob(os.path.join(EVI_RASTER_SUBDIR,
                                                  "US{}*.250m_16_days_EVI.tif".format(str(year))))
        output_raster_path = "evi_{}_maximum_stat.tif".format(str(year))
        if os.path.exists(os.path.join(env.workspace, output_raster_path)):
            print("{} has been created before".format(output_raster_path))
            continue
        print("CellStatistics is working for {}".format(str(year)))
        evi_year_stat = CellStatistics(evi_raster_paths, "MAXIMUM", "NODATA")
        evi_year_stat.save(output_raster_path)


def evi_year_mean_stat():
    years = YEARS
    for year in years:
        evi_raster_paths = glob.glob(os.path.join(EVI_RASTER_SUBDIR,
                                                    "US{}*.250m_16_days_EVI.tif".format(str(year))))
        output_raster_path = "evi_{}_mean_stat.tif".format(str(year))
        if os.path.exists(os.path.join(env.workspace, output_raster_path)):
            print("{} has been created before".format(output_raster_path))
            continue
        print("CellStatistics is working for {}".format(str(year)))
        evi_year_stat = CellStatistics(evi_raster_paths, "MAXIMUM", "NODATA")
        evi_year_stat.save(output_raster_path)


if __name__ == "__main__":
    evi_year_maximum_stat()
    evi_year_mean_stat()








