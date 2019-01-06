import sys

argList = str(sys.argv)
print(argList)

if 'updatecsv' in argList:
    #Push to csv
    print("Pushing data to csv...")
    #dataProcessing.pushToCsv(masterOrderList, masterFoodList)

if 'sendmsg' in argList:
    #generate Text Msg
    print("Generating text messages...")
    #msgToRider, msgToKedai = msgGenerator.genTextMsg(masterOrderList, masterFoodList, orderNum=1, rider='?')
    print("Sending test messages...")
    #print(msgToRider)
    #print(msgToKedai)