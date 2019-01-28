#!python3

# goto https://myaccount.google.com/lesssecureapps, turn on less secure app access
import imaplib
import time
import sys
import getpass
import os
from datetime import datetime, timedelta

import global_param
import data_processing
import data_extraction
import email_scraper


def clear_screen():
    os.system('cls')
    return


def email_login(server_name, username, folder):
    while True:
        print('\nUsername: ' + username)
        password = getpass.getpass("Press [Enter] to change Username or enter password now: ")
        if password == '':
            username = input("Username: ")
        else:
            break
    # login to email account
    mail = imaplib.IMAP4_SSL(server_name)
    print('\nLogging into email account...')
    try:
        mail.login(global_param.username, password)
    except imaplib.IMAP4.error:
        print('[ERROR] Login error. Check your username or password!')
        exit()
    # select email folder
    status, messages = mail.select(folder)
    # check whether email folder exist
    if status != "OK":
        print('[ERROR] Email folder \"' + folder + '\" does not exist!')
        exit()
    return mail


def get_search_criteria():
    # select email search mode
    valid_options = [1, 2, 3, 4]
    search_mode = 0
    while search_mode not in valid_options:
        print('\nSelect email search mode:')
        print('  [1] Unread')
        print('  [2] Date: SINCE -> BEFORE')
        print('  [3] Date: Today (' + datetime.now().strftime('%d-%m-%y') + ')')
        print('  [4] Date: Yesterday (' + (datetime.now() - timedelta(days=1)).strftime('%d-%m-%y') + ')')
        print('  [5] From (not working yet)')
        search_mode = int(input('Search mode: '))
        if search_mode not in valid_options:
            print("ERROR: Invalid option.")

    if search_mode == 2:  # SINCE -> BEFORE
        # http://strftime.org/
        while True:  # stuck here until correct date format is obtained
            since_date = input('\nEnter SINCE date (dd-mm-yy): ')
            before_date = input('Enter BEFORE date (dd-mm-yy): ')
            try:
                since_date_obj = datetime.strptime(since_date, "%d-%m-%y")
                before_date_obj = datetime.strptime(before_date, "%d-%m-%y")
                break
            except Exception as e:
                print('ERROR: ' + str(e))

        # convert to date format understandable by imap module
        since = since_date_obj.strftime("%d-%b-%Y")
        before = before_date_obj.strftime("%d-%b-%Y")
        sender = None
    elif search_mode == 3:  # TODAY
        since = datetime.now().strftime('%d-%b-%Y')  # today
        before = (datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y')  # tomorrow
        sender = None
    elif search_mode == 4:  # YESTERDAY
        since = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')  # yesterday
        before = datetime.now().strftime('%d-%b-%Y')  # today
        sender = None
    else:
        since = None
        before = None
        sender = None

    search_criteria_list = [search_mode, since, before, sender]
    return search_criteria_list


def get_save_destination():
    save_destination_str = '0'
    destination = None
    while save_destination_str not in ['1', '2', '3']:
        print('Which database you want the result to go into? Choose using the number below.')
        save_destination_str = input("[1] Master, [2] Daily, [3] Unit Test. Your selection: ")
    if save_destination_str == '1':
        destination = 'master'
    elif save_destination_str == '2':
        destination = 'daily'
    elif save_destination_str == '3':
        destination = 'unit_test'
    else:
        print("ERROR in get_save_destination")
        exit()
    return destination


def get_save_info(arg_list):
    save_destination = 'unit_test'
    if 'automode' in arg_list:  # handling of data saving in automode
        save = 'autodatapush' in arg_list  # will return True if 'autodatapush' arg is specified
        if save:  # if user choose to save to database.
            # for automode, pushTo is determined by arg
            # for non-automode, pushTo is selected by user (few codes below)
            if 'updatecsvmaster' in arg_list:
                save_destination = 'master'
            elif 'updatecsvdaily' in arg_list:
                save_destination = 'daily'
            else:
                save_destination = 'unit_test'
    else:  # handling of data saving in non-automde
        save_str = input("\nSave Result to Database? [Enter] for Yes, [Other Key] for No: ")
        if save_str == '':
            save = True
            save_destination = get_save_destination()  # ask user which database to update
        else:  # user don't want to save to database
            print('Result not saved')
            save = False
    return [save, save_destination]


argList = sys.argv  # get list of arguments
if 'debug' in argList:
    print(argList)
for arg in argList:
    if arg not in global_param.valid_arg_list:
        print(f"ERROR: '{arg}' is not a valid argument!")
        print("List of valid arguments: ", end='')
        for valid_arg in global_param.valid_arg_list:
            print(valid_arg + ' ', end='')
        exit()

if 'debug' in argList:
    global_param.debug = True

mailObj = email_login(global_param.server_name, global_param.username, global_param.email_folder)
tag = input('Add tag OR hit [ENTER] for no tag: ')  # admin can add tag here (optional)
counter = 0  # counter var is used to ensure in get_search_criteria is called only ONCE in automde

while True:
    clear_screen()
    searchCriteriaList = [None]
    emailList = [None]
    if 'automode' in argList:
        if counter == 0:
            searchCriteriaList = get_search_criteria()
        counter += 1
    else:
        searchCriteriaList = get_search_criteria()

    searchMode = searchCriteriaList[0]
    sinceDate = searchCriteriaList[1]
    beforeDate = searchCriteriaList[2]
    senderEmail = searchCriteriaList[3]

    print('Searching for email...')
    emailList = email_scraper.get_new_email(mailObj, searchMode, sinceDate, beforeDate, senderEmail)

    if len(emailList) > 0:
        print(str(len(emailList)) + ' email(s) found')
        time.sleep(1)

        newOrderFileList = email_scraper.get_new_order(mailObj, emailList)

        if 'debug' in argList:
            print('newOrderFileList = ', end='')
            print(newOrderFileList)

        for orderFileName in newOrderFileList:
            # flatten the raw email to simplify regex search
            data_extraction.flatten_raw_email(orderFileName)

        masterDict = {}  # create an empty dict to store order info extracted from emails

        for orderFileName in newOrderFileList:
            # Extract order information from the flatten raw email
            if 'debug' in argList:
                print('\nOrder Details:')
                print('orderFileName = ', end='')
                print("'" + orderFileName + "'")

            numOfShop, megaOrderList = data_extraction.get_order_info(orderFileName)
            if 'debug' in argList:
                print('megaOrderList = ', end='')
                print(megaOrderList)

            for orderInfoList in megaOrderList:
                foodInfoList = orderInfoList[2]
                shopInfoList = data_extraction.get_shop_info(orderInfoList[4])
                print(shopInfoList)
                if shopInfoList[0] == 'no match':
                    print('ERROR: No matching restaurant found. Cannot proceed!')
                    exit()
                customerInfoList = orderInfoList[-4:]

                if 'debug' in argList:
                    print('orderInfoList = ', end='')
                    print(orderInfoList)
                    print('foodInfoList = ', end='')
                    print(foodInfoList)
                    print('shopInfoList = ', end='')
                    print(shopInfoList)
                    print('customerInfoList = ', end='')
                    print(customerInfoList)

                # Data Processing
                # TODO: <add app or webapp> tag = dataExtraction.get_order_tool(orderFileName)+';'+tag
                masterOrderList = data_processing.gen_master_order_list(orderInfoList, shopInfoList[0],
                                                                        orderFileName, tag)
                masterFoodList = data_processing.gen_master_food_list(orderInfoList[0], shopInfoList[0],
                                                                      foodInfoList, orderFileName, tag)
                print('masterOrderList = ', end='')
                print(masterOrderList)
                print('masterFoodList = ', end='')
                print(masterFoodList)

                # pack everything into masterDict
                orderID = masterOrderList[0]
                orderInfoDict = {'masterOrderList': masterOrderList, 'masterFoodList': masterFoodList}
                masterDict[orderID] = orderInfoDict

        if 'debug' in argList:
            print('masterDict = ', end='')
            print(masterDict)

        # up to this point, data extraction and processing are done and stored in masterDict
        # from this point onwards is all about saving data from masterDict to database
        saveInfoList = get_save_info(argList)
        saveBool = saveInfoList[0]
        saveDestination = saveInfoList[1]
        if saveBool:
            for orderID, orderInfoDict in masterDict.items():
                masterOrderList = orderInfoDict['masterOrderList']
                masterFoodList = orderInfoDict['masterFoodList']
                print(f"Pushing data for order {orderID} to {saveDestination} csv...")
                data_processing.push_to_csv(saveDestination, masterOrderList, masterFoodList)

    else:  # len(emailList==0)
        print('No email found')

    if 'automode' in argList:
        print('Next email check in ' + str(global_param.check_interval) + 'sec...')
        print('CTRL+C to stop loop\n')
        time.sleep(global_param.check_interval)
        continue

    # automode should never reach this point
    loop = input("\nSearch again? [Enter] for Yes, [Other Key] for No: ")

    if loop == '':
        pass
    else:
        print('Thanks You!')
        break
