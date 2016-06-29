import csv

def region_process(input_csv):
    try:
        value = int(value)
        if value in [30,38,56,46,31]:
            return 'West North Central'
        elif value in [41,53,16]:
            return 'Northwest'
        elif value in [27,19,55,26]:
            return 'East North Central'
        elif value in [6, 32]:
            return 'West'
        elif value in [49,8,4,35]:
            return 'Southwest'
        elif value in [20,48,40,5,28,22]:
            return 'South'
        elif value in [12,1,13,45,37,51]:
            return 'Southeast'
        elif value in [17,18,39,29,21,54,47]:
            return 'Central'
        elif value in [11,23,33,50,36,42,24,10,34,9,44,25]:
            return 'Northeast'
        else:
            return "Unknown"
    except:
        return "cant find"