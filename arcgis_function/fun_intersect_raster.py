import arcpy
import os
from arcpy.sa import *


def intersect_raster(in_raster_paths, out_raster_path, value):
    if not os.path.exists(os.path.dirname(out_raster_path)):
        os.mkdir(os.path.dirname(out_raster_path))
    arcpy.CheckOutExtension("Spatial")
    logic_raster_files = map(lambda a: Raster(a) == value, in_raster_paths)
    result = reduce(lambda a, b: a & b, logic_raster_files)
    result.save(out_raster_path)


if __name__ == "__main__":
    pass
