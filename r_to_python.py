from __future__ import division
# coding=utf-8
__author__ = 'Philip'

import os
import glob
import numpy as np
import csv



if __name__ == "__main__":
    hourly_data_file_path = os.path.normcase("D:/Dian/Data/Ozone data")
    day_len_file_path = os.path.normcase("D:/Dian/Data/Ozone data")
    output_file_path = os.path.normcase("D:/Dian/Data/Ozone data/new")
    hourly_data_file_labels = ["State Code", "County Code",	"Site Num", "Parameter Code", "POC", "Latitude",
                               "Longitude",	"Datum", "Parameter Name", "Date Local", "Time Local", "Date GMT",
                               "Time GMT", "Sample Measurement", "Units of Measure", "MDL",	"Uncertainty",
                               "Qualifier",	"Method Type", "Method Name", "State Name",	"County Name",
                               "Date of Last Change"]
    output_file_labels = ["year","statecode","countycode","sitenum","latitude","longitude","mean","sd"]
    day_len_file_labels = ["sunrise", "sunset", "daylen"]
    hourly_data_file_list = list()
    day_len_file_list = list()

    abstract_file_list = glob.glob(os.path.join(hourly_data_file_path, "*.csv"))
    for item in abstract_file_list:
        item_name = os.path.split(item)[-1]
        if item_name[:item_name.find("_")] == "hourly":
            hourly_data_file_list.append(item)

    abstract_file_list = glob.glob(os.path.join(day_len_file_path, "*.csv"))
    for item in abstract_file_list:
        item_name = os.path.split(item)[-1]
        if item_name[:item_name.find("_")] == "daylen":
            day_len_file_list.append(item)



    for hourly_data_file in hourly_data_file_list:
        hourly_data_file_name = os.path.split(hourly_data_file)[-1]
        hourly_data_file_year = hourly_data_file_name[-8:hourly_data_file_name.find(".")]
        if hourly_data_file_year != "2003":
            continue
        hourly_data_file_ids = list()
        hourly_data_file_datelocal = list()
        hourly_data_file_timelocal = list()
        hourly_data_file_location = list()
        hourly_data_file_measurement = list()
        hourly_data_file_ids_set = set()
        day_len_file = None
        day_len_file_sunrise = list()
        day_len_file_sunset = list()
        day_len_file_daylen = list()
        for item in day_len_file_list:
            item_name = os.path.split(item)[-1]
            if item_name[item_name.find("_") + 1:item_name.find(".")] == hourly_data_file_year:
                day_len_file = item
                break
        with open(hourly_data_file, "rU") as hourly_data_file_fd:
            hourly_data_file_reader = csv.reader(hourly_data_file_fd)
            for hourly_data_line in hourly_data_file_reader:
                if hourly_data_line[0] == "State Code":
                    continue
                hourly_data_line_statecode = hourly_data_line[hourly_data_file_labels.index("State Code")]
                hourly_data_line_countycode = hourly_data_line[hourly_data_file_labels.index("County Code")]
                hourly_data_line_sitenum = hourly_data_line[hourly_data_file_labels.index("Site Num")]
                hourly_data_line_id = "_".join([hourly_data_line_statecode, hourly_data_line_countycode, hourly_data_line_sitenum])
                hourly_data_file_ids.append(hourly_data_line_id)
                hourly_data_line_location = hourly_data_line[hourly_data_file_labels.index("Latitude")] + "_" + hourly_data_line[hourly_data_file_labels.index("Longitude")]
                hourly_data_file_location.append(hourly_data_line_location)
                hourly_data_line_timelocal = hourly_data_line[hourly_data_file_labels.index("Time Local")]
                hourly_data_file_timelocal.append(hourly_data_line_timelocal)
                hourly_data_line_datelocal = hourly_data_line[hourly_data_file_labels.index("Date Local")]
                hourly_data_file_datelocal.append(hourly_data_line_datelocal)
                hourly_data_line_measurement = hourly_data_line[hourly_data_file_labels.index("Sample Measurement")]
                hourly_data_file_measurement.append(hourly_data_line_measurement)

        with open(day_len_file, "rU") as day_len_file_fd:
            day_len_file_reader = csv.reader(day_len_file_fd)
            for day_len_line in day_len_file_reader:
                if day_len_line[0] == "sunrise":
                    continue
                day_len_line_sunrise = day_len_line[day_len_file_labels.index("sunrise")]
                day_len_file_sunrise.append(day_len_line_sunrise)
                day_len_line_sunset = day_len_line[day_len_file_labels.index("sunset")]
                day_len_file_sunset.append(day_len_line_sunset)
                day_len_line_daylen = day_len_line[day_len_file_labels.index("daylen")]
                day_len_file_daylen.append(day_len_line_daylen)
        if len(day_len_file_daylen) != len(hourly_data_file_ids):
            print("Length of hourly_data_file and day_len_file is not equal")
            continue

        hourly_data_file_ids_set = set(hourly_data_file_ids)
        hourly_data_file_id_list = list()
        for hourly_data_file_id in hourly_data_file_ids_set:
            hourly_data_id_dict = dict()
            hourly_data_id_dict["id"] = hourly_data_file_id
            hourly_data_id_dict["year"] = hourly_data_file_year

            hourly_data_file_id_indexs = [index for (index, value) in enumerate(hourly_data_file_ids) if value == hourly_data_file_id]
            temp_previous_date = None
            temp_day_data_list = list()
            temp_year_data_list = list()
            temp_day_valid_nums = 0
            temp_day_theo_nums = 0
            temp_year_valid_nums_list = list()
            temp_year_theo_nums_list = list()
            for index in hourly_data_file_id_indexs:
                hourly_data_date = hourly_data_file_datelocal[index]

                if hourly_data_date.find("/") > 0:
                    hourly_data_month = hourly_data_date.split("/")[0]
                    hourly_data_day = hourly_data_date.split("/")[1]
                elif hourly_data_date.find("-") > 0:
                    hourly_data_month = hourly_data_date.split("-")[1]
                    hourly_data_day = hourly_data_date.split("-")[2]
                else:
                    print("unknown date format")

                if int(hourly_data_month) == 5 and int(hourly_data_day) == 1:
                    hourly_data_id_dict["index_start"] = index
                elif int(hourly_data_month) == 9 and int(hourly_data_day) == 30:
                    hourly_data_id_dict["index_end"] = index
                elif int(hourly_data_month) < 5 or int(hourly_data_month) >= 10:
                    continue
#####################################################
                #   valid index  after month choice

                if hourly_data_id_dict.get("valid_index", None) == None:
                    hourly_data_id_dict["valid_index"] = index
                hourly_data_measurement = hourly_data_file_measurement[index]
                day_sunrise = day_len_file_sunrise[index]
                day_sunset = day_len_file_sunset[index]
                day_daylen = day_len_file_daylen[index]
                hourly_data_time = hourly_data_file_timelocal[index]

                hour = int(hourly_data_time[:hourly_data_time.find(":")])
                if day_sunrise.find(".") < 0:
                    sunrise_hour = int(day_sunrise)
                else:
                    sunrise_hour = int(day_sunrise[:day_sunrise.find(".")])
                if day_sunset.find(".") < 0:
                    sunset_hour = int(day_sunset)
                else:
                    sunset_hour = int(day_sunset[:day_sunset.find(".")])

                if temp_day_theo_nums == 0:
                    temp_day_theo_nums = sunset_hour - sunrise_hour
                    if temp_day_theo_nums < 0:
                        print("there have theo num which is negative")

                if temp_previous_date == None or temp_previous_date == hourly_data_date:
                    temp_previous_date = hourly_data_date
                    if hour > sunrise_hour and hour <= sunset_hour:
                        if float(hourly_data_measurement) > 0.04:
                            temp_day_data_list.append(float(hourly_data_measurement) - 0.04)
                        temp_day_valid_nums = temp_day_valid_nums + 1
                elif temp_previous_date != hourly_data_date:
                    if temp_day_valid_nums == 0:
                        temp_previous_date = hourly_data_date
                        continue
                    temp_previous_date = hourly_data_date
                    temp_year_data_list.append(sum(temp_day_data_list))
                    temp_year_valid_nums_list.append(temp_day_valid_nums)
                    temp_year_theo_nums_list.append(temp_day_theo_nums)
                    temp_day_data_list = []
                    temp_day_valid_nums = 0

                    temp_day_theo_nums = sunset_hour - sunrise_hour
                    if temp_day_theo_nums < 0:
                        print("there have theo num which is negative")
                    if hour > sunrise_hour and hour <= sunset_hour:
                        if float(hourly_data_measurement) > 0.04:
                            temp_day_data_list.append(float(hourly_data_measurement) - 0.04)
                        temp_day_valid_nums = temp_day_valid_nums + 1

                if index == hourly_data_file_id_indexs[-1]:
                    temp_year_data_list.append(sum(temp_day_data_list))
                    temp_year_valid_nums_list.append(temp_day_valid_nums)
                    temp_year_theo_nums_list.append(temp_day_theo_nums)

            if len(temp_year_theo_nums_list) == 0 or len(temp_year_valid_nums_list) == 0:
                print("%s is null"%hourly_data_file_id)
                continue
            if sum(temp_year_valid_nums_list)/sum(temp_year_theo_nums_list) < 0.75:
                print("%s is less than 0.75"%hourly_data_file_id)
                continue

            narray = np.array(temp_year_data_list)
            hourly_data_id_dict["mean"] = np.mean(narray) * 1000
            hourly_data_id_dict["std"] = np.std(narray)
            hourly_data_file_id_list.append(hourly_data_id_dict)

        output_file_name = "aaotdaylen40_" + hourly_data_file_year + ".csv"
        output_file_name = os.path.join(output_file_path, output_file_name)
        with open(output_file_name, "wb") as output_file_fd:
            output_file_writer = csv.writer(output_file_fd)
            output_file_writer.writerow(output_file_labels)
            for item_dict in hourly_data_file_id_list:
                temp_list = list()
                temp_list.append(item_dict["year"])
                temp_list.extend(item_dict["id"].split("_"))
                temp_list.extend(hourly_data_file_location[item_dict["valid_index"]].split("_"))
                temp_list.append(item_dict["mean"])
                temp_list.append(item_dict["std"])
                output_file_writer.writerow(temp_list)


        print("%s is done" % hourly_data_file)






















