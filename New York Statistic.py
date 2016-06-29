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
    该函数用来统计纽约州每一个公园的mean、值，然后将这些mean值存入到New York NDVI parks.csv文件去
    :return:
    """
    input_path = os.path.normcase("D:/NDVI/New York/parks/ndvi new york parks")
    output_path = os.path.normcase("D:/NDVI/New York/parks/New York ndvi result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    if os.path.exists(os.path.join(output_path, "New York NDVI parks.csv")): #若存在统计结果csv文件，则该函数不执行
        return
    data_dict = dict()
    day_list = [81, 97, 113, 129, 145, 161, 177, 193, 209, 225, 241]
    time_labels = [str(year) + '_' + str(day) for year in range(2000, 2015) for day in day_list]
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
    output_name = os.path.join(output_path, "New York NDVI parks.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + time_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])


def task2():
    inraster_path = os.path.normcase("D:/NDVI/Environment/Ozone aot junaug layer")
    inmask_path = os.path.normcase("D:/NDVI/New York/parks/new york parks")
    output_path = os.path.normcase("D:/NDVI/New York/parks/junaug near_aot")
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
            year_list = range(2000, 2015)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            if os.path.exists(output_file): #如果该输出文件已经存在，则跳过
                continue
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)


def task3():
    inraster_path = os.path.normcase("D:/NDVI/Environment/Ttotal junaug layer") #这儿有问题，此文件下没有文件
    inmask_path = os.path.normcase("D:/NDVI/New York/parks/new york parks")
    output_path = os.path.normcase("D:/NDVI/New York/parks/junaug near_temp")
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
            year_list = range(2000, 2015)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0]
            if len(inraster_file_year) == 0:
                continue
            inraster_file_year = inraster_file_year[0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            if os.path.exists(output_file): #如果该输出文件已经存在，则跳过
                continue
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)


def task4():
    inraster_path = os.path.normcase("D:/NDVI/Environment/Prcp layer")
    inmask_path = os.path.normcase("D:/NDVI/New York/parks/new york parks")
    output_path = os.path.normcase("D:/NDVI/New York/parks/near_prcp")
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
            year_list = range(2000, 2015)
            inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0]
            if len(inraster_file_year) == 0:
                continue
            inraster_file_year = inraster_file_year[0]
            output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
            if os.path.exists(output_file): #如果该输出文件已经存在，则跳过
                continue
            arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
            print("%s has been produced" % output_file)

def task5():
    input_path = os.path.normcase("D:/NDVI/New York/parks/junaug near_aot")
    output_path = os.path.normcase("D:/NDVI/New York/parks/get_near_result")
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
            arcpy.ExportXYv_stats(input_file, "mean", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                temp_mean_list.append(value)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "junaug near_aot.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])
def task6():
    input_path = os.path.normcase("D:/NDVI/New York/parks/near_prcp")
    output_path = os.path.normcase("D:/NDVI/New York/parks/get_near_result")
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
            arcpy.ExportXYv_stats(input_file, "junaug", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
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

def task7():
    input_path = os.path.normcase("D:/NDVI/New York/parks/junaug near_temp")
    output_path = os.path.normcase("D:/NDVI/New York/parks/get_near_result")
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
            arcpy.ExportXYv_stats(input_file, "junaug", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
            with open(temp_txt_file, "rb") as txt_rd:
                txt_rd.readline()
                value = txt_rd.readline().strip().split(" ")[2]
                temp_mean_list.append(value)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.join(output_path, "junaug near_temp.csv")
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + year_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])


if __name__ == "__main__":
    for index in range(7, 8):
        task_name = "task" + str(index)
        function = eval(task_name)
        function()

