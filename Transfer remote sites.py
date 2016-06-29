import os
import xlwt

dir = "C:/Dian/SurfaceOzone/BRW/1993-2010/"


def txt2xls(source_file, year):
    if os.path.exists(source_file):
        print("it is processing " + source_file)
        f = open(source_file)
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Sheet1")
        labels = ["year", "month", "date", "hour", "measurements"]
        for col in range(0, 5):
            ws.write(0, col, labels[col])
            
        row = 0
        month = 0
        for line in f.readlines():
            items = line.split()
            if items:
                if items[0] == 'GMT':
                    month = month + 1
                    continue
                if items[0].isdigit():
                    date = items[0]              
                    for i in range(1,25):
                        ws.write(row + i, 0, year)
                        ws.write(row + i, 1, month)
                        ws.write(row + i, 2, date)
                    i  = 0 #i represents the hour
                    for index in range(1, len(items)): #index just points to element of items 
                        item = items[index] #get the measurement of specific hour
                        if i >= 24:
                            break
                        if len(item) <= 5:  # the measurement is a proper value
                            i = i + 1
                            ws.write(row + i, 3, i) #write the hour 
                            ws.write(row + i, 4, item) #write the measurement
                        else:# the measurement is not a proper value
                            residue = len(item) % 5
                            length = len(item) - residue
                            if residue > 0:
                                i = i + 1
                                ws.write(row + i, 3, i)
                                ws.write(row + i, 4, item[0:residue])
                            while length:
                                i = i + 1
                                if i > 24:
                                    break
                                ws.write(row + i, 3, i)
                                ws.write(row + i, 4,  item[residue:residue + 5])
                                residue = residue + 5
                                length = length - 5
                    row =  row + 24
        f.close()
        wb.save(source_file + '.xls')       
    else:
        print(source_file + " is not exist\n") 
                        
                    
                    

if __name__ == '__main__':
    for year in range(2008, 2010):
        filename = 'brtmpt' + str(year)
        txt2xls(dir + filename, year) 
    print("Work has been done, I love you Ms Dian\n")

        

















