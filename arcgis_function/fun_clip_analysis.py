import arcpy
import os


def clip_analysis(in_features, clip_features, out_features):
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
    arcpy.Clip_analysis(in_features, clip_features, out_features)


if __name__ == "__main__":
    pass