# coding=utf-8
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




def task1():
    """
    提取各个公园的NDVI均值，有可能某个公园出错，需要到最后生成的excel文件里剔除其公园选项
    :return:
    """
    input_path = os.path.normcase("D:/NDVI Parks/CalNorth/NDVI CalNorth parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/NDVI result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    data_dict = dict()
    day_list = [209, 225, 241, 257, 273, 289]
    time_labels = [str(year) + '_' + str(day) for year in range(2000, 2014) for day in day_list]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list:
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        for input_file_name in time_labels:
            input_file = os.path.join(input_directory, input_file_name)
#            elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
#            elevSTD = elevSTDResult.getOutput(0)
            try:
                elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                elevSTD = elevSTDResult.getOutput(0)
            except:
                print input_file
                continue
            temp_mean_list.append(elevSTD)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "NDVI parks.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + time_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])










def task2():
    input_path = os.path.normcase("D:/NDVI Parks/New York/Ozone AOT NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/try")
    data_dict = dict()
    time_labels = [str(year) for year in range(2000, 2014)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        for input_file_name in time_labels:
            input_file = os.path.join(input_directory, input_file_name)
            try:
                elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                elevSTD = elevSTDResult.getOutput(0)
            except:
                elevSTD = "error"
            temp_mean_list.append(elevSTD)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "Ozone AOT NY parks.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + time_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

def task3():
    input_path = os.path.normcase("D:/NDVI Parks/New York/Ozone ave NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/try")
    data_dict = dict()
    time_labels = [str(year) for year in range(2000, 2014)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        for input_file_name in time_labels:
            input_file = os.path.join(input_directory, input_file_name)
            try:
                elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                elevSTD = elevSTDResult.getOutput(0)
            except:
                elevSTD = "error"
            temp_mean_list.append(elevSTD)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "Ozone ave NY parks.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + time_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])

def task4():
    input_path = os.path.normcase("D:/NDVI Parks/New York/Prcp NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/try")
    data_dict = dict()
    time_labels = [str(year) for year in range(2000, 2014)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        for input_file_name in time_labels:
            input_file = os.path.join(input_directory, input_file_name)
            try:
                elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                elevSTD = elevSTDResult.getOutput(0)
            except:
                elevSTD = "error"
            temp_mean_list.append(elevSTD)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "Prcp NY parks.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + time_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])


def task4():
    inraster_path = os.path.normcase("D:/NDVI Process/Climate layer/Temptotal")
    inmask_path = os.path.normcase("D:/NDVI Parks/CalNorth/CalNorth Parks")
    output_path = os.path.normcase("D:/NDVI Parks/CalNorth/near_temp")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    inraster_file_list = glob.glob((os.path.join(inraster_path, "*.shp")))
    inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))
    for inmask_file in inmask_file_list:
        inmask_file_name = os.path.split(inmask_file)[-1][:-4] # park name
        output_dir = os.path.join(output_path, inmask_file_name)
        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)
        for inraster_file in inraster_file_list:
            inraster_file_name = os.path.split(inraster_file)[-1]
            year_list = range(2000, 2014)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0]
            if len(inraster_file_year) == 0:
                continue
            inraster_file_year = inraster_file_year[0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)


def task5():
    input_path = os.path.normcase("D:/NDVI Parks/New York/Temptotal NY parks")
    output_path = os.path.normcase("D:/NDVI Parks/New York/try")
    data_dict = dict()
    time_labels = [str(year) for year in range(2000, 2014)]
    input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
    for input_directory in input_file_dir_list: # iteret every park
        input_directory_name = os.path.split(input_directory)[-1]    # park name
        temp_mean_list = list()
        temp_mean_list.append(input_directory_name)
        for input_file_name in time_labels:
            input_file = os.path.join(input_directory, input_file_name)
            try:
                elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                elevSTD = elevSTDResult.getOutput(0)
            except:
                elevSTD = "error"
            temp_mean_list.append(elevSTD)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "Temptotal NY parks.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + time_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])



if __name__ == "__main__":
    for index in range(1, 2):
        task_name = "task" + str(index)
        function = eval(task_name)
        function()










