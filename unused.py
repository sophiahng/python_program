



out_feature = out_workspace + "urban_sites" + ".shp"
arcpy.Intersect_analysis([outFeatures,urban_polygon], out_feature)
erase_urban = out_workspace + "erase_urban" + ".shp"
arcpy.Erase_analysis(outFeatures, out_feature, erase_urban, "")
out_put = out_workspace+"annualmean"+".shp"
arcpy.Merge_management([out_feature, erase_urban],out_put)

csv_fn = out_put[:-4] + '.csv'
with open(csv_fn,'wb') as csvfile:
    in_db = dbf.Dbf(out_put)
    out_csv = csv.writer(csvfile)
    names = []
    for field in in_db.header.fields:
        names.append(field.name)
    out_csv.writerow(names)
    for rec in in_db:
        out_csv.writerow(rec.fieldData)
    in_db.close()
    print "Done..."