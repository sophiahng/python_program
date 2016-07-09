import arcpy
import os


def make_event_layer(in_table, out_shp):
    if not os.path.exists(os.path.dirname(out_shp)):
        os.mkdir(os.path.dirname(out_shp))
    if os.path.exists(out_shp):
        return
    x_coords = "longitude"
    y_coords = "latitude"
    spRef = r"D:/Dian/Data/United_States_2000/background/Coordinate.prj"
    arcpy.MakeXYEventLayer_management(in_table, x_coords, y_coords, os.path.basename(out_shp[:-4]), spRef)
    arcpy.FeatureClassToShapefile_conversion(os.path.basename(out_shp[:-4]), out_shp)

if __name__ == "__main__":
    pass