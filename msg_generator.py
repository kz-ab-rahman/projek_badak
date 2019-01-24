#!python3

import io
import urllib.parse
import global_param
from datetime import datetime, timedelta
from contextlib import redirect_stdout


def get_gmap_direction(raw_address):
    """
    https://developers.google.com/maps/documentation/urls/guide
    """
    gmap_dir_prefix = "https://www.google.com/maps/dir/?api=1&destination="
    gmap_dir_dest = urllib.parse.quote_plus(raw_address)
    gmap_dir_postfix = "&travelmode=driving"
    gmap_dir_url = gmap_dir_prefix+gmap_dir_dest+gmap_dir_postfix
    return gmap_dir_url


def print_common_info(order_num, shop, master_food_list, total_pack, rider, pay_to_shop):
    header = f"\n\
===HIPPO FOOD DELIVERY===\n\
*Order No: {order_num}*\n\
Nama Kedai: *{shop}*\n\
Pesanan:"

    print(header)
    for num, food_item in enumerate(master_food_list):
        unit_price = float(food_item[3])
        quantity = int(food_item[4])
        note = food_item[5]
        if note == ' ':
            pass
        else:
            note = '(note:'+note+')'
        print(f"{num+1}. {food_item[2]} (RM{unit_price:.2f}) x {quantity} set {note}")

    # print(f"Jumlah Pek: {total_pack}")
    print(f"Rider: {rider}")
    print(f"Bayar kpd {shop}: *RM{pay_to_shop:.2f}*")

    return


def gen_text_msg(master_order_list, master_food_list, order_num, rider):
    order_id = master_order_list[0]
    delivery_time = master_order_list[1]
    orderTime = master_order_list[2]
    shop = master_order_list[3]
    customer_name = master_order_list[4]
    customer_phone = master_order_list[5]
    customer_email = master_order_list[6]
    customer_address = master_order_list[7]
    total_pack = master_order_list[9]
    charge_type = master_order_list[10]
    total_food_price = master_order_list[11]
    delivery_charge = master_order_list[12]
    colect_from_customer = master_order_list[13]
    charge_to_shop = master_order_list[14]
    pay_to_shop = master_order_list[15]

    # calculate pick-up time
    delivery_time_obj = datetime.strptime(delivery_time, global_param.incoming_date_format)
    delivery_time = delivery_time_obj.strftime('%I:%M %p (%d %b, %Y)')
    pickup_time_obj = delivery_time_obj - timedelta(minutes=global_param.pickup_to_delivery_gap)
    pickup_time = pickup_time_obj.strftime('%I:%M %p (%d %b, %Y)')

    with io.StringIO() as buf, redirect_stdout(buf):
        # print("============== Message to Rider =================")
        print_common_info(order_num, shop, master_food_list, total_pack, rider, pay_to_shop)
        print("---------------------------------------------")
        print(f"Delivery Time: {delivery_time}")
        print(f"Customer: {customer_name}")
        print(f"Phone no: {customer_phone}")
        print(f"Address: {customer_address}")
        print(get_gmap_direction(customer_address))
        print(f"Cas Penghantaran: RM{delivery_charge:.2f}")
        print(f"Collect dari Customer: *RM{colect_from_customer:.2f}*")
        print(f"OrderID: {order_id}")
        msg_to_rider = buf.getvalue()
    with io.StringIO() as buf, redirect_stdout(buf):
        # print("============== Message to Shop =================")
        print_common_info(order_num, shop, master_food_list, total_pack, rider, pay_to_shop)
        print(f"Pick-up time: {pickup_time}")
        print(f"OrderID: {order_id}")
        msg_to_shop = buf.getvalue()

    return msg_to_rider, msg_to_shop


if __name__ == '__main__':
    # master_order_list = ['1899955', '03/01/2019 8:30 PM', '03/01/2019 6:33 PM', "Nan's Kitchen", 'Nizam Zain', '0135104516', 'nizamdiha@gmail.com', '18 Lorong Limonia 3  Bertam LAKESIDE ', "1x Nasi Goreng Cina; 1x Nasi Goreng Daging; 1x Nan's Special", 3, 1, 23.5, 4.0, 27.5, 0.0, 23.5, 'new_order_04012019.022721.html.txt', '']
    # master_food_list = [['1899955', "Nan's Kitchen", 'Nasi Goreng Cina', '6.50', '1', ' ', 'new_order_04012019.022721.html.txt', ''], ['1899955', "Nan's Kitchen", 'Nasi Goreng Daging', '7.00', '1', ' ', 'new_order_04012019.022721.html.txt', ''], ['1899955', "Nan's Kitchen", "Nan's Special", '10.00', '1', ' ', 'new_order_04012019.022721.html.txt', '']]

    master_order_list = ['1898054.1', '02/01/2019 12:30 PM', '02/01/2019 11:10 AM', "HippoFood (Nan's Kitchen)",
                         'nurul nadiah azmi', '01114430036', 'yon.paan@yahoo.com', 'no 55 g jalan dagangan 10 no 5 g',
                         '1x Nasi Ayam Kunyit (NK)', 1, 2, 7.0, 0.0, 7.0, 2.0, 5.0,
                         'new_order_04012019.022700.html.txt', '']
    master_food_list = [['1898054.1', "HippoFood (Nan's Kitchen)", 'Nasi Ayam Kunyit (NK)',
                         '7.00', '1', ' ', 'new_order_04012019.022700.html.txt', '']]

    # master_order_list = ['1899992', '03/01/2019 8:50 PM', '03/01/2019 7:48 PM', 'Char Koay Teow CIMB', 'Ayu  Halim', '0125550186', 'ayupali8684@gmail.com', '1728 Kepala Batas', '2x Char Koay Teow Biasa', 2, 3, 11.0, 4.0, 15.0, 1.0, 10.0, 'new_order_04012019.022731.html.txt', '']
    # master_food_list = [['1899992', 'Char Koay Teow CIMB', 'Char Koay Teow Biasa', '5.50', '2', ' ', 'new_order_04012019.022731.html.txt', '']]

    # master_order_list = ['1899890', '03/01/2019 2:25 PM', '03/01/2019 1:22 PM', 'Anjung Satay', 'Rozana Abd Rahim', '0134325494', 'rozana_ummizaim@yahoo.com', 'Jalan Perak, 13200 Kepala Batas 1', '2x Mee Tulang; 2x Nasi Daging', 4, 1, 28.0, 4.0, 32.0, 0.0, 28.0, 'new_order_04012019.022714.html.txt', '']
    # master_food_list = [['1899890', 'Anjung Satay', 'Mee Tulang', '7.00', '2', ' ', 'new_order_04012019.022714.html.txt', ''], ['1899890', 'Anjung Satay', 'Nasi Daging', '7.00', '2', ' ', 'new_order_04012019.022714.html.txt', '']]

    order_num = 1
    rider = '?'

    msg_to_rider, msg_to_shop = gen_text_msg(master_order_list, master_food_list, order_num, rider)
    print(msg_to_rider)
    print(msg_to_shop)
