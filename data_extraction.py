#!python3

import re
import linecache
import csv
import copy
import global_param
import data_processing


def get_order_tool(order_file_name):
    if order_file_name.find('type0') != -1:
        return 'app'
    elif order_file_name.find('type1') != -1:
        return 'web'
    else:
        return 'fastfood'


def flatten_raw_email(order_file_name):
    with open(global_param.raw_email_path + order_file_name, 'r+') as file:
        current_line = ''
        for line in file:
            line = line.strip('\n')
            line = line.replace('=', '')
            current_line = current_line + line
        # print(current_line)
        file.seek(0)
        file.write(current_line)
        file.truncate()
    return


def get_order_info(order_file_name):
    # print("inside getOrderInfo")
    line = linecache.getline(global_param.raw_email_path+order_file_name, 1)
    regex_string_order = re.compile(global_param.regex_in_order)
    regex_string_food = re.compile(global_param.regex_in_food)

    match = re.search(regex_string_order, line)
    # print(match)
    if match:
        order_info_list = list(match.groups())
        # print('order_info_list[2]: '+order_info_list[2])
        # add || delimiter to identify different food
        food_info = order_info_list[2].replace('</p><p><strong>Details', '</p>||<p><strong>Details')
        # print('food_info: '+food_info)
        food_info_list = food_info.split('||')  # split the multiple food into list
        keys = []
        for i, rawFood in enumerate(food_info_list):
            # print(i, rawFood)
            food_match = re.search(regex_string_food, rawFood)
            if food_match:
                food = food_match.group(1)
                unit_price = food_match.group(2)
                # option = food_match.group()
                quantity = food_match.group(3)
                note = food_match.group(4)

                match = re.search(global_param.regex_in_food_in_bracket, food)  # will match if the food is in ()
                if match:
                    food = match.group(1)  # take the food inside the bracket
                match = re.search(r"[\w+\s]+\(([A-Z]{2})\)", food)  # <word><space>(shop key)
                if match:
                    key = match.group(1)  # take the shop key
                    keys.append(key)
            else:
                food = 'no match'
                unit_price = 'no match'
                # option = 'no match'
                quantity = 'no match'
                note = 'no match'
            food_info_list[i] = [food, unit_price, quantity, note]

        order_info_list[2] = food_info_list

        # handling for multiple shop in 1 order for nasi ekonomi Hippo Food
        unique_key = list(set(keys))  # remove duplicate key in keys[]
        # print(unique_key)
        hippo_shop = len(unique_key)  # num of shop = number of item unique_key
        if hippo_shop > 1:  # if 0: not hippofood
                            # if 1: hippofood from 1 shop only. we process only if hippofood shop > 1
            # print('num of shop HippoFood: '+str(hippo_shop))
            mega_order_list = [None]*hippo_shop  # create new big list with number of item = number of kedai
            for i, sub_order_list in enumerate(mega_order_list):
                sub_order_list = copy.deepcopy(order_info_list)
                sub_order_list[0] = sub_order_list[0]+'.'+str(i+1)  # each suborder will have number increment after .
                # print(f"\nSuborderID: {sub_order_list[0]}")
                key = unique_key[i]
                new_food_info_list = []  # new empty list to store those foodinfo that matched key
                for j, food_info in enumerate(sub_order_list[2]):
                    result = food_info[0].find(key)  # check id key exist in food name
                    # print(f"food{j}, {key}, {food}, {result}")
                    if result != -1:  # if exist
                        new_food_info_list.append(food_info)  # append the food_info to the new list
                sub_order_list[2] = copy.deepcopy(new_food_info_list)
                # print(sub_order_list)
                mega_order_list[i] = copy.deepcopy(sub_order_list)
        # Done handling for multiple shop in 1 order

        else:
            mega_order_list = [order_info_list]
            hippo_shop = 1

    # handling for fast food delivery
    elif order_file_name.find('type3') != -1:  # fast food delivery (type2) handler
        order_info_list = [None]*9
        food_info_list = [None]*4
        match = re.search(r"formID(\d+)", order_file_name)  # extract formID from the filename
        order_info_list[0] = match.group(1)  # use formID as orderID
        regex_string_fast_food = re.compile(global_param.regex_in_fast_food)
        match = re.search(regex_string_fast_food, line)
        if match:
            order_info_list[5] = match.group(1)  # customer's name
            order_info_list[6] = match.group(2)  # customer's phone
            order_info_list[8] = match.group(3)  # customer's address
            order_info_list[3] = match.group(7)+' '+match.group(8)
            order_info_list[4] = match.group(4)  # restaurant name
            food_info_list[0] = match.group(5)  # food name
            order_info_list[2] = [food_info_list]  # food_info_list. need to list of list
            order_info_list[1] = match.group(7)+' ' + match.group(6)  # requested delivery time

        mega_order_list = [order_info_list]
        hippo_shop = 1
    # Done handling for fast food delivery

    else:
        order_info_list = ['no match']*9
        mega_order_list = [order_info_list]
        hippo_shop = 0

    return hippo_shop, mega_order_list


def add_shop():
    print('Restaurant not in the list. Please add Restaurant info.')
    name = input('Restaurant Name: ')
    name_id = input('Unique ID: ')
    address = input('Address: ')
    pic = input('Contact Person: ')
    phone_num = input('Phone Number: ')
    charge_type = input('Charge Type (1, 2, or 3): ')
    charge_amount = input('Charge Amount: RM')
    delivery_charge = input('Delivery Charge: RM')
    new_info = [name_id, name, address, pic, phone_num, charge_type,'0','0','0',delivery_charge]
    new_info[int(charge_type)+5] = charge_amount
    with open(global_param.shop_data_file, 'a', newline='') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        wr.writerow(new_info)
    return [name, address, pic, phone_num]


def get_shop_info(shop_info):
    # print("inside get_restaurant_info")
    # print(restaurant_info)
    name = shop_info
    address = None
    pic = None
    phone_num = None
    shop_info_list = [name, address, pic, phone_num]
    with open(global_param.shop_data_file, 'r') as file:
        next(file)  # skip csv header
        reader = csv.reader(file)
        found = False
        for line in reader:
            result = shop_info.lower().find(line[0])
            if result != -1:
                name = line[1]
                address = line[2]
                pic = line[3]  # person in-charge
                phone_num = line[4]
                found = True
                break
            else:
                pass
    if found:  # if found, update the list with result
        shop_info_list = [name, address, pic, phone_num]
    # print(shop_info_list)
    return shop_info_list


if __name__ == '__main__':
    orderFileName = 'type0_24012019.110811.html.txt'
    tag = ''
    # flattenRawEmail(orderFileName)
    numOfShop, megaOrderList = get_order_info(orderFileName)
    for orderInfoList in megaOrderList:
        foodInfoList = orderInfoList[2]
        shopInfoList = get_shop_info(orderInfoList[4])
        customerInfoList = orderInfoList[-4:]

        print('\nOrder Details:')
        print('orderFileName = ', end='')
        print("'"+orderFileName+"'")
        print('orderInfoList = ', end='')
        print(orderInfoList)
        print('foodInfoList = ', end='')
        print(foodInfoList)
        print('shopInfoList = ', end='')
        print(shopInfoList)
        print('customerInfoList = ', end='')
        print(customerInfoList)

        masterOrderList = data_processing.gen_master_order_list(orderInfoList, shopInfoList[0],
                                                                orderFileName, tag)
        masterFoodList = data_processing.gen_master_food_list(orderInfoList[0], shopInfoList[0],
                                                              foodInfoList, orderFileName, tag)
        print('masterOrderList = ', end='')
        print(masterOrderList)
        print('masterFoodList = ', end='')
        print(masterFoodList)
        pushTo = 'unit_test'
        print(f"Pushing data to {pushTo} csv...")
        data_processing.push_to_csv(pushTo, masterOrderList, masterFoodList)
