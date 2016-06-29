import arcpy
from arcpy.sa import *


def extract_value_to_points(in_features, in_rasters, out_features):
    arcpy.CheckOutExtension("Spatial")
    ExtractValuesToPoints(in_features, in_rasters, out_features)


if __name__ == "__main__":
    pass
