#!python3

import csv, io
import globalParam
from datetime import datetime, timedelta
from contextlib import redirect_stdout

def printCommonInfo(orderNum, kedai, masterFoodList, totalPack, rider, payToShop):
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

    #print(f"Jumlah Pek: {totalPack}")
    print(f"Rider: {rider}")
    print(f"Bayar kpd {kedai}: RM{payToShop:.2f}")

    return

def genTextMsg(masterOrderList, masterFoodList, orderNum, rider):
    orderID = masterOrderList[0]
    deliveryTime = masterOrderList[1]
    orderTime = masterOrderList[2]
    kedai = masterOrderList[3]
    customerName = masterOrderList[4]
    customerPhone = masterOrderList[5]
    customerEmail = masterOrderList[6]
    customerAddress = masterOrderList[7]
    totalPack = masterOrderList[9]
    chargeType = masterOrderList[10]
    totalFoodPrice = masterOrderList[11]
    deliveryCharge = masterOrderList[12]
    colectFromCustomer = masterOrderList[13]
    chargeToShop = masterOrderList[14]
    payToShop = masterOrderList[15]

    #calculate pick time
    deliveryTimeObj = datetime.strptime(deliveryTime, globalParam.incomingDateFormat)
    deliveryTime = deliveryTimeObj.strftime('%I:%M %p (%d %b, %Y)')
    pickupTimeObj = deliveryTimeObj - timedelta(minutes=globalParam.pickupToDeliveryGap)
    pickupTime = pickupTimeObj.strftime('%I:%M %p (%d %b, %Y)')

    with io.StringIO() as buf, redirect_stdout(buf):
        #print("============== Message to Rider =================")
        printCommonInfo(orderNum, kedai, masterFoodList, totalPack, rider, payToShop)
        print("---------------------------------------------")
        print(f"Delivery Time: {deliveryTime}")
        print(f"Customer: {customerName}")
        print(f"Phone no: {customerPhone}")
        print(f"Address: {customerAddress}")
        print(f"Cas Penghantaran: RM{deliveryCharge:.2f}")
        print(f"Collect dari Customer: RMRM{colectFromCustomer:.2f}")
        print(f"OrderID: {orderID}")
        msgToRider = buf.getvalue()
    with io.StringIO() as buf, redirect_stdout(buf):
        #print("============== Message to Kedai =================")
        printCommonInfo(orderNum, kedai, masterFoodList, totalPack, rider, payToShop)
        print(f"Pick-up time: {pickupTime}")
        print(f"OrderID: {orderID}")
        msgToKedai = buf.getvalue()

    return msgToRider, msgToKedai

"""
masterOrderList=['1899955', '03/01/2019 8:30 PM', '03/01/2019 6:33 PM', "Nan's Kitchen", 'Nizam Zain', '0135104516', 'nizamdiha@gmail.com', '18 Lorong Limonia 3  Bertam LAKESIDE ', "1x Nasi Goreng Cina; 1x Nasi Goreng Daging; 1x Nan's Special", 3, 1, 23.5, 4.0, 27.5, 0.0, 23.5, 'new_order_04012019.022721.html.txt', '']
masterFoodList=[['1899955', "Nan's Kitchen", 'Nasi Goreng Cina', '6.50', '1', ' ', 'new_order_04012019.022721.html.txt', ''], ['1899955', "Nan's Kitchen", 'Nasi Goreng Daging', '7.00', '1', ' ', 'new_order_04012019.022721.html.txt', ''], ['1899955', "Nan's Kitchen", "Nan's Special", '10.00', '1', ' ', 'new_order_04012019.022721.html.txt', '']]

#masterOrderList=['1898054.1', '02/01/2019 12:30 PM', '02/01/2019 11:10 AM', "HippoFood (Nan's Kitchen)", 'nurul nadiah azmi', '01114430036', 'yon.paan@yahoo.com', 'no 55 g jalan dagangan 10 no 5 g', '1x Nasi Ayam Kunyit (NK)', 1, 2, 7.0, 0.0, 7.0, 2.0, 5.0, 'new_order_04012019.022700.html.txt', '']
#masterFoodList=[['1898054.1', "HippoFood (Nan's Kitchen)", 'Nasi Ayam Kunyit (NK)', '7.00', '1', ' ', 'new_order_04012019.022700.html.txt', '']]

#masterOrderList=['1899992', '03/01/2019 8:50 PM', '03/01/2019 7:48 PM', 'Char Koay Teow CIMB', 'Ayu  Halim', '0125550186', 'ayupali8684@gmail.com', '1728 Kepala Batas', '2x Char Koay Teow Biasa', 2, 3, 11.0, 4.0, 15.0, 1.0, 10.0, 'new_order_04012019.022731.html.txt', '']
#masterFoodList=[['1899992', 'Char Koay Teow CIMB', 'Char Koay Teow Biasa', '5.50', '2', ' ', 'new_order_04012019.022731.html.txt', '']]

#masterOrderList=['1899890', '03/01/2019 2:25 PM', '03/01/2019 1:22 PM', 'Anjung Satay', 'Rozana Abd Rahim', '0134325494', 'rozana_ummizaim@yahoo.com', 'Jalan Perak, 13200 Kepala Batas 1', '2x Mee Tulang; 2x Nasi Daging', 4, 1, 28.0, 4.0, 32.0, 0.0, 28.0, 'new_order_04012019.022714.html.txt', '']
#masterFoodList=[['1899890', 'Anjung Satay', 'Mee Tulang', '7.00', '2', ' ', 'new_order_04012019.022714.html.txt', ''], ['1899890', 'Anjung Satay', 'Nasi Daging', '7.00', '2', ' ', 'new_order_04012019.022714.html.txt', '']]

orderNum = 1
rider = '?'

msgToRider, msgToKedai = genTextMsg(masterOrderList, masterFoodList, orderNum, rider)
print(msgToRider)
print(msgToKedai)
"""