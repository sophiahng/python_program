__author__ = 'Sophia'

from dbfpy import dbf
import os
import csv

def get_state_name_dict():
    state_name_file = os.path.normcase("D:\Dian\Spatial Image\Add attributes\state_name.csv")
    state_name_dict = dict()
    with open(state_name_file, "r") as file_handle:
        reader = csv.reader(file_handle)
        for ind, row in enumerate(reader):
            state_name_dict[int(row[2])] = row[0].strip()
    return state_name_dict


def elevation_new_process(value):
    value = int(value)
    if value >= 1500 and value <= 10000:
        return "High"
    elif value >= 0 and value < 1500:
        return "Low"
    else:
        return "Error"

def location_usr_process(value):
    value = int(value)
    if value in [24,23]:
        return "Urban" 
    elif value in [21,22]:
        return 'Suburban'
    elif value in [-9999, 0]:
        return "0"
    else:
        return 'Rural'
    
def location_ur_process(value):
    value = int(value)
    if value in [24,23]:
        return "Urban"
    elif value in [22,21]:
        return "Suburban"
    elif value in [-9999, 0]:
        return "0"
    else:
        return 'Rural'

def region_process(value):
    try:
        value = int(value)
        if value in [30,38,56,46,31]:
            return 'West North Central'
        elif value in [41,53,16]:
            return 'Northwest'
        elif value in [27,19,55,26]:
            return 'East North Central'
        elif value in [6, 32]:
            return 'West'
        elif value in [49,8,4,35]:
            return 'Southwest'
        elif value in [20,48,40,5,28,22]:
            return 'South'
        elif value in [12,1,13,45,37,51]:
            return 'Southeast'
        elif value in [17,18,39,29,21,54,47]:
            return 'Central'
        elif value in [11,23,33,50,36,42,24,10,34,9,44,25]:
            return 'Northeast'
        else:
            return "Unknown"
    except:
        return "cant find"

def state_name_process(value, state_name_dict):
    try:
        value = int(value)
    except:
        return "cant find"
    return state_name_dict.get(value, "cant find")


def new_location_process(nlcd_value, location_value):
    if location_value == 'Clean':
        return 'Clean'
    if nlcd_value in [24,23]:
        return "Urban"
    elif nlcd_value in [22,21]:
        return "Suburban"
    elif nlcd_value in [-9999, 0]:
        return "0"
    else:
        return 'Rural'


def process_referencefile(file_name):
    reference_db = dbf.Dbf(file_name)
    reference_new_file_name = file_name[:-4] + "_new.csv"
    with open(reference_new_file_name, "w") as output_handle:
        writer = csv.writer(output_handle)
        origin_fields = reference_db.fieldNames
        if "ID_X" in origin_fields:
            origin_fields.remove("ID_X")
        if "ID_Y" in origin_fields:
            origin_fields.remove("ID_Y")
        new_fields = ["ele_new", "loc_usr", "loc_ur", "region", "state_name", 'new_location']
        fields = origin_fields + new_fields
        writer.writerow(fields)
        for rec in reference_db:
            new_row = []
            for field in origin_fields:
                new_row.append(rec[field])
            new_row.append(elevation_new_process(rec["ELEVATION"]))
            new_row.append(location_usr_process(rec['NLCD_2011_']))
            new_row.append(location_ur_process(rec['NLCD_2011_']))
            new_row.append(region_process(rec['STATECODE']))
            new_row.append(state_name_process(rec['STATECODE'], state_name_dict))
            new_row.append(new_location_process(rec['NLCD_2011_'], rec['LOCATION']))
            writer.writerow(new_row)
    reference_db.close()
            
            
            

def process_daylenght(daylength_file_path, sitelist_file_path):
    location_dict = dict()
    require_fields = ['NIGHTLIGHT', 'ELEVATION', 'NLCD_2011_', 'LOCATION', 'POP2010', 'new_location', "ele_new",
                      "loc_usr", "loc_ur", "region", "state_name"]
    with open(sitelist_file_path, 'r') as file_handle:
        fields = []
        reader = csv.reader(file_handle)
        for row_ind, row in enumerate(reader):
            if row_ind == 0:
                fields.extend(row)
                continue
            id_key = str(row[fields.index("ID")])
            id_values = [row[fields.index(field)] for field in require_fields]
            location_dict[id_key] = id_values

    daylength_newfile_path = daylength_file_path[:-4] + "_new.csv"
    with open(daylength_newfile_path, 'w') as output_handle:
        with open(daylength_file_path, 'r') as file_handle:
            origin_fields = []
            new_fields = []
            writer = csv.writer(output_handle)
            reader = csv.reader(file_handle)
            for row_ind, row in enumerate(reader):
                new_row = []
                new_row.extend(row)
                if row_ind == 0:
                    origin_fields.extend(row)
                    new_row.extend(require_fields)
                    new_fields.extend(new_row)
                else:
                    key_id = str(row[origin_fields.index("id")])
                    cant_list = ["cant find" for i in range(len(new_fields))]
                    location = location_dict.get(key_id, cant_list)
                    new_row.extend(location)
                writer.writerow(new_row)




if __name__ == '__main__':
    reference_path = os.path.normcase("D:\Dian\Spatial Image\Add attributes")
    daylength_path = "D:\Dian\Data\Ozone data"
    state_name_dict = get_state_name_dict()
    for year in range(2014, 2015):
        print("Processing year %d" % year)
        reference_name = "Sitelist_new_" + str(year) + ".dbf"
        reference_new_name = "Sitelist_new_" + str(year) + "_new.csv"
        daylength_name = "daylen_" + str(year) + ".csv"
        process_referencefile(os.path.join(reference_path, reference_name))
        process_daylenght(os.path.join(daylength_path, daylength_name), os.path.join(reference_path, reference_new_name))




