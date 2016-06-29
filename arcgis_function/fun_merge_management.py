import arcpy
import os


def merge_management(in_features, out_features):
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
        arcpy.Merge_management(in_features, out_features)


if __name__ == "__main__":
    pass

