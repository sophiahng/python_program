import arcpy
import os
from arcpy.sa import *


def extract(in_raster, out_raster, SQLClause):
    if not os.path.exists(os.path.dirname(out_raster)):
        os.mkdir(os.path.dirname(out_raster))
    arcpy.CheckOutExtension("Spatial")
    attExtract = ExtractByAttributes(in_raster, SQLClause)
    attExtract.save(out_raster)


if __name__ == "__main__":
    pass
