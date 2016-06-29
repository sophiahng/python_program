import arcpy

def fill_attribute_table(in_features, field_name, field_value):
    with arcpy.da.UpdateCursor(in_features, field_name) as cursor:
        for row in cursor:
            for i in range(len(row)):
                row[i] = field_value
                cursor.updateRow(row)


if __name__ == "__main__":
    pass