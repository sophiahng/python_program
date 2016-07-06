import csv
import os


def add_field_by_others(csv_path, new_field, refer_fields, map_func):
    new_csv_path = csv_path[:-4] + "_new.csv"
    if os.path.exists(new_csv_path):
        return
    if not isinstance(refer_fields, (tuple, list)):
        refer_fields = [refer_fields]
    with open(csv_path, 'r') as handle:
        with open(new_csv_path, 'w') as new_handle:
            reader = csv.reader(handle)
            writer = csv.writer(new_handle)
            origin_fields = []
            new_fields = []
            for row_ind, row in enumerate(reader):
                new_row = []
                if row_ind == 0:
                    row_lower = [item.lower() for item in row]
                    origin_fields.extend(row_lower)
                    new_fields.extend(origin_fields)
                    new_fields.append(new_field)
                    new_row.extend(new_fields)
                else:
                    new_row.extend(row)
                    refer_values = [row[origin_fields.index(refer_field)] for refer_field in refer_fields]
                    new_value = map_func(refer_values)
                    new_row.append(new_value)
                writer.writerow(new_row)




