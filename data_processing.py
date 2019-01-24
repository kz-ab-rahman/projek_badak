#!python3
import csv
import re
import global_param


def get_charge_detail(restaurant_name):
    charge_list = []
    with open(global_param.shop_data_file, 'r') as file:
        next(file)  # skip csv header
        reader = csv.reader(file)
        found = False
        for line in reader:
            if line[1] == restaurant_name:
                charge_list = line[-5:]
                found = True
                break
            else:
                pass
    if not found:
        print(f"\nERROR: {restaurant_name} not in the list")
        charge_list = -1
        exit()
    return charge_list


def find_restaurant(key):
    with open(global_param.shop_data_file, 'r') as file:
        next(file)  # skip csv header
        reader = csv.reader(file)
        for line in reader:
            if line[5] == key:
                restaurant_name = line[1]
                break
            else:
                restaurant_name = 'no match'
    return restaurant_name


def gen_master_order_list(order_info_list, restaurant_name, order_file_name, tag):
    # Handling for fast food delivery
    if order_file_name.find('type3') != -1:  # fast food
        charge_list = get_charge_detail('fast food')
        charge_type = int(charge_list[0])
        delivery_charge = float(charge_list[-1])
        charge_to_shop = float(charge_list[charge_type])

        food_summary = order_info_list[2][0][0]
        total_food_quantity = None
        total_food_price = None
        charge_to_customer = None
        pay_to_shop = None
    # Done handling for fast food delivery
    else:
        if restaurant_name == 'Hippo Food Delivery':
            first_food = order_info_list[2][0][0]
            # print(first_food)
            match = re.search(r".*\((.*)\)", first_food)
            restaurant_key = match.group(1)
            restaurant_name = find_restaurant(restaurant_key)

        charge_list = get_charge_detail(restaurant_name)
        charge_type = int(charge_list[0])
        delivery_charge = float(charge_list[-1])
        charge_to_shop = float(charge_list[charge_type])  # charge to shop varies depends on charge type
        # print(charge_type,charge_to_shop,delivery_charge)

        # calculate total food price and quantity, and generate food summary
        total_food_price = 0
        total_food_quantity = 0
        food_summary = ''
        for i, foodItem in enumerate(order_info_list[2]):
            food = foodItem[0]
            unit_price = float(foodItem[1])
            # print(unit_price)
            quantity = int(foodItem[2])
            total_price = unit_price * quantity
            # print(total_price)
            total_food_quantity += quantity
            total_food_price += total_price
            if i > 0:
                spacer = '; '
            else:
                spacer = ''
            food_summary += spacer + str(quantity) + 'x ' + food
        charge_to_customer = total_food_price + delivery_charge
        if charge_type == 2:  # we charge shop per pack for type 2
            charge_to_shop = charge_to_shop * total_food_quantity
        pay_to_shop = total_food_price - charge_to_shop

    dummy_list = order_info_list.copy()
    del dummy_list[2]  # delete food list from master list. replace with summary
    dummy_list[3] = restaurant_name  # replace name+address with just name
    master_order_list = dummy_list
    master_order_list.extend(
        [food_summary, total_food_quantity, charge_type, total_food_price, delivery_charge,
         charge_to_customer, charge_to_shop, pay_to_shop, order_file_name, tag])  # append misc info
    # date reformatting for order 1892380 and below.
    order_id = float(master_order_list[0])
    if order_id <= 1892380:
        # print('date reformatting required')
        master_order_list[1] = reformat_date(master_order_list[1])
        master_order_list[2] = reformat_date(master_order_list[2])

    return master_order_list


def gen_master_food_list(order_id, restaurant_name, food_info_list, order_file_name, tag):
    if restaurant_name == 'Hippo Food Delivery':
        first_food = food_info_list[0][0]
        # print(first_food)
        match = re.search(r".*\((.*)\)", first_food)
        restaurant_key = match.group(1)
        restaurant_name = find_restaurant(restaurant_key)

    dummy_list = food_info_list.copy()
    for item in dummy_list:
        item.insert(0, order_id)
        item.insert(1, restaurant_name)
        item.extend([order_file_name, tag])
    return dummy_list


def push_to_csv(push_to, master_order_list, master_food_list):
    # tracking_list = [order_num, status, rider_name, pickup_actual, deliver_actual]
    tracking_list = ['not assigned', 'new', 'not assigned', None, None]
    if push_to == 'unit_test':
        order_data_file = global_param.unit_test_order_data_file
        food_data_file = global_param.unit_test_food_data_file
    if push_to == 'master':
        order_data_file = global_param.master_order_data_file
        food_data_file = global_param.master_food_data_file
    if push_to == 'daily':
        order_data_file = global_param.daily_order_data_file
        food_data_file = global_param.daily_food_data_file
        master_order_list.extend(tracking_list)  # append tracking_list before writing to file

    with open(order_data_file, 'a+', newline='') as my_file:
        wr = csv.writer(my_file, quoting=csv.QUOTE_ALL)
        wr.writerow(master_order_list)
    with open(food_data_file, 'a+', newline='') as my_file:
        wr = csv.writer(my_file, quoting=csv.QUOTE_ALL)
        for item in master_food_list:
            wr.writerow(item)
    return


def reformat_date(old_date):
    """
    reformat date from MM/DD/YYYY -> DD/MM/YYYY
    """
    match = re.search(r"(\d+)\/(\d+)(.*)", old_date)
    if match:
        new_date = match.group(2) + '/' + match.group(1) + match.group(3)
    else:
        print('ERROR: cannot reformat data')
        exit()
    return new_date


if __name__ == '__main__':
    tag = ''
    orderFileName = 'type0_24012019.110811.html.txt'
    orderInfoList = ['1946617', '23/01/2019 5:30 PM', [
        ['Kerabu Mangga/Sotong/Jejari Ayam/Somtam Betik/Somtam Seafood (Kerabu Mangga)', '6.00', '1', ' '],
        ['Tom Yam Ayam/Campur/Pok Tek (Tom Yam Campur)', '8.00', '1', ' '],
        ['Telur Bistik/Bungkus/Dadar (Telur Bungkus)', '5.00', '1', ' ']], '23/01/2019 10:10 AM',
                     'Kafe Mae Thai  Jalan Dagangan 8, 13200 Kepala Batas, Pulau Pinang, Malaysia', 'Dummy Order',
                     '1234', 'iffah.mohamed@gmail.com', 'xyz ']
    foodInfoList = [['Kerabu Mangga/Sotong/Jejari Ayam/Somtam Betik/Somtam Seafood (Kerabu Mangga)', '6.00', '1', ' '],
                    ['Tom Yam Ayam/Campur/Pok Tek (Tom Yam Campur)', '8.00', '1', ' '],
                    ['Telur Bistik/Bungkus/Dadar (Telur Bungkus)', '5.00', '1', ' ']]
    shopInfoList = ['Kafe Mae Thai', 'Jalan Dagangan 8, 13200 Kepala Batas, Pulau Pinang, Malaysia', 'none', 'none']
    customerInfoList = ['Dummy Order', '1234', 'iffah.mohamed@gmail.com', 'xyz ']

    masterOrderList = gen_master_order_list(orderInfoList, shopInfoList[0], orderFileName, tag)
    masterFoodList = gen_master_food_list(orderInfoList[0], shopInfoList[0], foodInfoList, orderFileName, tag)
    print('masterOrderList = ', end='')
    print(masterOrderList)
    print('masterFoodList = ', end='')
    print(masterFoodList)
    pushTo = 'unit_test'
    print(f"Pushing data to {pushTo} csv...")
    push_to_csv(pushTo, masterOrderList, masterFoodList)
