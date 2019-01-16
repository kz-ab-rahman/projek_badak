#!python3

#goto https://myaccount.google.com/lesssecureapps, turn on less secure app access
import imaplib, time, sys, getpass, msvcrt
from datetime import datetime, timedelta
import globalParam, dataProcessing, dataExtraction, emailScraper, msgGenerator

argList = sys.argv
#print(argList)
for arg in argList:
    if arg not in globalParam.validArgList:
        print(f"ERROR: '{arg}' is not a valid argument!")
        print("List of valid arguments: ",end='')
        for validArg in globalParam.validArgList:
            print(validArg+' ', end='')
        exit()

while True:
    print('\nUsername: '+'\x1b[6;30;42m'+globalParam.usernm+'\x1b[0m')
    passwd = getpass.getpass("Enter password or hit [ENTER] to change Username: ")
    if passwd == '':
        globalParam.usernm = input("Username: ")
    else:
        break

#login to email account
mail = imaplib.IMAP4_SSL(globalParam.serverName)
print('\nLogging into email account...')
try:
    mail.login(globalParam.usernm,passwd)
except:
    print('[ERROR] Invalid credientials!')
    exit()

#select email folder
status, messages = mail.select(globalParam.emailFolder)
#check whether email folder exist
if status != "OK":
    print('[ERROR] Email folder \"'+globalParam.emailFolder+'\" does not exist!')
    exit()

#admin can add tag here
tag = input('Add tag OR hit [ENTER] for no tag: ')

#select email search mode
validOptions = [1,2,3,4]
searchMode = 0
while searchMode not in validOptions:
    print('\nSelect email search mode:')
    print('  [1] Unread')
    print('  [2] Date: SINCE -> BEFORE')
    print('  [3] Date: Today ('+datetime.now().strftime('%d-%m-%y')+')')
    print('  [4] Date: Yesterday ('+(datetime.now() - timedelta(days=1)).strftime('%d-%m-%y')+')')
    print('  [5] From (not working yet)')
    searchMode = int(input('Search mode: '))
    if searchMode not in validOptions:
        print("ERROR: Invalid option.")

if searchMode == 2: #SINCE -> BEFORE
    #http://strftime.org/
    while True: #stuck here until correct date format is obtained
        sinceDate = input('\nEnter SINCE date (dd-mm-yy): ')
        beforeDate = input('Enter BEFORE date (dd-mm-yy): ')
        try:
            sinceDateObj = datetime.strptime(sinceDate, "%d-%m-%y")
            beforeDateObj = datetime.strptime(beforeDate, "%d-%m-%y")
            break
        except Exception as e:
            print('ERROR: '+str(e))

    #convert to date format understandable by imap module
    since = sinceDateObj.strftime("%d-%b-%Y")
    before = beforeDateObj.strftime("%d-%b-%Y")

elif searchMode == 3: #TODAY
    since = datetime.now().strftime('%d-%b-%Y') #today
    before = (datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y') #tomorrow

elif searchMode == 4: #YESTERDAY
    since = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y') #yesterday
    before = datetime.now().strftime('%d-%b-%Y') #today

else:
    since = 0
    before = 0

#MAIN LOOP starts here
if 'runloop' in argList:
    runLoop = True
else:
    runLoop = False

while True:
    foundEmail = False
    while not foundEmail: #will loop here until email with selected criteria is found
        print('Searching for email...')
        emailList = emailScraper.getNewEmail(mail, searchMode, since, before)
        if len(emailList) > 0:
            foundEmail = True
            print(str(len(emailList)) + ' email(s) found')
        else:
            print('No email found')
            if runLoop:
                print('Next email check in ' + str(globalParam.checkInterval) +'sec...')
                print('CTRL+C to stop loop\n')
                time.sleep(globalParam.checkInterval)
            else:
                break

    newOrderFileList = emailScraper.getNewOrder(mail,emailList)

    if 'debug' in argList:
        print('newOrderFileList = ', end='')
        print(newOrderFileList)

    for orderFileName in newOrderFileList:
        #flatten the raw email to simplify regex search
        dataExtraction.flattenRawEmail(orderFileName)

    for orderFileName in newOrderFileList:
        #Extract order information from the flatten raw email
        if 'debug' in argList:
            print('\nOrder Details:')
            print('orderFileName = ', end='')
            print("'"+orderFileName+"'")

        numOfKedai, megaOrderList = dataExtraction.getOrderInfo(orderFileName)
        if 'debug' in argList:
            print('megaOrderList = ',end='')
            print(megaOrderList)

        for orderInfoList in megaOrderList:
            foodInfoList = orderInfoList[2]
            restaurantInfoList = dataExtraction.getRestaurantInfo(orderInfoList[4])
            print(restaurantInfoList)
            if restaurantInfoList[0] == 'no match':
                print('ERROR: No matching restaurant found. Cannot proceed!')
                exit()
            customerInfoList = orderInfoList[-4:]

            if 'debug' in argList:
                print('orderInfoList = ', end='')
                print(orderInfoList)
                print('foodInfoList = ', end='')
                print(foodInfoList)
                print('restaurantInfoList = ', end='')
                print(restaurantInfoList)
                print('customerInfoList = ', end='')
                print(customerInfoList)

            #Data Processing
            #TODO: <add app or webapp> tag = dataExtraction.getOrderTool(orderFileName)+';'+tag
            masterOrderList = dataProcessing.genMasterOrderList(orderInfoList, restaurantInfoList[0], orderFileName, tag)
            masterFoodList = dataProcessing.genMasterFoodList(orderInfoList[0], restaurantInfoList[0], foodInfoList, orderFileName, tag)
            print('masterOrderList = ', end='')
            print(masterOrderList)
            print('masterFoodList = ', end='')
            print(masterFoodList)

            if 'updatecsvmaster' in argList:
                pushTo = 'master'
                print("Pushing data to master csv...")
                dataProcessing.pushToCsv(pushTo, masterOrderList, masterFoodList)

            if 'updatecsvdaily' in argList:
                pushTo = 'daily'
                print("Pushing data to daily csv...")
                dataProcessing.pushToCsv(pushTo, masterOrderList, masterFoodList)

            if 'genmsg' in argList:
                print("Generating text messages...")
                msgToRider, msgToKedai = msgGenerator.genTextMsg(masterOrderList, masterFoodList, orderNum=1, rider='?')
                print(msgToRider)
                print(msgToKedai)

    if foundEmail:
        print('\nNew order successfully added')
    if runLoop:
        print('Next email check in ' + str(globalParam.checkInterval) +'sec...')
        print('CTRL+C to stop loop\n')
        time.sleep(globalParam.checkInterval)
    else:
        break






