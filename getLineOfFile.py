import time, linecache, csv
import globalParam



def getLatestOrder(lastOrderID):
    dailyOrderDataFile = time.strftime("%b%d-%Y")+'_order_data.csv'
    #print(dailyOrderDataFile)
    lastLine = None
    with open(globalParam.dailyOrderPath+dailyOrderDataFile, 'r') as file:
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

dailyFoodDataFile = time.strftime("%b%d-%Y")+'_food_data.csv'
count = len(open(globalParam.dailyOrderPath+dailyOrderDataFile).readlines())
print(count)
count = len(open(globalParam.dailyOrderPath+dailyFoodDataFile).readlines())
print(count)
"""