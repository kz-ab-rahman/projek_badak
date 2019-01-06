#!python3
import csv, re
import globalParam

def getChargeDetail(restaurantName):
    chargeList=[]
    with open(globalParam.restaurantDataFile, 'r') as file:
        next(file) #skip csv header
        reader = csv.reader(file)
        found = False
        for line in reader:
            if line[1] == restaurantName:
                chargeList = line[-5:]
                found = True
                break
            else:
                pass
    if not found:
        chargeList = -1
    return chargeList

def findRestaurant(key):
    with open(globalParam.restaurantDataFile, 'r') as file:
        next(file) #skip csv header
        reader = csv.reader(file)
        found = False
        for line in reader:
            if line[5] == key:
                restaurantName = line[1]
                found = True
                break
            else:
                restaurantName = 'no match'
    return restaurantName

def genMasterOrderList(orderInfoList, restaurantName, orderFileName, tag):
    if restaurantName == 'Hippo Food Delivery':
        firstFood = orderInfoList[2][0][0]
        match = re.search(r".*\((.*)\)",firstFood)
        restaurantKey = match.group(1)
        restaurantName = findRestaurant(restaurantKey)

    chargeList = getChargeDetail(restaurantName)
    chargeType = int(chargeList[0])
    deliveryCharge = float(chargeList[-1])
    chargeToShop = float(chargeList[chargeType]) #charge to kedai varies depends on charge type
    #print(chargeType,chargeToShop,deliveryCharge)

    #calculate total food price and quantity, and generate food summary
    totalFoodPrice = 0
    totalFoodQuantity = 0
    foodSummary=''
    for i, foodItem in enumerate(orderInfoList[2]):
        food = foodItem[0]
        unitPrice = float(foodItem[1])
        #print(unitPrice)
        quantity = int(foodItem[2])
        totalPrice = unitPrice*quantity
        #print(totalPrice)
        totalFoodQuantity+=quantity
        totalFoodPrice+=totalPrice
        if i > 0:
            spacer='; '
        else:
            spacer=''
        foodSummary+=spacer+str(quantity)+'x '+food
    chargeToCustomer = totalFoodPrice + deliveryCharge
    if chargeType == 2: #we charge kedai per pack for type 2
        chargeToShop = chargeToShop*totalFoodQuantity
    payToShop = totalFoodPrice - chargeToShop

    dummyList=orderInfoList.copy()
    del dummyList[2] #delete food list from master list. replace with summary
    dummyList[3] = restaurantName #replace name+adress with just name
    masterOrderList = dummyList
    masterOrderList.extend([foodSummary,totalFoodQuantity,chargeType,totalFoodPrice,deliveryCharge,chargeToCustomer,chargeToShop,payToShop,orderFileName,tag]) #append misc info
    #date reformating for order 1892380 and below.
    orderID = float(masterOrderList[0])
    if orderID <= 1892380:
        #print('date reformatting required')
        masterOrderList[1], masterOrderList[2] = reformatDate(masterOrderList[1], masterOrderList[2])

    return masterOrderList

def genMasterFoodList(orderID, restaurantName, foodInfoList, orderFileName, tag):
    if restaurantName == 'Hippo Food Delivery':
        firstFood = foodInfoList[0][0]
        match = re.search(r".*\((.*)\)",firstFood)
        restaurantKey = match.group(1)
        restaurantName = findRestaurant(restaurantKey)

    dummyList=foodInfoList.copy()
    for item in dummyList:
        item.insert(0,orderID)
        item.insert(1,restaurantName)
        item.extend([orderFileName,tag])
    return dummyList

def pushToCsv(masterOrderList, masterFoodList):
    with open(globalParam.orderDataFile, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(masterOrderList)
    with open(globalParam.foodDataFile, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for item in masterFoodList:
            wr.writerow(item)
    return

def reformatDate(date1, date2):
    match = re.search(r"(\d+)\/(\d+)(.*)",date1)
    if match:
        newDate1 = match.group(2)+'/'+match.group(1)+match.group(3)
    match = re.search(r"(\d+)\/(\d+)(.*)",date2)
    if match:
        newDate2 = match.group(2)+'/'+match.group(1)+match.group(3)
    return newDate1, newDate2

"""
orderInfoList=['1898054', '02/01/2019 12:30 PM', [['Set Asam Pedas (MT)', '7.00', '1', ' '], ['Nasi Ayam Kunyit (NK)', '7.00', '1', ' ']], '02/01/2019 11:10 AM', "Hippo Food Delivery (Mangkuk Tingkat (MT)/Nan's Kitchen(NK)/Tapoou (TP)) Bertamlakeside , Kepala Batas, Penang, Malaysia", 'nurul nadiah azmi', '01114430036', 'yon.paan@yahoo.com', 'no 55 g jalan dagangan 10 no 5 g']
foodInfoList=[['Set Asam Pedas (MT)', '7.00', '1', ' '], ['Nasi Ayam Kunyit (NK)', '7.00', '1', ' ']]
restaurantInfoList=['Hippo Food Delivery', 'Bertamlakeside , Kepala Batas, Penang, Malaysia', '', '']
customerInfoList=['nurul nadiah azmi', '01114430036', 'yon.paan@yahoo.com', 'no 55 g jalan dagangan 10 no 5 g']
orderFileName = 'new_order_01012019.010636.html.txt'
tag=''

masterOrderList = genMasterOrderList(orderInfoList, restaurantInfoList[0], orderFileName, tag)
masterFoodList = genMasterFoodList(orderInfoList[0], restaurantInfoList[0], foodInfoList, orderFileName, tag)
print('masterOrderList:')
print(masterOrderList)
print('masterFoodList:')
print(masterFoodList)
#pushToCsv(masterOrderList,masterFoodList)
"""