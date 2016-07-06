import arcpy
import os


def split_features(in_features, split_features, splitField, out_workplace):
    if not os.path.exists(out_workplace):
        os.mkdir(os.path.dirname(out_workplace))
    arcpy.Split_analysis(in_features, split_features, splitField, out_workplace)

if __name__ == "__main__":
    pass
