import os
import arcgisscripting
gp = arcgisscripting.create()


def calculate_polygon_area(in_polygon, out_polygon):
    if not os.path.exists(out_polygon):
        os.mkdir(os.path.dirname(out_polygon))
    gp.CalculateAreas_stats(in_polygon, out_polygon)


if __name__ == "__main__":
    pass
