import os
import arcgisscripting
gp = arcgisscripting.create()


def calculate_polygon_area(in_polygon, out_polygon):
    if not os.path.exists(os.path.dirname(out_polygon)):
        os.mkdir(os.path.dirname(out_polygon))
    if os.path.exists(out_polygon):
        return
    print "processing calculating polygon area..."
    gp.CalculateAreas_stats(in_polygon, out_polygon)


if __name__ == "__main__":
    pass
