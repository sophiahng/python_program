
import arcpy
import os
import glob
import csv
import math
import string
from arcpy.sa import *

arcpy.env.Workspace= "D:/Dian/process/"
arcpy.env.overwriteOutput = True




def task1():
    inraster_path = os.path.normcase("D:/NDVI Process/Ozone layer/Average/MaySep")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_dis_ave_maysep")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    year_labels = [str(year) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    data_dict = dict()
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        local_dist_list = list()
        local_dist_list.append(inmask_file_name)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            arcpy.Near_analysis(inmask_file, inraster_file)
            temp_txt_file = os.path.join(output_path, "dist.txt")
            arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                local_dist_list.append(value)
        data_dict[inmask_file_name] = local_dist_list

    output_file_name = "near_distance.csv"
    output_file = os.path.join(output_path, output_file_name)
    with file(output_file, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])






def task2():
    inraster_path = os.path.normcase("D:/NDVI Process/Ozone layer/AOT40/MaySep")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_dis_aot_maysep")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    year_labels = [str(year) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    data_dict = dict()
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        local_dist_list = list()
        local_dist_list.append(inmask_file_name)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            arcpy.Near_analysis(inmask_file, inraster_file)
            temp_txt_file = os.path.join(output_path, "dist.txt")
            arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                local_dist_list.append(value)
        data_dict[inmask_file_name] = local_dist_list

    output_file_name = "near_distance.csv"
    output_file = os.path.join(output_path, output_file_name)
    with file(output_file, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

def task3():
    inraster_path = os.path.normcase("D:/NDVI Process/Climate layer/Prcp")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_dis_prcp_maysep")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    year_labels = [str(year) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    data_dict = dict()
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        local_dist_list = list()
        local_dist_list.append(inmask_file_name)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            arcpy.Near_analysis(inmask_file, inraster_file)
            temp_txt_file = os.path.join(output_path, "dist.txt")
            arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                local_dist_list.append(value)
        data_dict[inmask_file_name] = local_dist_list

    output_file_name = "prcp_near_distance.csv"
    output_file = os.path.join(output_path, output_file_name)
    with file(output_file, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

def task4():
    inraster_path = os.path.normcase("D:/NDVI Process/Climate layer/Temptotal")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_dis_temp_maysep")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    year_labels = [str(year) for year in range(2000, 2014)]
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    data_dict = dict()
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        local_dist_list = list()
        local_dist_list.append(inmask_file_name)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            arcpy.Near_analysis(inmask_file, inraster_file)
            temp_txt_file = os.path.join(output_path, "dist.txt")
            arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                local_dist_list.append(value)
        data_dict[inmask_file_name] = local_dist_list

    output_file_name = "near_distance.csv"
    output_file = os.path.join(output_path, output_file_name)
    with file(output_file, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

if __name__ == "__main__":
    for index in range(1, 5):
        task_name = "task" + str(index)
        function = eval(task_name)
        function()
