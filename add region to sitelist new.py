

def get_state_name_dict():
    state_name_file = os.path.join(out_path, "state_name.csv")
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
        new_fields = ["ele_new", "region", "state_name", 'new_location']
        fields = origin_fields + new_fields
        writer.writerow(fields)
        for rec in reference_db:
            new_row = []
            for field in origin_fields:
                new_row.append(rec[field])
            new_row.append(elevation_new_process(rec["ELEVATION"]))
            new_row.append(region_process(rec['STATECODE']))
            new_row.append(state_name_process(rec['STATECODE'], state_name_dict))
            writer.writerow(new_row)
    reference_db.close()

    if __name__ == '__main__':
        state_name_dict = get_state_name_dict()
        reference_name = "Sitelist_new" + ".dbf"
        reference_new_name = "Sitelist_new_" + "_new.csv"
        process_referencefile(os.path.join(out_path, reference_name))