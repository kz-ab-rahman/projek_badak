#!python3

import csv, io
import globalParam
from datetime import datetime, timedelta
from contextlib import redirect_stdout

def getChargeDetail(restaurantName):
    chargeList=[]
    with open(globalParam.restaurantDataFile, 'r') as file:
        next(file) #skip csv header
        reader = csv.reader(file)
        found = False
        for line in reader:
            result = restaurantName.find(line[1])
            if result != -1:
                chargeList = line[5:]
                found = True
                break
            else:
                pass
    if not found:
        chargeList = -1
    return chargeList

def printCommonInfo(kedai, orderNum, masterFoodList, rider, chargeType, chargeToShop):
    totalFoodPrice = 0
    totalFoodQuantity = 0
    header = f"\n\
HIPPO FOOD DELIVERY\n\
*Order No: {orderNum}*\n\
Nama Kedai: *{kedai}*\n\
Pesanan:"

    print(header)
    for num, foodItem in enumerate(masterFoodList):
        unitPrice = float(foodItem[3])
        quantity = int(foodItem[4])
        note = foodItem[5]
        if note == ' ':
            pass
        else:
            note = '(note:'+note+')'
        print(f"{num+1}. {foodItem[2]} (RM{unitPrice:.2f}) x {quantity} set {note}")
        totalPrice = unitPrice*quantity
        totalFoodQuantity+=quantity
        totalFoodPrice+=totalPrice
    #print(f"Jumlah Pek: {totalFoodQuantity}")
    if chargeType == 2:
        totalFoodPrice = totalFoodPrice - (chargeToShop*totalFoodQuantity)
    elif chargeType == 3:
        totalFoodPrice = totalFoodPrice - chargeToShop
    else:
        pass
    print(f"Rider: {rider}")
    print(f"Bayar kpd {kedai}: RM{totalFoodPrice:.2f}")

    return

def genTextMsg(masterOrderList, masterFoodList, orderNum, rider):
    kedai = masterOrderList[3]
    if kedai == 'no match':
        print('Could not find restaurant. Will not proceed')
        exit()
    orderID = masterOrderList[0]
    deliveryTime = masterOrderList[1]
    customerName = masterOrderList[4]
    customerPhone = masterOrderList[5]
    customerAddress = masterOrderList[7]
    chargeList = getChargeDetail(kedai)
    chargeType = int(chargeList[0])
    deliveryCharge = float(chargeList[-1])
    chargeToShop = float(chargeList[chargeType])
    #print(chargeType,chargeToShop,deliveryCharge)
    totalFoodPrice = 0

    #calculate total food price
    for foodItem in masterFoodList:
        totalPrice = float(foodItem[3])*int(foodItem[4]) #unitPrice x quantity
        totalFoodPrice+=totalPrice

    #calculate pick time (delivery time - 15min)
    deliveryTimeObj = datetime.strptime(deliveryTime, globalParam.incomingDateFormat)
    deliveryTime = deliveryTimeObj.strftime('%I:%M %p (%d %b, %Y)')
    pickupTimeObj = deliveryTimeObj - timedelta(minutes=globalParam.pickupToDeliveryGap)
    pickupTime = pickupTimeObj.strftime('%I:%M %p (%d %b, %Y)')

    with io.StringIO() as buf, redirect_stdout(buf):
        #print("============== Message to Rider =================")
        printCommonInfo(kedai, orderNum, masterFoodList, rider, chargeType, chargeToShop)
        print("---------------------------------------------")
        print(f"Delivery Time: {deliveryTime}")
        print(f"Customer: {customerName}")
        print(f"Phone no: {customerPhone}")
        print(f"Address: {customerAddress}")
        print(f"Cas Penghantaran: RM{deliveryCharge:.2f}")
        print(f"Collect dari Customer: RM{(totalFoodPrice+deliveryCharge):.2f}")
        print(f"OrderID: {orderID}")
        msgToRider = buf.getvalue()
    with io.StringIO() as buf, redirect_stdout(buf):
        #print("============== Message to Kedai =================")
        printCommonInfo(kedai, orderNum, masterFoodList, rider, chargeType, chargeToShop)
        print(f"Pick-up time: {pickupTime}")
        print(f"OrderID: {orderID}")
        msgToKedai = buf.getvalue()

    return msgToRider, msgToKedai

"""
masterOrderList = ['1848178', '12/10/2018 12:30 PM', '12/10/2018 7:10 AM', 'Dinis Café', 'Mohd Afzanizam  Mohd Zain', '0135104516', 'nizamdiha@gmail.com', '18 Lorong Limonia 3  Bertam LAKESIDE ', '1x Mee Goreng; 1x Nasi Goreng Pataya Ayam Goreng; 1x Nasi Tomato Ayam Masak Merah', 'new_order_28122018.024154.html.txt', 'cuti sekolah']
masterFoodList = [['1848178', 'Dinis Café', 'Mee Goreng', '4.00', '1', ' ', 'new_order_28122018.024154.html.txt', 'cuti sekolah'], ['1848178', 'Dinis Café', 'Nasi Goreng Pataya Ayam Goreng', '5.00', '1', ' ', 'new_order_28122018.024154.html.txt', 'cuti sekolah'], ['1848178', 'Dinis Café', 'Nasi Tomato Ayam Masak Merah', '4.50', '1', ' ', 'new_order_28122018.024154.html.txt', 'cuti sekolah']]

#masterOrderList = ['1865177', '12/18/2018 12:00 PM', '12/17/2018 1:47 PM', 'Mangkuk Tingkat', 'Ida Ismail', '0143696487', 'idashazrina@gmail.com', 'No 19 Lorong Limonia 1 Bertam Perdana 2 ', '2x Set Asam Pedas; 2x Set Ayam Madu', 'new_order_28122018.023820.html.txt', 'cuti sekolah']
#masterFoodList = [['1865177', 'Mangkuk Tingkat', 'Set Asam Pedas', '6.00', '2', ' ', 'new_order_28122018.023820.html.txt', 'cuti sekolah'], ['1865177', 'Mangkuk Tingkat', 'Set Ayam Madu', '6.00', '2', ' ', 'new_order_28122018.023820.html.txt', 'cuti sekolah']]

#masterOrderList = ['1881365', '12/24/2018 8:30 PM', '12/24/2018 7:00 PM', 'Char Koay Teow CIMB', 'am mohd borkhan', '01140394377', 'amgrey8889@gmail.com', 'no 54,lorong 1.taman air tawar indah.teluk air tawar ', '1x Char Koay Teow Special; 1x Char Koay Teow Biasa', 'new_order_28122018.023417.html.txt', 'cuti sekolah']
#masterFoodList = [['1881365', 'Char Koay Teow CIMB', 'Char Koay Teow Special', '7.50', '1', ' ', 'new_order_28122018.023417.html.txt', 'cuti sekolah'], ['1881365', 'Char Koay Teow CIMB', 'Char Koay Teow Biasa', '5.50', '1', ' ', 'new_order_28122018.023417.html.txt', 'cuti sekolah']]

#masterOrderList = ['1848214', '12/11/2018 12:30 PM', '12/10/2018 4:52 PM', 'Arango Park', 'Nur Syuhadah', '0125814410', 'syu3010@gmail.com', 'no 1 lorong limonia 2 No 1 Lorong Limonia 2 ', '1x Lasagna Cheezo', 'new_order_28122018.024159.html.txt', 'cuti sekolah']
#masterFoodList = [['1848214', 'Arango Park', 'Lasagna Cheezo', '12.90', '1', 'Tak Mau Chees', 'new_order_28122018.024159.html.txt', 'cuti sekolah']]

orderNum = 1
rider = '?'

msgToRider, msgToKedai = genTextMsg(masterOrderList, masterFoodList, orderNum, rider)
print(msgToRider)
print(msgToKedai)
"""