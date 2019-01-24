import time, linecache, csv
import global_param



def getLatestOrder(lastOrderID):
    dailyOrderDataFile = time.strftime("%b%d-%Y")+'_order_data.csv'
    #print(daily_order_data_file)
    lastLine = None
    with open(global_param.daily_path + dailyOrderDataFile, 'r') as file:
        next(file) #skip csv header
        reader = csv.reader(file)
        for line in reader:
            print(line)
            lastLine = line

    orderID = float(lastLine[0])
    if orderID == float(lastOrderID):
        return 0
    else:
        return orderID

print(getLatestOrder(123))




"""

daily_food_data_file = time.strftime("%b%d-%Y")+'_food_data.csv'
count = len(open(globalParam.daily_path+daily_order_data_file).readlines())
print(count)
count = len(open(globalParam.daily_path+daily_food_data_file).readlines())
print(count)
"""