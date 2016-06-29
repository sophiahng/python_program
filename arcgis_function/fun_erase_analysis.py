import arcpy
import os


def erase_analysis(in_features, erase_features, out_features):
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
    arcpy.Erase_analysis(in_features, erase_features, out_features)


if __name__ == "__main__":
    pass

