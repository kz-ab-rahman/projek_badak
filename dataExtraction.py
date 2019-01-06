#!python3

import re, linecache, csv, copy
import globalParam

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
    line = linecache.getline(globalParam.rawEmailPath+orderFileName, 1)
    #https://regex101.com/
    regexInOrder = 'Number: <\/strong>\s?([^<]+).*Place Time: <\/strong>\s?([^<]+)<\/p><hr(?: \/|><p)>(.*)(?:Tax Total|Delivery (?:Charge|Fee)).*Created on :<\/strong> ([^<]+)<\/p><p>([^<]+).*Information :<\/strong><\/p><p>(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>(.*)<br(?: \/)?>'
    regexInFood = 'Details<\/strong> : (.+)\s\((?:RM)?([^)]+).*Qty<\/strong> : ([^<]+).*Notes <\/strong>:\s?([^<]+)'
    regexStringOrder = re.compile(regexInOrder)
    regexStringFood = re.compile(regexInFood)

    match = re.search(regexStringOrder, line)
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
        restaurantInfoList = addRestaurant()
    return restaurantInfoList

"""
orderFileName = 'new_order_03012019.094058.html.txt'
#flattenRawEmail(orderFileName)
numOfKedai, megaOrderList = getOrderInfo(orderFileName)
print('\nOrder Details for '+orderFileName+': ')
for orderInfoList in megaOrderList:
    foodInfoList = orderInfoList[2]
    restaurantInfoList = getRestaurantInfo(orderInfoList[4])
    customerInfoList = orderInfoList[-4:]

    print('orderInfoList:')
    print(orderInfoList)
    print('foodInfoList:')
    print(foodInfoList)
    print('restaurantInfoList:')
    print(restaurantInfoList)
    print('customerInfoList:')
    print(customerInfoList)
"""