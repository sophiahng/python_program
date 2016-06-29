import arcpy
import os


def make_buffer(in_features, out_features, distance):
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
    arcpy.Buffer_analysis(in_features, out_features, distance)


if __name__ == "__main__":
    pass