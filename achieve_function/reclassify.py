# -*- coding: UTF-8 -*-
# File: reclassify
# Time: 7/18/2016 -> 12:16 PM

import os
import csv
from collections import Counter
import arcpy
from arcpy import env
from arcpy.sa import Reclassify, ExtractByMask, CellStatistics, RemapRange, Int, RemapValue
from arcpy.sa import *

arcpy.CheckOutExtension('Spatial')
arcpy.CheckInExtension('Spatial')

env.workspace = "G:/yang/ozone_process/night_images/"

remap = RemapRange([[0, 10, 1], [10, 20, 2], [20, 30, 3], [30, 40, 4], [40, 50, 5],
                    [50, 100, 6], [100, 200, 7], [200, 300, 8], [300, 400, 9], [400, 500, 10],
                    [500, 600, 11]])

out_raster = Reclassify(os.path.join(env.workspace,"night_mean.tif"), "value", remap, "NODATA")
out_raster.save("night_mean_classify.tif")

