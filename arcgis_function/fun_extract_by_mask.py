import arcpy
import os
from arcpy.sa import *

arcpy.CheckOutExtension('Spatial')


def extract_by_mask(inRaster, inMaskData, out_subdir):
    if not os.path.exists(out_subdir):
        os.mkdir(out_subdir)
    output_file = os.path.join(out_subdir, os.path.basename(inRaster))
    if not os.path.exists(output_file):
        outExtractByMask = ExtractByMask(inRaster, inMaskData)
        outExtractByMask.save(output_file)
        print("%s has been produced" % output_file)


if __name__ == "__main__":
    pass