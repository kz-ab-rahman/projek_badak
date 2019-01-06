#!python3


#goto https://myaccount.google.com/lesssecureapps, turn on less secure app access
import imaplib, time, re, linecache, sys, getpass, msvcrt
import globalParam, dataProcessing, dataExtraction, emailScraper, msgGenerator

argList = str(sys.argv)

usernm = 'hippofooddelivery@gmail.com'
serverName = 'imap.gmail.com'
emailFolder = 'Inbox'
checkInterval = 10 #seconds

while True:
    print('\nUsername: '+'\x1b[6;30;42m'+usernm+'\x1b[0m')
    passwd = getpass.getpass("Enter password or hit [ENTER] to change Username: ")
    if passwd == '':
        usernm = input("Username: ")
    else:
        break

#login to email account
mail = imaplib.IMAP4_SSL(serverName)
print('\nLogging into email account...')
try:
    mail.login(usernm,passwd)
except:
    print('[ERROR] Invalid credientials!')
    exit()

#select email folder
status, messages = mail.select(emailFolder)
#check whether email folder exist
if status != "OK":
    print('[ERROR] Email folder \"'+emailFolder+'\" does not exist!')
    exit()

#admin can add tag here
tag = input('Add tag OR hit [ENTER] for no tag: ')
print('\n')

#MAIN LOOP starts here
while True:
    newEmail = False
    while newEmail == False: #will loop here until new email available
        print('Checking for new email...')
        emailList = emailScraper.getNewEmail(mail)
        if len(emailList) > 0:
            newEmail = True
            print(str(len(emailList)) + ' new email(s)')
        else:
            print('No new email. Next email check in ' + str(checkInterval) +'sec...')
            print('CTRL+C to stop automation\n')
            time.sleep(checkInterval)

    newOrderFileList = emailScraper.getNewOrder(mail,emailList)
    #print(newOrderFileList)
    newOrderNum = len(newOrderFileList)
    for num, orderFileName in enumerate(newOrderFileList):
        #flatten the raw email to simplify regex search
        dataExtraction.flattenRawEmail(orderFileName)
    for orderFileName in newOrderFileList:
        #Extract order information from the flatten raw email
        numOfKedai, megaOrderList = dataExtraction.getOrderInfo(orderFileName)
        for orderInfoList in megaOrderList:
            foodInfoList = orderInfoList[2]
            restaurantInfoList = dataExtraction.getRestaurantInfo(orderInfoList[4])
            if restaurantInfoList[0] == 'no match':
                print('No matching restaurant found. Cannot proceed!')
                exit()
            customerInfoList = orderInfoList[-4:]
            """
            print('\nOrder Details for '+orderFileName+': ')
            print('orderInfoList:')
            print(orderInfoList)
            print('foodInfoList:')
            print(foodInfoList)
            print('restaurantInfoList:')
            print(restaurantInfoList)
            print('customerInfoList:')
            print(customerInfoList)
            """
            #Data Processing
            masterOrderList = dataProcessing.genMasterOrderList(orderInfoList, restaurantInfoList[0], orderFileName, tag)
            masterFoodList = dataProcessing.genMasterFoodList(orderInfoList[0], restaurantInfoList[0], foodInfoList, orderFileName, tag)
            print('masterOrderList:')
            print(masterOrderList)
            print('masterFoodList:')
            print(masterFoodList)

            if 'updatecsv' in argList:
                #Push to csv
                print("Pushing data to csv...")
                dataProcessing.pushToCsv(masterOrderList, masterFoodList)

            if 'sendmsg' in argList:
                #generate Text Msg
                print("Generating text messages...")
                msgToRider, msgToKedai = msgGenerator.genTextMsg(masterOrderList, masterFoodList, orderNum=1, rider='?')
                print("Sending test messages...")
                print(msgToRider)
                print(msgToKedai)

    print('\nNew order successfully added. Next email check in ' + str(checkInterval) +'sec...')
    print('CTRL+C to stop automation\n')
    time.sleep(checkInterval)






