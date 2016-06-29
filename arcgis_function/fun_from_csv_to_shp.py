import arcpy
import os

def make_event_layer(in_table, out_subdir, base_name):
    if not os.path.exists(out_subdir):
        os.mkdir(out_subdir)
    x_coords = "longitude"
    y_coords = "latitude"
    spRef = r"D:/Dian/Data/United_States_2000/background/Coordinate.prj"
    arcpy.MakeXYEventLayer_management(in_table, x_coords, y_coords, base_name, spRef)
    arcpy.FeatureClassToShapefile_conversion(base_name, out_subdir)

if __name__ == "__main__":
    pass