#!python3

# goto https://myaccount.google.com/lesssecureapps, turn on less secure app access
import imaplib
import time
import sys
import getpass
from datetime import datetime, timedelta

import global_param
import data_processing
import data_extraction
import email_scraper
import msg_generator

arg_list = sys.argv
# print(arg_list)
for arg in arg_list:
    if arg not in global_param.valid_arg_list:
        print(f"ERROR: '{arg}' is not a valid argument!")
        print("List of valid arguments: ", end='')
        for valid_arg in global_param.valid_arg_list:
            print(valid_arg + ' ', end='')
        exit()

while True:
    print('\nUsername: ' + global_param.username)
    password = getpass.getpass("Press [Enter] to change Username or enter password now: ")
    if password == '':
        global_param.username = input("Username: ")
    else:
        break

# login to email account
mail = imaplib.IMAP4_SSL(global_param.server_name)
print('\nLogging into email account...')
try:
    mail.login(global_param.username, password)
except imaplib.IMAP4.error:
    print('[ERROR] Login error. Check your username or password!')
    exit()

# select email folder
status, messages = mail.select(global_param.email_folder)
# check whether email folder exist
if status != "OK":
    print('[ERROR] Email folder \"' + global_param.email_folder + '\" does not exist!')
    exit()

# admin can add tag here
tag = input('Add tag OR hit [ENTER] for no tag: ')

# select email search mode
valid_options = [1, 2, 3, 4]
search_mode = 0
while search_mode not in valid_options:
    print('\nSelect email search mode:')
    print('  [1] Unread')
    print('  [2] Date: SINCE -> BEFORE')
    print('  [3] Date: Today ('+datetime.now().strftime('%d-%m-%y')+')')
    print('  [4] Date: Yesterday ('+(datetime.now() - timedelta(days=1)).strftime('%d-%m-%y')+')')
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
            print('ERROR: '+str(e))

    # convert to date format understandable by imap module
    since = since_date_obj.strftime("%d-%b-%Y")
    before = before_date_obj.strftime("%d-%b-%Y")

elif search_mode == 3:  # TODAY
    since = datetime.now().strftime('%d-%b-%Y')  # today
    before = (datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y')  # tomorrow

elif search_mode == 4:  # YESTERDAY
    since = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')  # yesterday
    before = datetime.now().strftime('%d-%b-%Y')  # today

else:
    since = 0
    before = 0

# MAIN LOOP starts here
if 'runloop' in arg_list:
    run_loop = True
else:
    run_loop = False

while True:
    # TODO: move the search mode selection into this loop so user can search again without re-login
    found_email = False
    email_list = [None]
    while not found_email:  # will loop here until email with selected criteria is found
        print('Searching for email...')
        email_list = email_scraper.get_new_email(mail, search_mode, since, before)
        if len(email_list) > 0:
            found_email = True
            print(str(len(email_list)) + ' email(s) found')
        else:
            print('No email found')
            if run_loop:
                print('Next email check in ' + str(global_param.check_interval) + 'sec...')
                print('CTRL+C to stop loop\n')
                time.sleep(global_param.check_interval)
            else:
                break

    new_order_file_list = email_scraper.get_new_order(mail, email_list)

    if 'debug' in arg_list:
        print('newOrderFileList = ', end='')
        print(new_order_file_list)

    for order_file_name in new_order_file_list:
        # flatten the raw email to simplify regex search
        data_extraction.flatten_raw_email(order_file_name)

    for order_file_name in new_order_file_list:
        # Extract order information from the flatten raw email
        if 'debug' in arg_list:
            print('\nOrder Details:')
            print('orderFileName = ', end='')
            print("'" + order_file_name + "'")

        num_of_shop, mega_order_list = data_extraction.get_order_info(order_file_name)
        if 'debug' in arg_list:
            print('megaOrderList = ', end='')
            print(mega_order_list)

        for order_info_list in mega_order_list:
            food_info_list = order_info_list[2]
            restaurant_info_list = data_extraction.get_shop_info(order_info_list[4])
            print(restaurant_info_list)
            if restaurant_info_list[0] == 'no match':
                print('ERROR: No matching restaurant found. Cannot proceed!')
                exit()
            customer_info_list = order_info_list[-4:]

            if 'debug' in arg_list:
                print('orderInfoList = ', end='')
                print(order_info_list)
                print('foodInfoList = ', end='')
                print(food_info_list)
                print('shopInfoList = ', end='')
                print(restaurant_info_list)
                print('customerInfoList = ', end='')
                print(customer_info_list)

            # Data Processing
            # TODO: <add app or webapp> tag = dataExtraction.get_order_tool(orderFileName)+';'+tag
            master_order_list = data_processing.gen_master_order_list(order_info_list, restaurant_info_list[0],
                                                                      order_file_name, tag)
            master_food_list = data_processing.gen_master_food_list(order_info_list[0], restaurant_info_list[0],
                                                                    food_info_list, order_file_name, tag)
            print('masterOrderList = ', end='')
            print(master_order_list)
            print('masterFoodList = ', end='')
            print(master_food_list)

            # TODO: ask user whether to update database or not
            if 'updatecsvmaster' in arg_list:
                pushTo = 'master'
            elif 'updatecsvdaily' in arg_list:
                pushTo = 'daily'
            else:
                pushTo = 'unit_test'

            print(f"Pushing data to {pushTo} csv...")
            data_processing.push_to_csv(pushTo, master_order_list, master_food_list)

            if 'genmsg' in arg_list:
                print("Generating text messages...")
                orderNum = 1
                rider = '?'
                msg_to_rider, msg_to_shop = msg_generator.gen_text_msg(master_order_list, master_food_list,
                                                                       orderNum, rider)
                print(msg_to_rider)
                print(msg_to_shop)

    if found_email:
        print('\nNew order successfully added')
    if run_loop:
        print('Next email check in ' + str(global_param.check_interval) + 'sec...')
        print('CTRL+C to stop loop\n')
        time.sleep(global_param.check_interval)
    else:
        break
