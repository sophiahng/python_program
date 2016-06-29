import arcpy
from arcpy.sa import *


def extract_value_to_points(in_features, in_rasters):
    arcpy.CheckOutExtension("Spatial")
    ExtractValuesToPoints(in_features, in_rasters)


if __name__ == "__main__":
    pass
