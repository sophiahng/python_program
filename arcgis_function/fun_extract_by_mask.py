import arcpy
import os
from arcpy.sa import *

arcpy.CheckOutExtension('Spatial')


def extract_by_mask(inRaster, inMaskData, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.mkdir(os.path.dirname(output_file))
    if os.path.exists(output_file):
        return
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(output_file)
    print("%s has been produced" % output_file)


if __name__ == "__main__":
    pass