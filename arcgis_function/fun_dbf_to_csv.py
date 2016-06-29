import csv
from dbfpy import dbf

def dbf_csv(in_dbf,out_csv):
    with open(out_csv, 'wb') as csvfile:
        in_db = dbf.Dbf(in_dbf)
        out_csv = csv.writer(csvfile)
        names = []
        for field in in_db.header.fields:
            names.append(field.name)
        out_csv.writerow(names)
        for rec in in_db:
            out_csv.writerow(rec.fieldData)
        in_db.close()

if __name__ == "__main__":
    pass