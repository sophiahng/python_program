__author__ = 'Philip'


import glob
import xlwt
import os


if __name__ == "__main__":
    txt_path = os.path.normcase("D:/NDVI Process/Stats/new")
    file_list = glob.glob(os.path.join(txt_path, "*.txt"))
    orgin_labels = ["XCoord", "YCoord", "GRIDCODE", "STATE", "LATITUDE_2",
                    "LONGITUD_2", "MEAN", "MEAN_1", "MAYSEP", "MAYSEP_1", "MEAN_12"]
    new_labels = ["XCoord", "YCoord", "GRIDCODE", "STATE", "LATITUDE_2",
                    "LONGITUD_2", "AOT40", "Ozone_avg", "Prcp","TEMP"]

    for txt_file in file_list:
        txt_file_name = os.path.split(txt_file)[-1][:-4]
        state_value_list = list()
        state_value_set = set()
        with open(txt_file) as txt_file_fr:
            line_list = txt_file_fr.readlines()
            txt_line_list_list = list()
            for line_data in line_list:
                line_data_list = line_data.strip().split(' ')
                if line_data_list[0] == "XCoord":
                    continue
                temp1 = float(line_data_list[-2])
                temp2 = float(line_data_list[-1])
                line_data_list.pop(orgin_labels.index("MEAN_12"))
                line_data_list.pop(orgin_labels.index("MAYSEP_1"))
                if temp1 == float(0):
                    line_data_list.append(temp2)
                else:
                    line_data_list.append(temp1)
                txt_line_list_list.append(line_data_list)
                state_value = line_data_list[orgin_labels.index("STATE")]
                state_value_list.append(state_value)

            state_value_set = set(state_value_list)
            for each_state in state_value_set:
                wb = xlwt.Workbook()
                ws = wb.add_sheet("Sheet1")
                output_file_name = txt_file_name + "_" + str(each_state) + ".xls"
                out_file_name = os.path.join(txt_path, output_file_name)
                for ind, item in enumerate(new_labels):
                    ws.write(0, ind, item)
                row = 1
                for line_data_list in txt_line_list_list:
                    state_value = line_data_list[new_labels.index("STATE")]
                    if state_value != each_state:
                        continue
                    for col, item in enumerate(line_data_list):
                        ws.write(row, col, item)
                    row = row + 1
                wb.save(output_file_name)

    print("completed")







