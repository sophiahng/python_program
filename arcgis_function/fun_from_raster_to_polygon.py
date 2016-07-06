import arcpy
import os
import arcgisscripting
gp = arcgisscripting.create()

def raster_polygon(in_raster_paths, out_polygon_path):
    if not os.path.exists(os.path.dirname(out_polygon_path)):
        os.mkdir(os.path.dirname(out_polygon_path))
    if os.path.exists(os.path.basename(out_polygon_path)):
        return
    arcpy.CheckOutExtension("Spatial")
    gp.RasterToPolygon_conversion(in_raster_paths, out_polygon_path, "NO_SIMPLIFY")


if __name__ == "__main__":
    pass
