import arcpy



def add_field(in_features, field_name, field_type, field_length):
    arcpy.AddField_management(in_features, field_name, field_type, field_length)


if __name__ == "__main__":
    pass
