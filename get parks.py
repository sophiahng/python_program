__author__ = 'Philip'

import os
import glob
import csv


if __name__ == "__main__":
    file_path = os.path.normcase('D:/NDVI Parks/New York/try')
    file_list = glob.glob(os.path.join(file_path, "*.csv"))
    park_dict = dict()
    for csv_file in file_list:
        park_name = os.path.split(csv_file)[-1][:-4]
        with file(csv_file, "rb") as file_fd:
            local_park_list = list()
            csv_reader = csv.reader(file_fd)
            for row in csv_reader:
                if row[2] == "error":
                    continue
                local_park_list.append(row[0])
            park_dict[park_name] = local_park_list
    share_park_set = None
    for key, value in park_dict.items():
        if share_park_set == None:
            share_park_set = set(value)
        else:
            share_park_set = share_park_set & set(value)
    for csv_file in file_list:
        file_data_list = list()
        with file(csv_file, "rb") as file_fd:
            csv_reader = csv.reader(file_fd)
            for row in csv_reader:
                if row[0] in share_park_set:
                    file_data_list.append(row)
        with file(csv_file, "wb") as file_fd:
            csv_writer = csv.writer(file_fd)
            for row in file_data_list:
                csv_writer.writerow(row)

