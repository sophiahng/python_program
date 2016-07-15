import arcpy
import os
from arcpy.sa import *

arcpy.CheckOutExtension('Spatial')


def extract_by_mask(in_raster, in_mask, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.mkdir(os.path.dirname(output_path))
    if os.path.exists(output_path):
        return
    print "processing extract by mask..."
    outExtractByMask = ExtractByMask(in_raster, in_mask)
    outExtractByMask.save(output_path)
    print("%s has been produced" % output_path)


if __name__ == "__main__":
    pass