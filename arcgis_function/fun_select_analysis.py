import arcpy
import os

def select_analysis(in_features, out_features, SQLClause):
    if not os.path.exists(os.path.dirname(out_features)):
        os.mkdir(os.path.dirname(out_features))
    if os.path.exists(out_features):
        return
    print "processing select analysis.."
    arcpy.Select_analysis(in_features, out_features, SQLClause)

if __name__ == "__main__":
    pass