__author__ = 'Sophia'


import arcpy
import os
import glob
import csv
import math
import string
from arcpy.sa import *
arcpy.env.Workspace= "D:/Dian/process/"
arcpy.env.overwriteOutput = True

state_list = ["Arizona"]
#state_list = ["Arizona", "Maryland"]
#state_list = ["New York","Maryland","Pennsylvania","Northern California","Southern California","Texas"]

def phase_1():
    shp_file_list = [os.path.join("D:/Dian/United States/State", state + ".shp") for state in state_list]
    in_features = os.path.normcase("D:/Dian/United States/Parks (Local).lyr")
    out_put_dir = os.path.normcase("D:/NDVI")
    for shp_file in shp_file_list:
        shp_file_name = os.path.split(shp_file)[-1]
        state_name = shp_file_name[:-4]
        out_put_path = os.path.join(out_put_dir, state_name)
        if os.path.exists(out_put_path) is False:
            os.mkdir(out_put_path)
        out_put_path = os.path.join(out_put_path, "parks")
        if os.path.exists(out_put_path) is False:
            os.mkdir(out_put_path)
        temp_out_features = os.path.join(out_put_path, state_name + " ParksOr")
        if os.path.exists(temp_out_features + ".shp") is False:
            arcpy.Clip_analysis(in_features, shp_file, temp_out_features)
#            print("%s is produced" % temp_out_features)
        out_features = os.path.join(out_put_path, state_name + " Parks")
        if os.path.exists(out_features + ".shp") is False:
            try:
                arcpy.Select_analysis(temp_out_features + ".shp", out_features,  '"AREA" > 1')
            except:
                print("%s fails to be produced" %out_features)
                continue
            print("%s is produced" % out_features)

def extract_by_mask(inRaster, inMaskData, output_file):
    arcpy.CheckOutExtension("Spatial")
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(output_file)
    print("%s has been produced" % output_file)


def phase_2():
    inraster_path = os.path.normcase("H:/Data/ndvi extract intersect")
    inraster_file_list = glob.glob(os.path.join(inraster_path, "*.tif"))
    inmask_file_list = [os.path.normcase("D:/NDVI/" + state + "/parks/" + state + " Parks.shp") for state in state_list]
    for inmask_file in inmask_file_list:
        state = inmask_file.split("\\")[2]
        output_dir = os.path.normcase("D:/NDVI/" + state + "/ndvi parks total")
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            inraster_file_year = inraster_file_name[2:6]
            inraster_file_day = inraster_file_name[6:inraster_file_name.find(".")]
            output_file = os.path.join(output_dir, inraster_file_year + "_" + inraster_file_day)
            if os.path.exists(output_file):
                continue
            try:
                extract_by_mask(inraster_file, inmask_file, output_file)
            except:
                print output_file


def phase_3():
    input_path_list = [os.path.normcase("D:/NDVI/" + state + "/ndvi parks total") for state in state_list]
    day_list = [i*16 + 1 for i in range(23) if (i*16 + 1) <= 366]
    time_labels = [str(year) + '_' + str(day) for year in range(2000, 2015) for day in day_list]
    for input_parks_dir in input_path_list:
        state = input_parks_dir.split("\\")[2]
        output_path = "D:/NDVI/" + state + "/ndvi parks total result"
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        data_dict = dict()
        for input_file_name in time_labels:
            day = int(input_file_name[5:])
            if not data_dict.has_key(day):
                data_dict[day] = list()
                data_dict[day].append(day)
            temp_mean_list = data_dict[day]
            input_file = os.path.join(input_parks_dir, input_file_name)
            if not os.path.exists(input_file):
                temp_mean_list.append("NA")
                continue
            try:
                elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                elevSTD = elevSTDResult.getOutput(0)
            except:
                print input_file
                temp_mean_list.append("ERR")
                continue
            temp_mean_list.append(elevSTD)
        output_name = os.path.join(output_path, state + " ndvi parks.csv")

        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            first_row = [str(item) for item in range(2000, 2015)]
            output_writer.writerow([state,] + first_row + ["mean",])
            for key in sorted(data_dict.keys()):
                row_list = data_dict[key]
                sum = 0
                nums = len(row_list) - 1
                for i in range(1, len(row_list)):
                    if row_list[i] == "NA" or row_list[i] == "ERR":
                        nums -= 1
                        continue
                    sum += float(row_list[i])
                mean = sum/float(nums)
                row_list.append(str(mean))
                output_writer.writerow(data_dict[key])




if __name__ == "__main__":
    #phase_1()
    phase_2()
    phase_3()
