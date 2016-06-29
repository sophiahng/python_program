import arcpy


def build_pyramid(in_raster):
    arcpy.BuildPyramids_management(in_raster)


if __name__ == "__main__":
    pass
