#!python3

import re, linecache, csv
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
        #print('foodInfoList: ')
        #print(foodInfoList, len(foodInfoList))

        for i, rawFood in enumerate(foodInfoList):
            #print(i, rawFood)
            foodMatch = re.search(regexStringFood, rawFood)
            if foodMatch:
                food = foodMatch.group(1)
                unitPrice = foodMatch.group(2)
                #option = foodMatch.group()
                quantity = foodMatch.group(3)
                note = foodMatch.group(4)
            else:
                food = 'no match'
                unitPrice = 'no match'
                #option = 'no match'
                quantity = 'no match'
                note = 'no match'
            #foodInfoList[i]=[food,unitPrice,quantity,option,note]
            matchFoodInBracket = re.search(r".*\((.*(?:Nasi|Mee|Keow|Bihun).*)\)", food) #will match if the food is in ()
            if matchFoodInBracket:
                food = matchFoodInBracket.group(1) #take the food inside the bracket
            foodInfoList[i]=[food,unitPrice,quantity,note]

        orderInfoList[2] = foodInfoList
    else:
        orderInfoList=['no match']*9

    return orderInfoList

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
        restaurantInfoList = ['no match', 'no match', 'no match', 'no match']
    return restaurantInfoList

"""
orderFileName = 'new_order_28122018.022522.html.txt'
flattenRawEmail(orderFileName)
orderInfoList = getOrderInfo(orderFileName)
foodInfoList = orderInfoList[2]
restaurantInfoList = getRestaurantInfo(orderInfoList[4])
customerInfoList = orderInfoList[-4:]

print('FINAL OUTPUT:')
print(orderInfoList)
print(foodInfoList)
print(restaurantInfoList)
print(customerInfoList)
"""