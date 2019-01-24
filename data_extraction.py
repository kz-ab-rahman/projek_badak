#!python3

import re, linecache, csv, copy
import globalParam, dataProcessing

def getOrderTool(orderFileName):
    if orderFileName.find('type0') != -1:
        return 'app'
    elif orderFileName.find('type1') != -1:
        return 'webapp/emulator'
    else:
        return 'fastfood'

def flattenRawEmail(orderFileName):
    with open(globalParam.rawEmailPath+orderFileName, 'r+') as file:
        currentline=''
        for line in file:
            line = line.strip('\n')
            line = line.replace('=','')
            currentline = currentline + line
        #print(currentline)
        file.seek(0)
        file.write(currentline)
        file.truncate()
    return

def getOrderInfo(orderFileName):
    #print("inside getOrderInfo")
    line = linecache.getline(globalParam.rawEmailPath+orderFileName, 1)
    regexStringOrder = re.compile(globalParam.regexInOrder)
    regexStringFood = re.compile(globalParam.regexInFood)

    match = re.search(regexStringOrder, line)
    #print(match)
    if match:
        orderInfoList = list(match.groups())
        #print('orderInfoList[2]: '+orderInfoList[2])
        foodInfo = orderInfoList[2].replace('</p><p><strong>Details','</p>||<p><strong>Details')
        #print('foodInfo: '+foodInfo)
        foodInfoList = foodInfo.split('||')
        keys=[]
        for i, rawFood in enumerate(foodInfoList):
            #print(i, rawFood)
            foodMatch = re.search(regexStringFood, rawFood)
            if foodMatch:
                food = foodMatch.group(1)
                unitPrice = foodMatch.group(2)
                #option = foodMatch.group()
                quantity = foodMatch.group(3)
                note = foodMatch.group(4)
                match = re.search(r".*\((.*(?:Nasi|Mee|Keow|Bihun).*)\)", food) #will match if the food is in ()
                if match:
                    food = match.group(1) #take the food inside the bracket
                match = re.search(r"[\w+\s]+\(([A-Z]{2})\)", food) #<word><space>(kedai key)
                if match:
                    key = match.group(1) #take the kedai key
                    keys.append(key)
            else:
                food = 'no match'
                unitPrice = 'no match'
                #option = 'no match'
                quantity = 'no match'
                note = 'no match'
            foodInfoList[i]=[food,unitPrice,quantity,note]

        orderInfoList[2] = foodInfoList

        #####handling for multiple kedai in 1 order for nasi ekonomi Hippo Food
        uniqueKey = list(set(keys)) #remove duplicate key in keys[]
        #print(uniqueKey)
        kedaiHippo = len(uniqueKey) #num of kedai = number of item uniquekey
        if kedaiHippo > 1: #if 0: not hippofood, if 1: hippofood from 1 kedai only. we process only if hippofood kedai more than 1
            #print('num of kedai HippoFood: '+str(kedaiHippo))
            megaOrderList = [None]*kedaiHippo #create new big list with number of item = number of kedai
            for i, subOrderList in enumerate(megaOrderList):
                subOrderList = copy.deepcopy(orderInfoList)
                subOrderList[0] = subOrderList[0]+'.'+str(i+1) #each suborder will have number increment after .
                #print(f"\nSuborderID: {subOrderList[0]}")
                key=uniqueKey[i]
                newFoodInfoList = [] # new empty list to store those foodinfo that matched key
                for j, foodInfo in enumerate(subOrderList[2]):
                    result = foodInfo[0].find(key) #check id key exist in food name
                    #print(f"food{j}, {key}, {food}, {result}")
                    if result != -1: # if exist
                        newFoodInfoList.append(foodInfo) #append the foodInfo to the new list
                subOrderList[2] = copy.deepcopy(newFoodInfoList)
                #print(subOrderList)
                megaOrderList[i] = copy.deepcopy(subOrderList)
            orderInfoList = megaOrderList
        #####Done handling for multiple kedai in 1 order
        else:
            megaOrderList=[orderInfoList]
            kedaiHippo=1
    ######handling for fast food delivery
    elif orderFileName.find('type3') != -1: #fast food delivery (type2) handler
        orderInfoList=[None]*9
        foodInfoList=[None]*4
        match = re.search(r"formID(\d+)",orderFileName) #extract formID from the filename
        orderInfoList[0] = match.group(1) #use formID as orderID
        regexStringFastFood = re.compile(globalParam.regexInFastFood)
        match = re.search(regexStringFastFood, line)
        if match:
            orderInfoList[5] = match.group(1) #customer's name
            orderInfoList[6] = match.group(2) #customer's phone
            orderInfoList[8] = match.group(3) #customer's address
            orderInfoList[3] = match.group(7)+' '+match.group(8)
            orderInfoList[4] = match.group(4) #restaurant name
            foodInfoList[0]  = match.group(5) #foodname
            orderInfoList[2] = [foodInfoList] #foodInfoList. need to list of list
            orderInfoList[1] = match.group(7)+' '+ match.group(6) #requested delivery time

        megaOrderList = [orderInfoList]
        kedaiHippo = 1
    ######Done handling for fast food delivery
    else:
        orderInfoList=['no match']*9
        megaOrderList=[orderInfoList]
        kedaiHippo = 0

    return kedaiHippo, megaOrderList

def addRestaurant():
    print('Restaurant not in the list. Please add Restaurant info.')
    name=input('Restaurant Name: ')
    nameID=input('Unique ID: ')
    address=input('Address: ')
    pic=input('Contact Person: ')
    phoneNum=input('Phone Number: ')
    chargeType=input('Charge Type (1, 2, or 3): ')
    chargeAmount=input('Charge Amount: RM')
    deliveryCharge=input('Delivery Charge: RM')
    newInfo = [nameID, name, address, pic, phoneNum, chargeType,'0','0','0',deliveryCharge]
    newInfo[int(chargeType)+5] = chargeAmount
    with open(globalParam.restaurantDataFile, 'a', newline='') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        wr.writerow(newInfo)
    return [name,address,pic,phoneNum]

def getRestaurantInfo(restaurantInfo):
    #print("inside getRestaurant")
    #print(restaurantInfo)
    with open(globalParam.restaurantDataFile, 'r') as file:
        next(file) #skip csv header
        reader = csv.reader(file)
        found = False
        for line in reader:
            result = restaurantInfo.lower().find(line[0])
            if result != -1:
                name = line[1]
                address = line[2]
                pic = line[3] #person in-charge
                phoneNum = line[4]
                found = True
                break
            else:
                pass
    if found:
        restaurantInfoList = [name,address,pic,phoneNum]
    else:
        restaurantInfoList = [restaurantInfo,None,None,None]
    #print(restaurantInfoList)
    return restaurantInfoList

"""
orderFileName = 'type0_14012019.233937.html.txt'
tag=''
#flattenRawEmail(orderFileName)
numOfKedai, megaOrderList = getOrderInfo(orderFileName)
for orderInfoList in megaOrderList:
    foodInfoList = orderInfoList[2]
    restaurantInfoList = getRestaurantInfo(orderInfoList[4])
    customerInfoList = orderInfoList[-4:]

    print('\nOrder Details:')
    print('orderFileName = ', end='')
    print("'"+orderFileName+"'")
    print('orderInfoList = ', end='')
    print(orderInfoList)
    print('foodInfoList = ', end='')
    print(foodInfoList)
    print('restaurantInfoList = ', end='')
    print(restaurantInfoList)
    print('customerInfoList = ', end='')
    print(customerInfoList)

    masterOrderList = dataProcessing.genMasterOrderList(orderInfoList, restaurantInfoList[0], orderFileName, tag)
    masterFoodList = dataProcessing.genMasterFoodList(orderInfoList[0], restaurantInfoList[0], foodInfoList, orderFileName, tag)
    print('masterOrderList = ', end='')
    print(masterOrderList)
    print('masterFoodList = ', end='')
    print(masterFoodList)
    pushTo = 'master'
    print("Pushing data to master csv...")
    dataProcessing.pushToCsv(pushTo, masterOrderList, masterFoodList)
"""