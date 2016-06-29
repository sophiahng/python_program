#coding=utf-8
__author__ = 'Philip'

import os
import glob
import shutil

FILE_PATH = os.path.normcase("D:/Environment Factors/NDVI")
TARGET_PATH = os.path.normcase("D:/Environment Factors/NDVI 200300")

if __name__ == "__main__":
    dir_list = os.listdir(FILE_PATH)
    for file_name in dir_list:
        if file_name.startswith("US"):
            dot_index = file_name.find('.')
            day_number = int(file_name[6:dot_index])
            print day_number
            if day_number in range(200, 301):
                shutil.copy(os.path.join(FILE_PATH, file_name), os.path.join(TARGET_PATH, file_name))




