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
    #####Handling for fast food delivery
    if orderFileName.find('type3') != -1: #fast food
        chargeList = getChargeDetail('fast food')
        chargeType = int(chargeList[0])
        deliveryCharge = float(chargeList[-1])
        chargeToShop = float(chargeList[chargeType])

        foodSummary = orderInfoList[2][0][0]
        totalFoodQuantity = None
        totalFoodPrice = None
        chargeToCustomer = None
        payToShop = None
    ######Done handling for fast food delivery
    else:
        if restaurantName == 'Hippo Food Delivery':
            firstFood = orderInfoList[2][0][0]
            #print(firstFood)
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
        masterOrderList[1] = reformatDate(masterOrderList[1])
        masterOrderList[2] = reformatDate(masterOrderList[2])

    return masterOrderList

def genMasterFoodList(orderID, restaurantName, foodInfoList, orderFileName, tag):
    if restaurantName == 'Hippo Food Delivery':
        firstFood = foodInfoList[0][0]
        #print(firstFood)
        match = re.search(r".*\((.*)\)",firstFood)
        restaurantKey = match.group(1)
        restaurantName = findRestaurant(restaurantKey)

    dummyList=foodInfoList.copy()
    for item in dummyList:
        item.insert(0,orderID)
        item.insert(1,restaurantName)
        item.extend([orderFileName,tag])
    return dummyList

def pushToCsv(pushTo, masterOrderList, masterFoodList):
    #trakcingList = [status,rider,pickup_actual,deliver_actual]
    trackingList = ['new','not assigned',None,None]
    if pushTo == 'master':
        orderDataFile = globalParam.orderDataFile
        foodDataFile = globalParam.foodDataFile
    if pushTo == 'daily':
        orderDataFile = globalParam.dailyOrderDataFile
        foodDataFile = globalParam.dailyFoodDataFile
        masterOrderList.extend(trackingList) #append trakcingList before writing to file

    with open(orderDataFile, 'a+', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(masterOrderList)
    with open(foodDataFile, 'a+', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for item in masterFoodList:
            wr.writerow(item)
    return

def reformatDate(oldDate):
    """
    reformat date from MM/DD/YYYY -> DD/MM/YYYY
    """
    match = re.search(r"(\d+)\/(\d+)(.*)",oldDate)
    if match:
        newDate = match.group(2)+'/'+match.group(1)+match.group(3)
    return newDate


tag=''
orderFileName = 'type0_14012019.233937.html.txt'
orderInfoList = ['1926717', '14/01/2019 2:25 PM', [['Nasi Briyani Daging', '10.00', '1', ' '], ['Nasi Briyani Chicken Buttermilk', '12.00', '1', ' ']], '14/01/2019 1:23 PM', "D'Biryani Hyderabad  Persiaran Seksyen 4/8, Bandar Putra Bertam, 13200 Kepala Batas, Pulau Pinang, Malaysia", 'Emy Marhainis', '0103837765', 'iffah.mohamed@gmail.com', 'No.11 Lorong Limonia 8 Bertam lakeside']
foodInfoList = [['Nasi Briyani Daging', '10.00', '1', ' '], ['Nasi Briyani Chicken Buttermilk', '12.00', '1', ' ']]
restaurantInfoList = ["D'Biryani Hyderabad", 'Persiaran Seksyen 4/8, Bandar Putra Bertam, 13200 Kepala Batas, Pulau Pinang, Malaysia', 'Hazieq', '60194970371']
customerInfoList = ['Emy Marhainis', '0103837765', 'iffah.mohamed@gmail.com', 'No.11 Lorong Limonia 8 Bertam lakeside']

masterOrderList = genMasterOrderList(orderInfoList, restaurantInfoList[0], orderFileName, tag)
masterFoodList = genMasterFoodList(orderInfoList[0], restaurantInfoList[0], foodInfoList, orderFileName, tag)
print('masterOrderList = ', end='')
print(masterOrderList)
print('masterFoodList = ', end='')
print(masterFoodList)
pushTo = 'daily'
print("Pushing data to master csv...")
pushToCsv(pushTo, masterOrderList,masterFoodList)
