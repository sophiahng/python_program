import os
import arcpy
from arcpy import env
env.overwriteOutput = True
from arcpy.sa import *
import glob

dest_subdir = os.path.normcase("G:/EVI extract")
data_subdir = os.path.normcase('G:/EVI')
mask_data_path = os.path.normcase("D:/Dian/Data/United States 2000/background/" + "newstates" + ".shp")

arcpy.CheckOutExtension("Spatial")


def extract(tif_file_path, dest_file_path, mask_data_path):
    print('Extracting %s' % tif_file_path)
    outExtractByMask = ExtractByMask(tif_file_path, mask_data_path)
    outExtractByMask.save(dest_file_path)


if __name__ == '__main__':
    if not os.path.exists(dest_subdir):
        os.mkdir(dest_subdir)
    if not os.path.exists(mask_data_path):
        print("mask_data_path is not existed")
    tif_file_paths = glob.glob(os.path.join(data_subdir, '*.tif'))
    for tif_file_path in tif_file_paths:
        # print filename
        tif_file_name = os.path.split(tif_file_path)[1]
        dest_file_path = os.path.join(dest_subdir, tif_file_name)
        # print output_name
        if os.path.exists(dest_file_path):
            continue
        extract(tif_file_path, dest_file_path, mask_data_path)












