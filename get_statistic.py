__author__ = 'Philip'


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
    input_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_ave_maysep")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/get_near_result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    data_dict = dict()
    year_labels = [str(year) for year in range(2000, 2014)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        input_file_list = sorted(glob.glob(os.path.join(input_directory, "*.shp")))
        for input_file in input_file_list:
            temp_txt_file = os.path.join(output_path, "aidsbycacnty.txt")
            arcpy.ExportXYv_stats(input_file, "mean", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")
                value = value[2]
                temp_mean_list.append(value)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "near_ave_maysep.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

def task2():
    input_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_aot_maysep")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/get_near_result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    data_dict = dict()
    year_labels = [str(year) for year in range(2000, 2014)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        input_file_list = sorted(glob.glob(os.path.join(input_directory, "*.shp")))
        for input_file in input_file_list:
            temp_txt_file = os.path.join(output_path, "aidsbycacnty.txt")
            arcpy.ExportXYv_stats(input_file, "mean", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                temp_mean_list.append(value)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "near_aot_maysep.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

def task3():
    input_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_prcp")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/get_near_result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    data_dict = dict()
    year_labels = [str(year) for year in range(2000, 2014)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        input_file_list = sorted(glob.glob(os.path.join(input_directory, "*.shp")))
        for input_file in input_file_list:
            temp_txt_file = os.path.join(output_path, "aidsbycacnty.txt")
            arcpy.ExportXYv_stats(input_file, "maysep", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                temp_mean_list.append(value)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "near_prcp.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])




def task4():
    input_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_temp")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/get_near_result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    data_dict = dict()
    year_labels = [str(year) for year in range(2000, 2015)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        input_file_list = sorted(glob.glob(os.path.join(input_directory, "*.shp")))
        for input_file in input_file_list:
            temp_txt_file = os.path.join(output_path, "aidsbycacnty.txt")
            arcpy.ExportXYv_stats(input_file, "maysep", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                temp_mean_list.append(value)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "near_temp.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

if __name__ == "__main__":
    for index in range(1, 5):
        task_name = "task" + str(index)
        function = eval(task_name)
        function()

