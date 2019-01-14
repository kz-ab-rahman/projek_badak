#!python3
import time

workPath = 'C:\\Users\\mabrahma\\Documents\\projek_badak\\'
rawEmailPath = workPath+'raw_email\\'
dailyOrderPath = workPath+'daily_order\\'
dailyOrderDataFile = dailyOrderPath+time.strftime("%b%d-%Y")+'_order_data.csv'
restaurantDataFile = workPath+'restaurant.csv'
orderDataFile = workPath+'order_data.csv'
foodDataFile = workPath+'food_data.csv'
incomingDateFormat = '%d/%m/%Y %I:%M %p' #http://strftime.org/
pickupToDeliveryGap = 15 #minutes

#email related parameters
usernm = 'hippofooddelivery@gmail.com'
serverName = 'imap.gmail.com'
emailFolder = 'Inbox'
checkInterval = 10 #sec
okSubject= ["New order has been placed",
            "Hello",
            "Hippo Fast Food Delivery",]

#regex. https://regex101.com/
regexInOrder = 'Number: <\/strong>\s?([^<]+).*Place Time: <\/strong>\s?([^<]+)<\/p><hr(?: \/|><p)>(.*)(?:Tax Total|Delivery (?:Charge|Fee)).*Created on :<\/strong> ([^<]+)<\/p><p>([^<]+).*Information :<\/strong><\/p><p>(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>\s?(.*)<br(?: \/)?>(.*)<br(?: \/)?>'
regexInFood = 'Details<\/strong> : (.+)\s\((?:RM)?([^)]+).*Qty<\/strong> : ([^<]+).*Notes <\/strong>:\s?([^<]+)'
regexInFastFood = 'Nama</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Phone</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Alamat</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Nama Restoran</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Menu</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*Masa Penghantaran</td><td style3D\"background:#fff; padding:10px;\">([^<]+).*recieved at ([^ ]+) (.*)'
#list of request supported by Virtual Admin
rdReqList = ['status', 'msgkedai', 'msgrider', 'rider']
wrReqList = ['cancel', 'donepickup', 'donedeliver', 'updateaddress', 'updatefood', 'updatephone', 'setrider']


#print(dailyOrderDataFile)