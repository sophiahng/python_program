__author__ = 'Philip'



import glob
import xlwt
import xlrd
import os


if __name__ == "__main__":
    txt_path = os.path.normcase("D:/NDVI Process/Results of each state")
    target_path = os.path.normcase("D:/NDVI Process/State results")
    if os.path.exists(target_path) is False:
        os.mkdir(target_path)
    xls_file_list = glob.glob(os.path.join(txt_path, "*.xls"))
    xls_file_name_list = [os.path.split(xls_file)[-1] for xls_file in xls_file_list]
    origin_labels = ["XCoord", "YCoord", "GRIDCODE", "STATE", "LATITUDE_2",
                    "LONGITUD_2", "AOT40", "Ozone_avg", "Prcp","TEMP"]
    new_labels = ["XCoord", "YCoord", "GRIDCODE", "STATE", "LATITUDE_2",
                    "LONGITUD_2", "AOT40", "Ozone_avg", "Prcp","TEMP", "TIME"]
    site_list = [xls_file[xls_file.find('.')-2:xls_file.find('.')] for xls_file in xls_file_name_list]
    site_set = set(site_list)
    for site in site_set:
        site_file_list = [xls_file for xls_file in xls_file_list if xls_file[-6:-4] == site]
        output_file = os.path.join(target_path, site + ".xls")
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Sheet1")
        for col, item in enumerate(new_labels):
            ws.write(0, col, item)
        xls_row = 1
        for site_file in site_file_list:
            origin_data_list = list()
            new_data_dict = dict()
            time = os.path.split(site_file)[-1][:8]
            with xlrd.open_workbook(site_file) as site_file_fr:
                sheet_names = site_file_fr.sheet_names()
                for sheet_name in sheet_names:
                    sheet = site_file_fr.sheet_by_name(sheet_name)
                mean_values = sheet.col_values(origin_labels.index("AOT40"))
                mean_values = mean_values[1:]
                mean_values_set = set(mean_values)

                for row in range(1, sheet.nrows):
                    row_values = sheet.row_values(row)
                    origin_data_list.append(row_values)

                for row_values in origin_data_list:
                    mean_value = row_values[origin_labels.index("AOT40")]
                    if mean_value not in new_data_dict.keys():
                        new_data_dict[mean_value] = list()
                    new_data_dict[mean_value].append(row_values)

                for key in new_data_dict:
                    temp_list = new_data_dict[key]
                    temp_list.sort(key = lambda x: x[origin_labels.index("GRIDCODE")])
                    list_nums = len(temp_list)
                    index = int(list_nums * 0.9)
                    temp_list[index].append(time)
                    new_data_dict[key] = temp_list[index]

                for key in new_data_dict:
                    temp_list = new_data_dict[key]
                    for col, item in enumerate(temp_list):
                        ws.write(xls_row, col, item)
                    xls_row = xls_row + 1

        wb.save(output_file)


    print "completed"


