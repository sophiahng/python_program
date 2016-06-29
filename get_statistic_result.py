__author__ = 'Philip'

import os
import glob
import csv



if __name__ == "__main__":
    input_path = 'D:/NDVI Parks/Calnifornia/get_near_result'
    input_file_list = glob.glob(os.path.join(input_path, "*.csv"))
    data_dict = dict()
    for input_file in input_file_list:
        input_file_name = os.path.split(input_file)[-1]
        with file(input_file, "rb") as file_rd:
            local_data_list = list()
            csv_reader = csv.reader(file_rd)
            for row in csv_reader:
                local_data_list.append(row)
            data_dict[input_file_name] = local_data_list
    year_list = range(2000, 2014)
    data_dict_by_year = dict()
    selected_data_dict_by_year = dict()
    park_list = [row[0] for row in data_dict["near_ave_maysep.csv"] if row[0] != " "]
    selected_park_list = list()
    selected_park_ur_list = list()
    with file(os.path.join(input_path, "Selected parks.csv"), "rb") as file_rd:
        csv_reader = csv.reader(file_rd)
        for row in csv_reader:
            if row[3] != "2000":
                continue
            selected_park_list.append(row[2])
            selected_park_ur_list.append(row[1])

    for year in year_list:
        local_year_data_list = list()
        selected_local_year_data_list = list()
        temp_data_list = data_dict["near_temp.csv"]
        temp_dist_data_list = data_dict["temp_near_distance.csv"]
        ave_data_list = data_dict["near_ave_maysep.csv"]
        ave_dist_data_list = data_dict["ave_near_distance.csv"]
        aot_data_list = data_dict["near_aot_maysep.csv"]
        aot_dist_data_list = data_dict["aot_near_distance.csv"]
        prcp_data_list = data_dict["near_prcp.csv"]
        prcp_dist_data_list = data_dict["prcp_near_distance.csv"]
        ndvi_data_list = data_dict["NDVI NY parks.csv"]

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
                                local_park_data_list.append(row[start_index + i])
                            break
            local_year_data_list.append(local_park_data_list)
        data_dict_by_year[year] = local_year_data_list

        for index, park in enumerate(selected_park_list, start=1):
            local_park_data_list = list()
            local_park_data_list.append(str(index))
            local_park_data_list.append(selected_park_ur_list[index - 1])
            local_park_data_list.append(park)
            local_park_data_list.append(str(year))
            selected_local_park_data_list = list()
            selected_local_park_data_list.append(str(index))
            selected_local_park_data_list.append(park)
            selected_local_park_data_list.append(str(year))
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
                                local_park_data_list.append(row[start_index + i])
                            break
            selected_local_year_data_list.append(local_park_data_list)
        selected_data_dict_by_year[year] = selected_local_year_data_list

    output_file_name = "total_result.csv"
    output_file = os.path.join(input_path, output_file_name)
    with file(output_file, "wb") as file_wd:
        csv_writer = csv.writer(file_wd)
        labels = [" ", "Parks", "Year", "Temp", "Temp_dist", "Ozoneave", "Ozoneave_dist", "Ozoneaot", "Ozoneaot_dist",
                  "Prcp", "Prcp_dist", "NDVI209", "NDVI225", "NDVI241", "NDVI257", "NDVI273", "NDVI289"]
        csv_writer.writerow(labels)
        for year in year_list:
            year_data_list = data_dict_by_year[year]
            for data_list in year_data_list:
                csv_writer.writerow(data_list)

    output_file_name = "seleted_total_result.csv"
    output_file = os.path.join(input_path, output_file_name)
    with file(output_file, "wb") as file_wd:
        csv_writer = csv.writer(file_wd)
        labels = [" ", "UR", "Parks", "Year", "Temp", "Temp_dist", "Ozoneave", "Ozoneave_dist", "Ozoneaot",
                  "Ozoneaot_dist", "Prcp", "Prcp_dist", "NDVI209", "NDVI225", "NDVI241", "NDVI257", "NDVI273", "NDVI289"]
        csv_writer.writerow(labels)
        for year in year_list:
            year_data_list = selected_data_dict_by_year[year]
            for data_list in year_data_list:
                csv_writer.writerow(data_list)


    output_file_name = "selected_parks_info.csv"
    output_file = os.path.join(input_path, output_file_name)
    with file(output_file, "wb") as file_wd:
        csv_writer = csv.writer(file_wd)
        csv_writer.writerow(selected_park_list)
        csv_writer.writerow(selected_park_ur_list)











