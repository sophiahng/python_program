# coding=utf-8
__author__ = 'Sophia'

"""
获得NDVI数据之后，接下来获取环境数据，将包含五个州的,接下来将结果统计出来
"""



import arcpy
import os
import glob
import csv
import math
import string
from arcpy.sa import *
arcpy.env.Workspace= "D:/Dian/process/"
arcpy.env.overwriteOutput = True


def task1(state, day_list, epochs):
    """
    该函数用来统计纽约州每一个公园的mean、值，然后将这些mean值存入到New York NDVI parks.csv文件去
    :return:
    """
    input_path = os.path.normcase("D:/NDVI/" + state + "/parks/ndvi " + state + " parks")
    output_path = os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    if os.path.exists(os.path.join(output_path, state + " ndvi parks.csv")): #若存在统计结果csv文件，则该函数不执行
        return
    data_dict = dict()
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
            if not os.path.exists(input_file):
                elevSTD = "NA"
                temp_mean_list.append(elevSTD)
                continue
            try:
                elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                elevSTD = elevSTDResult.getOutput(0)
            except:
                print input_file
                elevSTD="ERROR"
            temp_mean_list.append(elevSTD)
        data_dict[input_directory_name] = temp_mean_list
    output_name = os.path.normcase(os.path.join(output_path, state + " ndvi parks.csv"))
    with file(output_name, "wb") as output_fd:
        output_writer = csv.writer(output_fd)
        output_writer.writerow([' '] + time_labels)
        for key in sorted(data_dict.keys()):
            output_writer.writerow(data_dict[key])


def task2(state, day_list, epochs):
    for epoch in epochs:
        inraster_path = os.path.normcase("D:/NDVI/Environment/Ozone aot " + epoch + " layer")
        inmask_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + state + " parks")
        output_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + epoch + " near_aot")
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


def task3(state, day_list, epochs):
    for epoch in epochs:
        inraster_path = os.path.normcase("D:/NDVI/Environment/Ttotal " + epoch + " layer")
        inmask_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + state + " parks")
        output_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + epoch + " near_temp")
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


def task4(state, day_list, epochs):
    inraster_path = os.path.normcase("D:/NDVI/Environment/Prcp layer")
    inmask_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + state + " parks")
    output_path = os.path.normcase("D:/NDVI/" + state + "/parks/near_prcp")
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

def task5(state, day_list, epochs):
    for epoch in epochs:
        input_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + epoch + " near_aot")
        output_path = os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result")
        if os.path.exists(output_path) is False:
            os.mkdir(output_path)
        output_name = os.path.join(output_path, epoch + " near_aot.csv")
        if os.path.exists(output_name):
            continue
        data_dict = dict()
        year_labels = [str(year) for year in range(2000, 2015)]
        input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
        for input_directory in input_file_dir_list: # iteret every park
            input_directory_name = os.path.split(input_directory)[-1]    # park name
            temp_mean_list = list()
            temp_mean_list.append(input_directory_name)
            input_file_list = sorted(glob.glob(os.path.join(input_directory, "*.shp")))
            year = 2000
            for input_file in input_file_list:
                print("task5 is processing %s of %s" %(input_file,epoch))
                input_file_year = input_file[-8:-4]
                while year < int(input_file_year):
                    temp_mean_list.append("NA")
                    year += 1
                temp_txt_file = os.path.join(output_path, "aidsbycacnty.txt")
                try:
                    arcpy.ExportXYv_stats(input_file, "mean", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
                    with open(temp_txt_file, "rb") as txt_rd:
                        txt_rd.readline()
                        value = txt_rd.readline().strip().split(" ")[2]
                        temp_mean_list.append(value)
                except:
                    temp_mean_list.append("ERROR")
                year += 1
            data_dict[input_directory_name] = temp_mean_list
        output_name = os.path.join(output_path, epoch + " near_aot.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])


def task6(state, day_list, epochs):
    input_path = os.path.normcase("D:/NDVI/" + state + "/parks/near_prcp")
    output_path = os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result")
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    for epoch in epochs:
        output_name = os.path.join(output_path, epoch + " near_prcp.csv")
        if os.path.exists(output_name):
            continue
        data_dict = dict()
        year_labels = [str(year) for year in range(2000, 2015)]
        input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
        for input_directory in input_file_dir_list: # iteret every park
            input_directory_name = os.path.split(input_directory)[-1]    # park name
            temp_mean_list = list()
            temp_mean_list.append(input_directory_name)
            input_file_list = sorted(glob.glob(os.path.join(input_directory, "*.shp")))
            year = 2000
            for input_file in input_file_list:
                print("task6 is processing %s of %s" %(input_file,epoch))
                input_file_year = input_file[-8:-4]
                while year < int(input_file_year):
                    temp_mean_list.append("NA")
                    year += 1
                year += 1
                temp_txt_file = os.path.join(output_path, "aidsbycacnty.txt")
                try:
                    arcpy.ExportXYv_stats(input_file, epoch, "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
                    with open(temp_txt_file, "rb") as txt_rd:
                        txt_rd.readline()
                        value = txt_rd.readline().strip().split(" ")[2]
                        temp_mean_list.append(value)
                except:
                    temp_mean_list.append("ERROR")
            data_dict[input_directory_name] = temp_mean_list
        output_name = os.path.join(output_path, epoch + " near_prcp.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

def task7(state, day_list, epochs):
    for epoch in epochs:
        input_path = os.path.normcase("D:/NDVI/" + state + "/parks/" + epoch + " near_temp")
        output_path = os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result")
        if os.path.exists(output_path) is False:
            os.mkdir(output_path)
        output_name = os.path.join(output_path, epoch + " near_temp.csv")
        if os.path.exists(output_name):
            continue
        data_dict = dict()
        year_labels = [str(year) for year in range(2000, 2015)]
        input_file_dir_list = [os.path.join(input_path, directory) for directory in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, directory))]
        for input_directory in input_file_dir_list: # iteret every park
            input_directory_name = os.path.split(input_directory)[-1]    # park name
            temp_mean_list = list()
            temp_mean_list.append(input_directory_name)
            input_file_list = sorted(glob.glob(os.path.join(input_directory, "*.shp")))
            year = 2000
            for input_file in input_file_list:
                print("task7 is processing %s of %s" %(input_file,epoch))
                input_file_year = input_file[-8:-4]
                while year < int(input_file_year):
                    temp_mean_list.append("NA")
                    year += 1
                year += 1
                temp_txt_file = os.path.join(output_path, "aidsbycacnty.txt")
                try:
                    arcpy.ExportXYv_stats(input_file, epoch, "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
                    with open(temp_txt_file, "rb") as txt_rd:
                        txt_rd.readline()
                        value = txt_rd.readline().strip().split(" ")[2]
                        temp_mean_list.append(value)
                except:
                    temp_mean_list.append("ERROR")
            data_dict[input_directory_name] = temp_mean_list
        output_name = os.path.join(output_path, epoch + " near_temp.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])


def task8(state, day_list, epochs):
    input_path = os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result")
    output_path = os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result")
    input_file_list = glob.glob(os.path.join(input_path, "*.csv"))
    data_dict = dict()
    output_file_name = "total_result.csv"
    output_file = os.path.join(output_path, output_file_name)
    if os.path.exists(output_file):
        return
    for input_file in input_file_list:
        with file(input_file, "rb") as file_rd:
            local_data_list = list()
            csv_reader = csv.reader(file_rd)
            for row in csv_reader:
                local_data_list.append(row)
            data_dict[input_file] = local_data_list

    year_list = range(2000, 2015)
    data_dict_by_year = dict()
    ndvi_csv = os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result/" + state + " ndvi parks.csv")
    park_list = [row[0] for row in data_dict[ndvi_csv] if row[0] != " "]

    for year in year_list:
        local_year_data_list = list()
        temp_data_list = list()
        aot_data_list = list()
        prcp_data_list = list()
        for epoch in epochs:
            temp_data_list.append(data_dict[os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result/" + epoch + " near_temp.csv")])
            aot_data_list.append(data_dict[os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result/" + epoch + " near_aot.csv")])
            prcp_data_list.append(data_dict[os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result/" + epoch + " near_prcp.csv")])
        ndvi_data_list = data_dict[os.path.normcase("D:/NDVI/" + state + "/parks/get_near_result/" + state + " ndvi parks.csv")]
        local_data_list_list = temp_data_list + aot_data_list + prcp_data_list + [ndvi_data_list, ]
        for index, park in enumerate(park_list, start=1):
            local_park_data_list = list()
            local_park_data_list.append(str(index))
            local_park_data_list.append(park)
            local_park_data_list.append(str(year))
            for index, data_list in enumerate(local_data_list_list):
                if index != 3 * len(epochs):
                    for row in data_list:
                        if row[0] == " " or row[0] != park:
                            continue
                        else:
                            local_park_data_list.append(row[year_list.index(year) + 1])
                            break
                else:
                    for row in data_list:
                        if row[0] == " " or row[0] != park:
                            continue
                        else:
                            start_index = year_list.index(year) * len(day_list) + 1
                            for i in range(len(day_list)):
                                try:
                                    local_park_data_list.append(row[start_index + i])
                                except:
                                    print year
                                    print park
                            break
            local_year_data_list.append(local_park_data_list)
        data_dict_by_year[year] = local_year_data_list

    output_file_name = state + " total_result.csv"
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    output_file = os.path.join(output_path, output_file_name)
    with file(output_file, "wb") as file_wd:
        csv_writer = csv.writer(file_wd)
        labels = [" ", "Parks", "Year"]
        for item in ["Temp", "Ozoneaot", "Prcp"]:
            for epoch in epochs:
                labels += [item + "_" + epoch, ]
        for day in day_list:
            labels += ["NDVI_" + str(day), ]
        csv_writer.writerow(labels)
        for year in year_list:
            year_data_list = data_dict_by_year[year]
            for data_list in year_data_list:
                csv_writer.writerow(data_list)




def task(state, day_list, epochs):
    print("task1 is running")
    task1(state, day_list, epochs)
    print("task2 is running")
    task2(state, day_list, epochs)
    print("task3 is running")
    task3(state, day_list, epochs)
    print("task4 is running")
    task4(state, day_list, epochs)
    print("task5 is running")
    task5(state, day_list, epochs)
    print("task6 is running")
    task6(state, day_list, epochs)
    print("task7 is running")
    task7(state, day_list, epochs)
    print("task8 is running")
    task8(state, day_list, epochs)






if __name__ == "__main__":
    state_list = ["Arizona"]
    #state_list = ["Texas", "New York", "Illinois","Arizona","Northern California","Maryland","Southern California","Pennsylvania"]
    #state_list = ["New York","Pennsylvania","Maryland"]
    state_day_list = [range(1, 366, 16)]
    #state_day_list = [range(1, 366, 16), range(1, 366, 16), range(1, 366, 16), range(1, 366, 16), range(1, 366,16),range(1, 366,16),range(1, 366,16),range(1,366,16)]
    epoch_list = ["marmay", "junaug","sepnov","decfeb"]
    epoch_list_list = []
    for i in range(len(state_list)):
        epoch_list_list.append(epoch_list)
    for index, value in enumerate(state_list):
        state = value
        task(state, state_day_list[index], epoch_list_list[index])

