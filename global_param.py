#!python3
import time

work_path = 'C:\\Users\\mabrahma\\PycharmProjects\\projek_badak\\'
raw_email_path = work_path + 'raw_email\\'

unit_test_path = work_path + 'unit_test\\'
unit_test_order_data_file = unit_test_path + 'order_data.csv'
unit_test_food_data_file = unit_test_path + 'food_data.csv'

daily_path = work_path + 'daily_csv\\'
daily_order_data_file = daily_path + time.strftime("%b%d-%Y") + '_order_data.csv'
daily_food_data_file = daily_path + time.strftime("%b%d-%Y") + '_food_data.csv'

master_path = work_path + 'master_csv\\'
master_order_data_file = master_path + 'order_data.csv'
master_food_data_file = master_path + 'food_data.csv'

shop_data_file = master_path + 'restaurant.csv'

incoming_date_format = '%d/%m/%Y %I:%M %p'  # http://strftime.org/
pickup_to_delivery_gap = 15  # minutes
valid_arg_list = ['top_wrapper.py', 'debug', 'updatecsvmaster', 'updatecsvdaily',
                  'updatecsvunittest', 'genmsg', 'automode', 'autodatapush']

# email related parameters
username = 'hippofooddelivery@gmail.com'
server_name = 'imap.gmail.com'
email_folder = 'Inbox'
check_interval = 10  # sec
ok_subject = ['New order has been placed',
              'New order lunch Set has been placed',
              'Hello',
              'Hippo Fast Food Delivery',
              ]

# regex. https://regex101.com/
regex_in_order = r"Number: <\/strong>\s?([^<]+).*Place Time: <\/strong>\s?([^<]+)<\/p><hr(?: \/|><p)>(.*)(?:Tax Total|Delivery (?:Charge|Fee)).*Created on :<\/strong> ([^<]+)<\/p><p>([^<]+).*Information :<\/strong><\/p><p>(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>(.*)<br(?: \/)?>"
regex_in_food = r"Details<\/strong> : (.+)\s\((?:RM)?([^)]+).*Qty<\/strong> : ([^<]+).*Notes <\/strong>:\s?([^<]+)"
regex_in_fast_food = r"Nama</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Phone</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Alamat</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Nama Restoran</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Menu</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Masa Penghantaran</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*received at ([^ ]+) (.*)"

# list of request supported by Virtual Admin
rdReqList = ['status', 'msg2shop', 'msg2rider', 'riderName', 'help']
wrReqList = ['cancel', 'donepickup', 'donedeliver', 'updateaddress',
             'updatefood', 'updatephone', 'setrider']

# mouse position for theBridge
newMsgPixColor = (255, 255, 255)
newMsgPos = (1340, 930)
replyBoxPos = (1500, 1000)
reqBoxPos = (80, 45)
resBoxPos = (85, 70)

# print(daily_order_data_file)
