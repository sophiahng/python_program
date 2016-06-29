__author__ = 'Sophia'


import os
import glob
import csv


if __name__ == "__main__":
    input_path = 'D:/NDVI/New York/parks/get_near_result'
    output_path = "D:/NDVI/New York/parks/get_near_result"
    input_file_list = glob.glob(os.path.join(input_path, "*.csv"))
    data_dict = dict()
    input_path = "D:/NDVI/New York/parks/get_near_result"
    for input_file in input_file_list:
        with file(input_file, "rb") as file_rd:
            local_data_list = list()
            csv_reader = csv.reader(file_rd)
            for row in csv_reader:
                local_data_list.append(row)
            data_dict[input_file] = local_data_list


    year_list = range(2000, 2015)
    data_dict_by_year = dict()
    selected_data_dict_by_year = dict()
    park_list = [row[0] for row in data_dict["D:/NDVI/New York/parks/get_near_result\\New York NDVI parks.csv"] if row[0] != " "]

    for year in year_list:
        local_year_data_list = list()
        selected_local_year_data_list = list()
        temp_data_list = data_dict["D:/NDVI/New York/parks/get_near_result\\junaug near_temp.csv"]
        aot_data_list = data_dict["D:/NDVI/New York/parks/get_near_result\\junaug near_aot.csv"]
        prcp_data_list = data_dict["D:/NDVI/New York/parks/get_near_result\\near_prcp.csv"]
        ndvi_data_list = data_dict["D:/NDVI/New York/parks/get_near_result\\New York NDVI parks.csv"]

        local_data_list_list = [temp_data_list,aot_data_list, prcp_data_list,ndvi_data_list]

        for index, park in enumerate(park_list, start=1):
            local_park_data_list = list()
            local_park_data_list.append(str(index))
            local_park_data_list.append(park)
            local_park_data_list.append(str(year))
            for index, data_list in enumerate(local_data_list_list):
                if index != 3:
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
                            start_index = year_list.index(year) * 11 + 1
                            for i in range(11):
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
        labels = [" ", "Parks", "Year", "Temp", "Ozoneaot", "Prcp", "NDVI81","NDVI97","NDVI113","NDVI129","NDVI145","NDVI161","NDVI177","NDVI193","NDVI209", "NDVI225", "NDVI241"]
        csv_writer.writerow(labels)
        for year in year_list:
            year_data_list = data_dict_by_year[year]
            for data_list in year_data_list:
                csv_writer.writerow(data_list)















