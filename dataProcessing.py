#!python3
import csv
import globalParam

def genMasterOrderList(orderInfoList, restaurantName, orderFileName, tag):
    foodListStr=''
    dummyList=orderInfoList.copy()
    #create summary of food order to be included in master order list
    for i, item in enumerate(dummyList[2]):
        #print(item)
        food=item[0]
        qty=item[2]
        #print(food,qty)
        if i > 0:
            spacer='; '
        else:
            spacer=''
        foodListStr+=spacer+qty+'x '+food

    del dummyList[2] #delete food list from master list. replace with summary
    dummyList[3] = restaurantName
    masterOrderList = dummyList
    masterOrderList.extend([foodListStr,orderFileName,tag]) #append food summary, rawdata, tag
    return masterOrderList

def genMasterFoodList(orderID, restaurant, foodInfoList, orderFileName, tag):
    dummyList=foodInfoList.copy()
    for item in dummyList:
        item.insert(0,orderID)
        item.insert(1,restaurant)
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

"""
orderInfoList = ['1885157', '12/27/2018 8:45 PM', [['Satay Daging', '9.00', '1', ' '], ['Bihun Sup Tulang', '6.00', '1', 'Takmau Sayur, Cabai Dll.. Hanya Bihun Kosong Dgn Sup.. Untuk Budak Makan']], '12/27/2018 7:43 PM', 'Anjung Satay  Jalan Dagangan 3, 13200 Kepala Batas, Pulau Pinang, Malaysia', 'Radzi Rosidi', '0125812648', 'lekiu9900@gmail.com', 'no. 17, persiaran seksyen 2/4 ']
foodInfoList = [['Satay Daging', '9.00', '1', ' '], ['Bihun Sup Tulang', '6.00', '1', 'Takmau Sayur, Cabai Dll.. Hanya Bihun Kosong Dgn Sup.. Untuk Budak Makan']]
restaurantInfoList = ['Anjung Satay', 'Jalan Dagangan 3, 13200 Kepala Batas, Pulau Pinang, Malaysia', 'none', '60174408013']
customerInfoList = ['Radzi Rosidi', '0125812648', 'lekiu9900@gmail.com', 'no. 17, persiaran seksyen 2/4 ']
orderFileName = 'new_order_28122018.022522.html.txt'
tag=''

masterOrderList = genMasterOrderList(orderInfoList, restaurantInfoList[0], orderFileName, tag)
masterFoodList = genMasterFoodList(orderInfoList[0], restaurantInfoList[0], foodInfoList, orderFileName, tag)
print(masterOrderList)
print(masterFoodList)
#pushToCsv(masterOrderList,masterFoodList)
"""
