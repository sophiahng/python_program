# coding=utf-8
__author__ = 'Sophia'
"""
这个程序是对所有的州进行批处理统计分析
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

class State_analysis(object):
    """

    """
    def __init__(self, state):
        """
        :param state: 参数是州所在的目录位置
        :return:
        """
        self.state_path = os.path.normcase(state)
        self.state_name = os.path.split(state)[-1]
        self.ndvi_inraster_path = os.path.normcase("D:/Environment Factors/NDVI Extract")

    def create_parks(self):
        """
        创建该州的各个parks的shp文件
        :return:
        """
        in_features = os.path.normcase(os.path.join(self.state_path, self.state_name + " Parks.shp"))
        split_features = in_features
        split_field = "NAME"
        out_workspace = os.path.normcase(os.path.join(self.state_path, self.state_name + " Parks"))
        if os.path.exists(out_workspace) is False:
            os.mkdir(out_workspace)
        try:
            arcpy.Split_analysis (in_features, split_features, split_field, out_workspace)
        except:
            print("there are some errors in %s during create parks process" % self.state_name)

    @staticmethod
    def extract_by_mask(inRaster, inMaskData, output_file):
        arcpy.CheckOutExtension("Spatial")
        outExtractByMask = ExtractByMask(inRaster, inMaskData)
        outExtractByMask.save(output_file)
        print("%s has been produced" % output_file)

    def ndvi_mask(self):
        """
        创基该州的ndvi统计数据
        :return:
        """
        inraster_path = self.ndvi_inraster_path
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "ndvi " + self.state_name + " parks"))
        if os.path.exists(output_path) is False:
            os.mkdir(output_path)
        inraster_file_list = glob.glob(os.path.join(inraster_path, "*.tif"))
        inmask_file_list = glob.glob((os.path.join(inmask_path, "*.shp")))

        for inmask_file in inmask_file_list:
            inmask_file_name = os.path.split(inmask_file)[-1][:-4]
            output_dir = os.path.join(output_path, inmask_file_name)
            if os.path.exists(output_dir) is False:
                os.mkdir(output_dir)
            for inraster_file in inraster_file_list:
                inraster_file_name = os.path.split(inraster_file)[-1]
                year_list = range(2000, 2014)
                day_list = [209, 225, 241, 257, 273, 289]
                inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
                inraster_file_day = [day for day in day_list if inraster_file_name.find(str(day)) == 6][0]
                output_file = os.path.join(output_dir, str(inraster_file_year) + "_" + str(inraster_file_day))
                if os.path.exists(output_file):
                    continue
                try:
                    self.extract_by_mask(inraster_file, inmask_file, output_file)
                except:
                    print("%s fails to produce during ndvi_analysis process" %output_file)

    def ndvi_xml(self):
        input_path = os.path.normcase(os.path.join(self.state_path, "ndvi " + self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "ndvi results"))
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
                try:
                    elevSTDResult = arcpy.GetRasterProperties_management(input_file, "MEAN")
                    elevSTD = elevSTDResult.getOutput(0)
                except:
                    print("%s has no MEAN value" %input_file)
                    temp_mean_list = list()
                    break
                temp_mean_list.append(elevSTD)
            if temp_mean_list:
                data_dict[input_directory_name] = temp_mean_list
        output_name = os.path.join(output_path, "ndvi parks.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + time_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

    def get_near_task1(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Ozone ave layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_ave_aprsep"))
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
                inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
                output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
                try:
                    arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
                except:
                    os.rmdir(output_dir)
                    print("%s fails" %output_file)
                    break
                print("%s has been produced" % output_file)

    def get_near_task2(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Ozone aot layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_aot_aprsep"))
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
                inraster_file_year = [year for year in year_list if inraster_file_name.find(str(year)) >= 0][0]
                output_file = os.path.join(output_dir, "near_" + str(inraster_file_year) + ".shp")
                try:
                    arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
                except:
                    os.rmdir(output_dir)
                    print("%s fails" %output_file)
                    break
                print("%s has been produced" % output_file)

    def get_near_task3(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Prcp layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_prcp_aprsep"))
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
                try:
                    arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
                except:
                    os.rmdir(output_dir)
                    print("%s fails" %output_file)
                    break
                print("%s has been produced" % output_file)

    def get_near_task4(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Ttotal layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_temp_aprsep"))
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
                try:
                    arcpy.SpatialJoin_analysis(inmask_file, inraster_file, output_file,"#","#","#","CLOSEST")
                except:
                    os.rmdir(output_dir)
                    print("%s fails" %output_file)
                    break
                print("%s has been produced" % output_file)

    def get_near_distance_task1(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Ozone ave layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_dis_ave_aprsep"))
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
                try:
                    arcpy.Near_analysis(inmask_file, inraster_file)
                except:
                    local_dist_list = list()
                    break
                temp_txt_file = os.path.join(output_path, "dist.txt")
                arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
                with open(temp_txt_file, "rb") as txt_rd:
                    txt_rd.readline()
                    value = txt_rd.readline().strip().split(" ")[2]
                    local_dist_list.append(value)
            if local_dist_list:
                data_dict[inmask_file_name] = local_dist_list
        output_file_name = "near_distance.csv"
        output_file = os.path.join(output_path, output_file_name)
        with file(output_file, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])



    def get_near_distance_task2(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Ozone aot layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_dis_aot_aprsep"))
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
                try:
                    arcpy.Near_analysis(inmask_file, inraster_file)
                except:
                    local_dist_list = list()
                    break
                temp_txt_file = os.path.join(output_path, "dist.txt")
                arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
                with open(temp_txt_file, "rb") as txt_rd:
                    txt_rd.readline()
                    value = txt_rd.readline().strip().split(" ")[2]
                    local_dist_list.append(value)
            if local_dist_list:
                data_dict[inmask_file_name] = local_dist_list
        output_file_name = "near_distance.csv"
        output_file = os.path.join(output_path, output_file_name)
        with file(output_file, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

    def get_near_distance_task3(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Prcp layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_dis_prcp_aprsep"))
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
                try:
                    arcpy.Near_analysis(inmask_file, inraster_file)
                except:
                    local_dist_list = list()
                    break
                temp_txt_file = os.path.join(output_path, "dist.txt")
                arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
                with open(temp_txt_file, "rb") as txt_rd:
                    txt_rd.readline()
                    value = txt_rd.readline().strip().split(" ")[2]
                    local_dist_list.append(value)
            if local_dist_list:
                data_dict[inmask_file_name] = local_dist_list
        output_file_name = "prcp_near_distance.csv"
        output_file = os.path.join(output_path, output_file_name)
        with file(output_file, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

    def get_near_distance_task4(self):
        inraster_path = os.path.normcase("D:/Environment Factors/Ttotal layer")
        inmask_path = os.path.normcase(os.path.join(self.state_path, self.state_name + " parks"))
        output_path = os.path.normcase(os.path.join(self.state_path, "near_dis_temp_aprsep"))
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
                try:
                    arcpy.Near_analysis(inmask_file, inraster_file)
                except:
                    local_dist_list = list()
                    break
                temp_txt_file = os.path.join(output_path, "dist.txt")
                arcpy.ExportXYv_stats(inmask_file, "NEAR_DIST", "space", temp_txt_file, "ADD_FIELD_NAMES")
                with open(temp_txt_file, "rb") as txt_rd:
                    txt_rd.readline()
                    value = txt_rd.readline().strip().split(" ")[2]
                    local_dist_list.append(value)
            if local_dist_list:
                data_dict[inmask_file_name] = local_dist_list
        output_file_name = "near_distance.csv"
        output_file = os.path.join(output_path, output_file_name)
        with file(output_file, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])


    def get_statistic_task1(self):
        input_path = os.path.normcase(os.path.join(self.state_path, "near_ave_aprsep"))
        output_path = os.path.normcase(os.path.join(self.state_path, "get_near_result"))
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
        output_name = os.path.join(output_path, "near_ave_aprsep.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

    def get_statistic_task2(self):
        input_path = os.path.normcase(os.path.join(self.state_path, "near_aot_aprsep"))
        output_path = os.path.normcase(os.path.join(self.state_path, "get_near_result"))
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
        output_name = os.path.join(output_path, "near_aot_aprsep.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

    def get_statistic_task3(self):
        input_path = os.path.normcase(os.path.join(self.state_path, "near_prcp_aprsep"))
        output_path = os.path.normcase(os.path.join(self.state_path, "get_near_result"))
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
                arcpy.ExportXYv_stats(input_file, "aprsep", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
                with open(temp_txt_file, "rb") as txt_rd:
                    txt_rd.readline()
                    value = txt_rd.readline().strip().split(" ")[2]
                    temp_mean_list.append(value)
            data_dict[input_directory_name] = temp_mean_list
        output_name = os.path.join(output_path, "near_prcp_aprsep.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

    def get_statistic_task4(self):
        input_path = os.path.normcase(os.path.join(self.state_path, "near_temp_aprsep"))
        output_path = os.path.normcase(os.path.join(self.state_path, "get_near_result"))
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
                arcpy.ExportXYv_stats(input_file, "aprsep", "SPACE", temp_txt_file, "ADD_FIELD_NAMES")
                with open(temp_txt_file, "rb") as txt_rd:
                    txt_rd.readline()
                    value = txt_rd.readline().strip().split(" ")[2]
                    temp_mean_list.append(value)
            data_dict[input_directory_name] = temp_mean_list
        output_name = os.path.join(output_path, "near_temp_aprsep.csv")
        with file(output_name, "wb") as output_fd:
            output_writer = csv.writer(output_fd)
            output_writer.writerow([' '] + year_labels)
            for key in sorted(data_dict.keys()):
                output_writer.writerow(data_dict[key])

    def get_result(self):
        input_path = os.path.normcase(os.path.join(self.state_path, "get_near_result"))
        output_path = os.path.normcase(os.path.join(self.state_path, "statistic_result"))
        input_file_list = glob.glob(os.path.join(input_path, "*.csv"))
        data_dict = dict()
        input_path = os.path.normcase(os.path.join(self.state_path, "ndvi results"))
        input_file_list.extend(glob.glob(os.path.join(input_path, "*.csv")))
        input_file_list.extend(glob.glob(os.path.normcase(os.path.join(self.state_path, "near_dis_aot_aprsep/*.csv"))))
        input_file_list.extend(glob.glob(os.path.normcase(os.path.join(self.state_path, "near_dis_ave_aprsep/*.csv"))))
        input_file_list.extend(glob.glob(os.path.normcase(os.path.join(self.state_path, "near_dis_prcp_aprsep/*.csv"))))
        input_file_list.extend(glob.glob(os.path.normcase(os.path.join(self.state_path, "near_dis_temp_aprsep/*.csv"))))
        for input_file in input_file_list:
            with file(input_file, "rb") as file_rd:
                local_data_list = list()
                csv_reader = csv.reader(file_rd)
                for row in csv_reader:
                    local_data_list.append(row)
                data_dict[input_file] = local_data_list
        year_list = range(2000, 2014)
        data_dict_by_year = dict()
        selected_data_dict_by_year = dict()
        park_list = [row[0] for row in data_dict[os.path.normcase(os.path.join(self.state_path,"ndvi results/ndvi parks.csv"))] if row[0] != " "]
        for year in year_list:
            local_year_data_list = list()
            selected_local_year_data_list = list()
            temp_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "get_near_result/near_temp_aprsep.csv"))]
            temp_dist_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "near_dis_temp_aprsep/near_distance.csv"))]
            ave_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "get_near_result/near_ave_aprsep.csv"))]
            ave_dist_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "near_dis_ave_aprsep/near_distance.csv"))]
            aot_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "get_near_result/near_aot_aprsep.csv"))]
            aot_dist_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "near_dis_aot_aprsep/near_distance.csv"))]
            prcp_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "get_near_result/near_prcp_aprsep.csv"))]
            prcp_dist_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "near_dis_prcp_aprsep/prcp_near_distance.csv"))]
            ndvi_data_list = data_dict[os.path.normcase(os.path.join(self.state_path, "ndvi results/ndvi parks.csv"))]
            local_data_list_list = [temp_data_list, temp_dist_data_list, ave_data_list, ave_data_list,
                                aot_data_list, aot_dist_data_list, prcp_data_list, prcp_dist_data_list, ndvi_data_list]
            for index, park in enumerate(park_list, start=1):
                local_park_data_list = list()
                local_park_data_list.append(str(index))
                local_park_data_list.append(park)
                local_park_data_list.append(str(year))
                for index, data_list in enumerate(local_data_list_list):
                    if index != 8:
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
                                start_index = year_list.index(year) * 6 + 1
                                for i in range(6):
                                    try:
                                        local_park_data_list.append(row[start_index + i])
                                    except:
                                        print year
                                        print park
                                break
                local_year_data_list.append(local_park_data_list)
            data_dict_by_year[year] = local_year_data_list
        output_file_name = "total_result.csv"
        if os.path.exists(output_path) is False:
            os.mkdir(output_path)
        output_file = os.path.join(output_path, output_file_name)
        with file(output_file, "wb") as file_wd:
            csv_writer = csv.writer(file_wd)
            labels = [" ", "Parks", "Year", "Temp", "Temp_dist", "Ozoneave", "Ozoneave_dist", "Ozoneaot", "Ozoneaot_dist",
                  "Prcp", "Prcp_dist", "NDVI209", "NDVI225", "NDVI241", "NDVI257", "NDVI273", "NDVI289"]
            csv_writer.writerow(labels)
            for year in year_list:
                year_data_list = data_dict_by_year[year]
                for data_list in year_data_list:
                    csv_writer.writerow(data_list)

def create_state_parks():
    """
    创建每一个州以及每个州的总park的shp文件
    :return:
    """
    shp_file_list = glob.glob(os.path.join("D:/Dian/United States/State", "*.shp"))
    in_features = os.path.normcase("D:/Dian/United States/Parks (Local).lyr")
    out_put_dir = os.path.normcase("D:/NDVI APRSEP")
    for shp_file in shp_file_list:
        shp_file_name = os.path.split(shp_file)[-1]
        state_name = shp_file_name[:-4]
        out_put_path = os.path.join(out_put_dir, state_name)
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

if __name__ == "__main__":
    input_dir = os.path.normcase("D:/NDVI APRSEP")
#    create_state_parks()
    state_dir_list = os.listdir(input_dir)
    state_dir_list = [os.path.normcase(os.path.join(input_dir, dir)) for dir in state_dir_list]

    for state_dir in state_dir_list:
        if not os.listdir(state_dir):
            print("%s is empty" %state_dir)
        if os.path.exists(os.path.join(state_dir, "statistic_result/total_result.csv")):
            continue
        state_instance = State_analysis(state_dir)
#        state_instance.create_parks()
#        state_instance.ndvi_mask()
 #       state_instance.ndvi_xml()
        for index in range(1,5):
            task_name = "state_instance.get_near_task" + str(index)
            function = eval(task_name)
            function()
        for index in range(1,5):
            task_name = "state_instance.get_near_distance_task" + str(index)
            function = eval(task_name)
            function()

        for index in range(1,5):
            task_name = "state_instance.get_statistic_task" + str(index)
            function = eval(task_name)
            function()
        state_instance.get_result()
    print "well done"
